# Notexio — Submission Report (STAR) + GitHub Page + Demo Video Script

## GitHub Pages link (submission)

- **Project page**: https://nafisatabassum30.github.io/Notexio/
- **Repo**: https://github.com/nafisatabassum30/Notexio

> If the page isn’t live yet: in GitHub go to **Settings → Pages → Build and deployment** and set:
> - **Source**: Deploy from a branch
> - **Branch**: `main`
> - **Folder**: `/docs`

---

## Short project introduction (what I built)

**Notexio** is a lightweight, customizable text editor built with **Python + Tkinter**. It demonstrates OS/project fundamentals (file I/O, GUI/event-driven programming, persistent settings) and practical editor features (recent files, find/replace, formatting, themes, PDF export, print, recovery).

Key modules (separation of concerns):
- `src/file_manager.py`: open/save/save-as, recent files, unsaved-change prompts
- `src/safety_features.py`: recovery file creation + startup restore prompt
- `src/misc_features.py`: print/preview + PDF export (ReportLab) + drag/drop hooks
- `src/ui_components.py`: toolbar, status bar, line numbers
- `src/settings_manager.py`: settings persistence in `config/settings.json`

---

## STAR report — challenges faced

### 1) Preventing data loss (unsaved changes + recovery)

- **Situation**: GUI editors feel “unsafe” if a user can accidentally close or open a new file and lose edits.
- **Task**: Add safety checks before destructive actions and implement a lightweight recovery mechanism.
- **Action**:
  - Implemented an **unsaved-changes guard** using a Yes/No/Cancel dialog so users can save, discard, or abort (`FileManager.check_unsaved_changes`).
  - Implemented **recovery snapshots** written to a `recovery/` folder with timestamps and capped to the most recent files (`SafetyFeatures.create_recovery_file`, `cleanup_old_recovery_files`).
  - On startup, scan for recovery files and prompt restore of the newest one (`SafetyFeatures.check_recovery_files`).
- **Result**: Users get predictable protection against accidental loss: destructive operations are gated, and a recovery path exists after crashes/forced closes.

### 2) Keeping the app maintainable as features grew (modular architecture)

- **Situation**: As the feature list expanded (tools, formatting, theme, safety, printing, etc.), a single “god file” would become hard to reason about and error-prone.
- **Task**: Organize features so each subsystem can be developed/tested independently while still integrating cleanly into the Tkinter app.
- **Action**:
  - Designed the app as small, focused classes (Editor / FileManager / EditOperations / Formatter / ViewManager / Tools / ThemeManager / SafetyFeatures / UIComponents / SettingsManager / MiscFeatures).
  - Wired them together in `main.py` with a single “composition root” (`NotexioApp`) to keep dependencies explicit.
  - Centralized shared UI updates (title/status bar/line numbers) to reduce duplicated state handling.
- **Result**: Faster iteration and fewer regressions because logic is isolated by responsibility; adding features doesn’t require touching unrelated code.

### 3) Cross-platform “extras” (PDF export + printing + drag/drop)

- **Situation**: Printing and drag/drop vary significantly across OSes; adding them can break portability.
- **Task**: Provide these features while keeping the app usable on Windows/Linux/macOS.
- **Action**:
  - Implemented **PDF export** using ReportLab as an optional dependency (`requirements.txt` already includes `reportlab>=4.0.0`).
  - Implemented printing via:
    - Windows: `pywin32` (optional) using `win32print`/`ShellExecute`
    - Linux/macOS: fallback to `lp`/`lpr`
  - Implemented drag/drop with `tkinterdnd2` on Windows (optional) and graceful fallback elsewhere.
- **Result**: Feature-rich experience without locking the project to one OS; optional dependencies are handled with clear user messaging.

---

## 2–5 minute video demo script (recording plan)

**Target length**: ~3:30 (fits the 2–5 min requirement)

- **0:00–0:15 — Intro**
  - “Hi, I’m ___, this is Notexio — a Python/Tkinter text editor showcasing file I/O, GUI events, and safety features.”

- **0:15–0:45 — Core flow (New/Open/Save)**
  - Create a new file, type a few lines.
  - Save As → show `.txt` default.

- **0:45–1:20 — Edit productivity**
  - Find (Ctrl+F) + Replace (Ctrl+H).
  - Go to Line (Ctrl+G).

- **1:20–1:55 — UX polish**
  - Show status bar updating (Ln/Col + character count).
  - Toggle line numbers (View → Line Numbers).

- **1:55–2:30 — Safety demo (unsaved changes + recovery)**
  - Make an edit → show `*` in title/status.
  - Try to open another file → show unsaved prompt (Save/Don’t Save/Cancel).
  - Mention recovery files and restore prompt on startup.

- **2:30–3:05 — “Nice to have” features**
  - Theme switch (Light/Dark).
  - Export as PDF (File → Export as PDF).

- **3:05–3:30 — Engineering highlight (skills + structure)**
  - Briefly show project structure in the repo: modules for file ops, safety, UI, settings.
  - Close with GitHub Pages link.

**Tip for the recording**: keep your cursor movements deliberate and use keyboard shortcuts on-screen (Ctrl+S, Ctrl+F, Ctrl+H) to highlight efficiency.
