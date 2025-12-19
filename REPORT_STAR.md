# Notexio (Python/Tkinter Text Editor) — STAR Report

This report summarizes key development challenges I faced while building **Notexio**, a lightweight text editor in Python (Tkinter), using the **STAR** method.

---

## Challenge 1 — Keeping the app maintainable as features grew

### Situation
As features expanded (file operations, formatting, view controls, tools, themes, safety features), a single-file approach became hard to reason about, and small changes risked breaking unrelated functionality.

### Task
Design the project so new features could be added quickly while keeping the UI responsive and the code easy to test and debug.

### Action
- Split responsibilities into focused modules (`file_manager.py`, `edit_operations.py`, `formatter.py`, `view_manager.py`, `tools.py`, `theme_manager.py`, `safety_features.py`, `ui_components.py`, `settings_manager.py`).
- Used a central app entry point (`main.py`) to wire dependencies and keep feature modules loosely coupled.
- Standardized how modules interact with the editor state (current file, modified flag, title updates, status bar updates).

### Result
- Feature work became faster because each capability had a clear “home.”
- Bugs became easier to localize (module boundaries reduced side effects).
- The UI stayed consistent because common editor state updates were centralized.

---

## Challenge 2 — Preventing data loss (unsaved changes + recovery)

### Situation
Text editors fail the user when they lose work. Closing the window, crashes, or forgetting to save can cause data loss.

### Task
Implement safety behavior that matches user expectations: warn on exit if there are unsaved changes, and support recovery when possible.

### Action
- Tracked editor modification state via Tkinter’s `<<Modified>>` event and updated the window title with an unsaved indicator (`*`).
- Added exit-time checks to warn the user before closing when content has changed.
- Implemented recovery file creation and a startup flow that detects recovery files and offers restoration.

### Result
- The app protects users from accidental closes with unsaved content.
- Recovery flow improves trust: even after unexpected interruptions, users can restore recent work.

---

## Challenge 3 — Building a polished “Notepad-like” UX in Tkinter

### Situation
Tkinter is powerful but low-level: recreating familiar editor UX (status bar, toolbar actions, shortcuts, clean layout, line numbers, zoom, word wrap) requires careful event wiring and layout management.

### Task
Deliver a smooth, modern editing experience with productivity features and consistent keyboard shortcuts.

### Action
- Implemented a Windows-Notepad-inspired menu structure with accelerators and bound keyboard shortcuts (Ctrl+S/Ctrl+F/Ctrl+H/etc.).
- Added a toolbar and status bar, and ensured they update when the caret position or document state changes.
- Implemented view controls (zoom in/out/reset, fullscreen, optional line numbers, word wrap toggle).
- Designed default styling for readability (font, padding, selection colors) and added theme toggles (light/dark).

### Result
- The editor feels familiar and efficient for users coming from Notepad-style workflows.
- Keyboard-first actions work reliably, which is essential for productivity.
- The app presents a cohesive UI despite being built with a minimal GUI toolkit.

---

## Summary
Using STAR, the main challenges were **maintainability**, **data safety**, and **UX polish**. By modularizing the codebase, tracking editor state carefully, and wiring UI events consistently, Notexio achieves a reliable, feature-rich editor experience in Python/Tkinter.
