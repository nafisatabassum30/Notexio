# Notexio (CSE323 — Operating Systems Design)  
## Project Report (STAR-format challenges)

**Project name:** Notexio Text Editor  
**Course:** CSE323 — Operating Systems Design  
**Semester/Section:** _[Fill]_  
**Student name:** _[Fill]_  
**Student ID:** _[Fill]_  
**Instructor:** _[Fill]_  
**Date:** 2025-12-20  

---

## 1) Abstract
Notexio is a lightweight text editor built with Python and Tkinter. The project was designed as an OS-oriented application to practice **file I/O**, **data persistence**, **event-driven GUI programming**, and **safe recovery mechanisms** in the presence of crashes, forced exits, or unexpected shutdowns. The final system supports common editor workflows (open/save, undo/redo, find/replace), usability features (status bar, line numbers, zoom, themes), and OS-adjacent integrations (printing via platform tools and exporting to PDF).

---

## 2) Project Overview
### 2.1 Goals
- Build a stable, user-friendly editor that behaves like a modern Notepad-style app.
- Demonstrate OS concepts through real features:
  - **File system interaction:** open/save, recent files, safe persistence
  - **Concurrency considerations:** auto-save without blocking UI
  - **Process/tool invocation:** printing via system commands or Windows APIs
  - **Fault tolerance:** recovery files and cleanup policies

### 2.2 Key Features Implemented
- **File operations:** New/Open/Save/Save As, “Open Recent”, unsaved-change prompts
- **Editing:** Undo/Redo, clipboard operations, Find/Replace, Go To Line
- **View:** Zoom in/out/reset, word wrap, fullscreen, optional line numbers
- **Tools:** word/character/line counts, reading time estimate, duplicate-word highlight, remove extra spaces
- **Themes:** light/dark/custom themes
- **Safety:** optional auto-save, crash recovery files, warning on exit
- **Export/print:** export as PDF, print preview, printing (platform-dependent)

---

## 3) System Design & Architecture
### 3.1 High-level structure
Notexio uses a modular architecture. `main.py` wires together the components and passes shared references so modules can coordinate without duplicating state.

**Modules (high-signal responsibilities):**
- `src/editor.py`: the Tkinter root and main text widget; tracks modification state and title updates
- `src/file_manager.py`: open/save operations, recent files, unsaved-change prompts
- `src/edit_operations.py`: find/replace/go-to-line and clipboard + undo/redo helpers
- `src/formatter.py`: font and visual formatting controls
- `src/view_manager.py`: zoom/word-wrap/fullscreen logic
- `src/tools.py`: document statistics and text-cleanup utilities
- `src/theme_manager.py`: theme application across UI widgets
- `src/safety_features.py`: recovery file creation and auto-save loop
- `src/misc_features.py`: printing, print preview, PDF export, drag/drop (Windows)
- `src/settings_manager.py`: JSON settings persistence (`config/settings.json`)

### 3.2 Data flow (typical “Save” path)
1. User edits text → `Editor` marks document as modified (dirty flag)  
2. User triggers Save → `FileManager` reads content from widget and writes to disk  
3. `SettingsManager` persists recent files and preferences (theme/window size/etc.)

### 3.3 OS concepts reflected in the implementation
- **File I/O + persistence:** explicit open/read/write using OS files; recent files persisted in JSON
- **Reliability:** recovery files act as “journaling lite” for user text content
- **Concurrency model:** GUI is an event loop; long-running tasks must not block it
- **System integration:** printing delegates to OS-level tooling (`lp`/`lpr`) or Windows APIs

---

## 4) Challenges Faced (STAR format)

### Challenge 1 — “Dirty state” stayed incorrect after programmatic loads/saves
**Situation:** When opening or programmatically replacing text in a Tkinter `Text` widget, Tkinter can still consider the buffer “modified”, which can cause false unsaved-change prompts or a permanent `*` in the title/status.  
**Task:** Ensure the app’s “modified” state is accurate and matches real user edits, not internal loading operations.  
**Action:** Implemented a clear boundary between “programmatic text set” and “user edits” by resetting Tk’s internal modified flag after `open_file()`, `new_file()`, `save_file()`, and `save_as_file()` logic completes. Kept the app-level flag (`Editor.is_modified`) synchronized with the UI title and status bar.  
**Result:** Opening/saving no longer triggers false “unsaved changes” dialogs, and the window title reliably shows `*` only when the user has actually changed content.

**Theory (why this matters):** GUI text components often maintain internal state (like a “modified” bit) used for event generation. If an app writes to the widget from code, the widget cannot always infer intent (“load file” vs “user typed”), so the application must explicitly reset/acknowledge the modification state.

---

### Challenge 2 — Auto-save crashed intermittently (threading + Tkinter)
**Situation:** The auto-save mechanism ran on a background thread to avoid freezing the UI. However, Tkinter widgets are **not thread-safe**; reading UI state from a non-main thread can cause random crashes or undefined behavior.  
**Task:** Keep the UI responsive while still generating recovery files safely and reliably.  
**Action:** Updated auto-save to schedule recovery creation onto Tkinter’s main event loop using `root.after(...)`. The worker thread only sleeps and triggers scheduling; the actual widget read happens on the UI thread.  
**Result:** Auto-save remains non-blocking while eliminating thread-safety crashes.

**Theory (thread confinement):** Many GUI frameworks (including Tkinter/Tk) require that widget access happens only on the thread running the GUI event loop. `after()` queues work onto that loop, preserving correctness while still allowing background timing.

---

### Challenge 3 — Recovery files could grow without bounds
**Situation:** Recovery files are intentionally redundant; without a retention policy, the folder can grow indefinitely and waste storage.  
**Task:** Keep recovery useful while preventing uncontrolled disk growth.  
**Action:** Implemented a cleanup policy that keeps only the most recent recovery files (by modification time). Old files are removed automatically after creating a new recovery snapshot.  
**Result:** Recovery remains available for “last edits” scenarios while storage stays bounded.

**Theory (bounded logs):** OS and systems software commonly apply log rotation/retention policies. The same idea applies here: recovery is a log of snapshots, and retention prevents resource exhaustion.

---

### Challenge 4 — Export to PDF failed on special characters
**Situation:** PDF export uses ReportLab `Paragraph` objects, which accept a markup-like syntax. Unescaped characters such as `&`, `<`, and `>` can break parsing and cause export failures.  
**Task:** Make PDF export robust for normal text files containing symbols (e.g., code snippets, HTML, shell commands).  
**Action:** Escaped reserved markup characters before creating `Paragraph` objects. Split content into paragraph blocks and added spacing for readability.  
**Result:** PDF export works reliably across typical user content.

**Theory (escaping):** When a renderer supports markup, raw user text must be escaped to prevent accidental interpretation as formatting instructions.

---

### Challenge 5 — Cross-platform printing behavior differed by OS
**Situation:** Printing is not “one API” across platforms. Windows printing often goes through Win32 APIs (e.g., via `pywin32`), while Linux/macOS typically use `lp`/`lpr`.  
**Task:** Provide a print feature that works on multiple OSes with graceful fallbacks.  
**Action:** Implemented OS detection: use Windows printing via `pywin32` when available; otherwise fall back to invoking system printing commands on Unix-like systems. For missing dependencies, show clear guidance rather than failing silently.  
**Result:** Printing works where supported, and the app provides actionable feedback where additional OS tooling is needed.

**Theory (OS abstraction boundaries):** Applications frequently bridge portable UI logic with OS-specific system services. Runtime detection + optional dependencies is a practical approach for course projects.

---

### Challenge 6 — Status bar column index mismatched user expectations
**Situation:** Tkinter reports cursor column indices as **0-based**, but Notepad-style UIs typically show **1-based** columns.  
**Task:** Match “expected UX” so the status bar feels correct and professional.  
**Action:** Converted the internal column index to a user-facing one by adding \(+1\) before display.  
**Result:** The status bar now shows “Ln 1, Col 1” at the start of a new document, matching Notepad behavior.

---

## 5) Validation / Test Plan (manual)
- **File I/O**
  - Open a `.txt`, edit, save, re-open: content matches
  - Save As default extension: created file includes `.txt` when omitted
  - Recent files list updates after open/save
- **Safety**
  - Modify text → close → prompted to save
  - Create recovery file → restart → restore prompt appears
  - Auto-save enabled: recovery snapshots appear periodically
- **Export & print**
  - Export PDF with special characters `< & >` works
  - Print Preview displays full content
- **UX**
  - Status bar shows correct line/column and `*` indicator only when modified
  - Zoom updates status bar percentage
  - Dark mode updates toolbar + status bar colors

---

## 6) How to Run
```bash
pip install -r requirements.txt
python main.py
```

---

## 7) Submission Package (matches course screenshot requirements)
- **GitHub folder submission**
  - `docs/Notexio_CSE323_Project_Report.pdf` (this report)
  - Optional: `docs/Notexio_CSE323_Project_Report.md` (editable source)

- **GitHub page link submission**
  - Recommended: enable GitHub Pages for this repo and point it to `/docs` or the root + a `docs/index.html` (optional).
  - Put your final Pages link here: _[Fill after enabling]_  

- **Submission video demo (2–5 minutes)**
  - Suggested demo flow:
    - Open app → show menus/toolbar/status bar
    - Open a file → edit → Save → show recent files
    - Show Find/Replace + Go To Line
    - Toggle theme (light/dark)
    - Export as PDF
    - Show recovery behavior (briefly: show recovery folder or restore prompt)
  - Add your demo video link here: _[Fill]_  

- **Short introduction**
  - Notexio is a Tkinter-based Notepad-style editor focused on OS concepts: persistence, reliability, and safe interactions with the file system and system tools.

