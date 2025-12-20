# Notexio — CSE323 (Operating Systems Design) Project Report
**Project**: Notexio Text Editor (Python + Tkinter)  
**Course**: CSE323 — Operating Systems Design  
**Version**: 1.0.0  
**Date**: 2025-12-20  
**Author**: _<Your Name>_  
**Student ID**: _<Your ID>_

---

## Short introduction (what the project is)
Notexio is a lightweight, customizable text editor built with **Python** and **Tkinter**. It was designed as an operating-systems-focused course project to demonstrate practical OS-adjacent concepts such as **file I/O**, **safe persistence**, **event-driven GUI programming**, and **basic OS integration** (printing, filesystem interactions, configuration storage).

Key features include:
- File operations (new/open/save/save as, recent files)
- Edit operations (undo/redo, find/replace, go-to-line)
- Formatting (font family/size, bold/italic/underline, colors)
- View controls (zoom, fullscreen, word wrap, line numbers)
- Tools (word/char/line count, reading time, duplicate highlighting)
- Safety features (unsaved-change prompts, recovery files, optional auto-save)
- Export as PDF, print preview, printing (platform dependent)

---

## GitHub submission links (required)
- **GitHub repository**: _<paste your repo link here>_
- **GitHub Pages link**: _<paste your GitHub Pages link here (e.g., https://USERNAME.github.io/REPO/ )>_
- **2–5 minute demo video**: _<paste your YouTube/Drive link here>_

---

## Project structure (high-level)
The project is modular, with each feature group placed into its own component:
- `main.py`: application entry point, menu bar, shortcut bindings
- `src/editor.py`: main editor widget setup and core editor state
- `src/file_manager.py`: open/save/recent files + unsaved-change workflow
- `src/edit_operations.py`: undo/redo, clipboard ops, find/replace, go-to-line
- `src/formatter.py`: fonts/colors and text styling
- `src/view_manager.py`: zoom, word wrap, fullscreen, line-number font syncing
- `src/tools.py`: statistics and cleanup tools
- `src/safety_features.py`: recovery files + optional auto-save
- `src/misc_features.py`: drag & drop (optional), printing, PDF export
- `src/settings_manager.py`: persisted preferences in `config/settings.json`
- `src/ui_components.py`: toolbar, status bar, line numbers UI

This structure helped keep the OS-facing concerns (persistence, recovery, external integration) separate from pure UI concerns.

---

## OS / Systems concepts demonstrated
- **File I/O and persistence**
  - Opening/saving text files using UTF-8, managing file paths, handling exceptions.
  - Maintaining an application-level “modified” state so the user is protected from data loss.
- **Safe shutdown and data-loss prevention**
  - A “warn on exit” flow (save / don’t save / cancel) mirrors real desktop apps.
  - Recovery-file strategy: periodic snapshots are saved to disk and offered on startup.
- **Threads vs. UI event loops**
  - Tkinter runs a **single-threaded event loop**; it must own all widget access.
  - Background operations (like periodic auto-save timing) can run in a thread, but must hand work back to the UI thread safely.
- **Cross-platform OS integration**
  - Printing differs across Windows vs. Linux/macOS; Notexio uses OS-appropriate mechanisms and provides fallback warnings when dependencies are missing.

---

## Challenges faced (STAR format) — problems and fixes
Below are the major technical problems encountered during development, written in **STAR** format (Situation, Task, Action, Result). Where necessary, theoretical details are included to justify the fix.

---

### Challenge 1 — Auto-save crashes due to unsafe Tkinter access (Thread-safety)
**Situation**: Auto-save was implemented using a background thread that periodically created recovery files. Occasionally, the editor would freeze or behave inconsistently during auto-save.  
**Task**: Implement recovery snapshots without crashing or blocking the UI, while keeping periodic auto-save.  
**Action**:
- Identified the root cause: Tkinter widgets are **not thread-safe**. Calling `text_widget.get(...)` from a non-UI thread can cause undefined behavior.
- Changed auto-save to **schedule a snapshot on the UI thread** using `root.after(...)`, then wrote the recovery file to disk in a background thread (filesystem work does not need UI thread).
- Improved filename uniqueness by adding millisecond precision to timestamps to prevent collisions when multiple snapshots happen quickly.

**Result**:
- Auto-save became stable and predictable.
- UI remained responsive because content snapshot is fast and file writes happen asynchronously.
- Recovery file collisions were avoided.

**Theory (why this works)**:
Tkinter’s event loop is single-threaded; widget operations must occur on that thread. `after()` safely enqueues work on the UI loop. This is a common “handoff” pattern: **thread does timing → UI thread snapshots → worker thread writes**.

---

### Challenge 2 — Preventing data loss on exit (Unsaved-change workflow)
**Situation**: Users could close the application and lose work unless the editor consistently tracked modifications and prompted correctly.  
**Task**: Make the “close” behavior safe and consistent (save / don’t save / cancel), similar to a real editor.  
**Action**:
- Maintained an explicit `is_modified` flag representing unsaved changes.
- On “new/open/exit”, executed a **three-choice prompt** (Yes / No / Cancel) and routed the outcome to save logic.
- Updated UI feedback (title/status bar `*`) when modifications occurred, to align user expectation with actual persistence state.

**Result**:
- Accidental data loss was prevented.
- Editor behavior matched real-world desktop application UX.

**Theory**:
This is an application-level consistency contract: the UI is an abstraction over the filesystem. Because OS writes are explicit operations, the editor must track “dirty state” and gate destructive actions.

---

### Challenge 3 — “Open Recent” menu opened the wrong file (Closure capture bug)
**Situation**: The Recent Files menu was generated dynamically. A common Tkinter bug is that lambdas inside loops can capture the same variable, causing every menu item to open the last file in the list.  
**Task**: Ensure each menu entry opens the correct file it corresponds to.  
**Action**:
- Used a lambda with a **default argument** to freeze the current path:
  - `command=lambda fp=filepath: open_file(fp)`
- Also refreshed the recent-files menu after file operations so it stays accurate.

**Result**:
- Each menu item reliably opened the intended file.

**Theory**:
In Python, closures capture variables by reference (late binding). Default arguments evaluate immediately and store the value, eliminating the late-binding issue.

---

### Challenge 4 — PDF export broke on special characters (Markup escaping)
**Situation**: PDF export uses ReportLab `Paragraph`, which interprets the input as markup-like text. If the document contained characters such as `&`, `<`, or `>`, the export could fail or render incorrectly.  
**Task**: Export any plain-text content to PDF without errors.  
**Action**:
- Escaped markup-sensitive characters (`&`, `<`, `>`) before creating a `Paragraph`.
- Split the document by lines and added spacing so paragraphs remain readable.

**Result**:
- PDF export became robust for normal text documents (including code-like content).

**Theory**:
ReportLab `Paragraph` uses a lightweight markup language. Escaping prevents the parser from interpreting plain-text content as tags/entities.

---

### Challenge 5 — Printing is OS-dependent (Windows vs. Linux/macOS)
**Situation**: Printing is not a single portable API in Python. Windows printing often relies on `pywin32`, while Unix-like systems typically use `lp`/`lpr`.  
**Task**: Provide printing that works when possible and fails gracefully when not.  
**Action**:
- On Windows, attempted `win32print`/`win32api` printing; if unavailable, displayed a clear dependency message.
- On Linux/macOS, wrote to a temp file and invoked `lp` (Linux) or `lpr` (macOS).
- Added a “Print Preview” window to let users validate output before printing.

**Result**:
- Printing works across platforms when the OS tooling exists.
- The app degrades gracefully instead of crashing.

**Theory**:
Printing is an OS service accessed through platform-specific layers. A robust application must detect capabilities and provide fallbacks and user guidance.

---

### Challenge 6 — Line numbers drifted during scrolling (UI sync)
**Situation**: When line numbers were enabled, scrolling could desynchronize the line-number gutter from the text area.  
**Task**: Keep the gutter aligned with the text widget while scrolling and editing.  
**Action**:
- Regenerated line numbers on modifications (`<<Modified>>`) and attempted to synchronize scroll using `yview` data.
- Applied `yview_moveto(...)` on the gutter to match the editor’s scroll fraction.
- Re-packed widgets carefully when toggling line numbers so layout remained stable.

**Result**:
- Line numbers stayed visually aligned with the text during normal use.

**Theory**:
GUI sync issues are often caused by multiple scrolling sources (mousewheel, scrollbar, programmatic scrolling). Using `yview()` as the single source of truth helps prevent drift.

---

## Test plan (what I verified)
- Open/save files and verify correct content persisted.
- Modify content, verify `*` indicator and prompt-on-exit flow.
- Generate and restore recovery files from `recovery/`.
- Export PDF and open it to verify readability.
- Toggle line numbers and scroll to ensure gutter remains aligned.

---

## Demo video plan (2–5 minutes, required)
Recommended flow for your submission demo:
1. Quick introduction + show GitHub repo and GitHub Pages page.
2. Create a new file, type content, show modified indicator.
3. Use Find/Replace and Go-to-Line quickly.
4. Demonstrate recent files list.
5. Toggle theme/zoom/line numbers.
6. Export as PDF and open the output.
7. Close the app with unsaved changes to show the safety prompt.

---

## Conclusion
Notexio demonstrates OS design concepts through a real GUI application: safe file I/O, graceful OS integration, and reliability-focused features like recovery and safe shutdown. The biggest lessons were around event-driven design, cross-platform behavior, and building safeguards that mirror professional desktop editors.

