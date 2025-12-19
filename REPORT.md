# Notexio Text Editor — STAR Challenges Report

Notexio is a lightweight, Windows Notepad-inspired text editor built in **Python + Tkinter**. The project focuses on practical OS-adjacent workflows: file I/O, persistence, recovery, and responsive GUI behavior.

---

## STAR #1 — Preventing data loss (unsaved changes, recovery, auto-save)

- **Situation (challenge)**: Text editors are unforgiving—closing the window or a crash can lose work instantly. Tkinter doesn’t provide “document safety” for free, and state can get out of sync (file name vs. modified flag vs. UI).
- **Task (what I needed to do)**: Add a reliable “unsaved changes” flow (prompting the user), plus recovery files and startup restore so users can get work back after unexpected exits.
- **Action (what I did)**:
  - Tracked document state via `Editor.is_modified` using the `<<Modified>>` event and updated the window title with an unsaved indicator (`*`).
  - Implemented a consistent save/exit gate with `FileManager.check_unsaved_changes()` and reused it from the main close handler (`SafetyFeatures.warn_on_exit()`).
  - Added an auto-save recovery mechanism (`SafetyFeatures`) that periodically writes `.recovery` snapshots in a dedicated `recovery/` directory, then cleans up older files to keep storage bounded.
  - On app startup, scanned for recovery files and prompted the user to restore the latest one.
- **Result (outcome)**:
  - Users are warned before losing work and can recover content after an unexpected exit.
  - Recovery storage is automatically managed (keeps the most recent snapshots), reducing clutter while still protecting work.

---

## STAR #2 — Keeping the UI responsive while constantly updating status/line numbers

- **Situation (challenge)**: A text editor UI updates frequently (cursor position, character counts, file status). In Tkinter, doing too much work on every keystroke can make typing feel laggy.
- **Task (what I needed to do)**: Provide a “Notepad-style” status bar (line/column + character count + filename/modified indicator) and optional line numbers, without degrading typing responsiveness.
- **Action (what I did)**:
  - Centralized “UI readouts” in `UIComponents.update_status_bar()` and bound it to key/click events.
  - Used `after(...)` scheduling for one of the key bindings to avoid measuring the text widget before it finishes updating.
  - Implemented line numbers as an opt-in feature (`toggle_line_numbers`) and guarded updates so the line-number renderer only runs when the sidebar is visible.
  - Synced scrolling by reading the main text widget’s `yview()` and applying it to the line numbers view.
- **Result (outcome)**:
  - Users get real-time feedback (cursor position + character count + file status) in a familiar layout.
  - Line numbers are available when needed, and the app avoids paying that rendering cost unless the user enables the sidebar.

---

## STAR #3 — Cross-platform features with optional dependencies (graceful degradation)

- **Situation (challenge)**: Features like drag & drop, printing, and PDF export differ across OSes and often require extra packages (e.g., Windows-only APIs). Hard dependencies would break installs on other platforms.
- **Task (what I needed to do)**: Provide these capabilities where possible, but keep the core editor stable on any machine (Windows/macOS/Linux) even if optional packages are missing.
- **Action (what I did)**:
  - Detected the platform (`sys.platform`) and wrapped optional imports in `try/except ImportError` (e.g., `tkinterdnd2`, `pywin32`, `reportlab`).
  - Implemented OS-specific print paths (Windows via `win32api/win32print`, Unix-like via `lp`/`lpr`) with clear user-facing fallback messages when requirements aren’t met.
  - Kept the core editor independent from these extras so the app still runs even when optional modules aren’t installed.
- **Result (outcome)**:
  - Notexio runs with core editing features everywhere, while advanced integrations activate only when the platform and dependencies support them.
  - Error handling is user-friendly (actionable install hints instead of crashes).

---

## GitHub Pages submission (what to submit)

- **GitHub Pages link**: Enable Pages for this repo and submit the resulting site URL (template: `https://<github-username>.github.io/<repo-name>/`).
- **Recommended setup**: Deploy from the `main` branch using the `/docs` folder (added in this change).

Steps:
1. Go to **Repo Settings → Pages**
2. Under **Build and deployment** choose **Deploy from a branch**
3. Select **Branch: `main`** and **Folder: `/docs`**
4. Save, wait for deployment, then copy the provided URL

---

## 2–5 minute video demo (ready-to-record script)

**0:00–0:20 — Intro**
- “Hi, I’m <Your Name>. This is **Notexio**, a lightweight text editor in Python + Tkinter inspired by Windows Notepad.”
- “My focus was building real-world editor workflows: file safety, UI feedback, and cross-platform features.”

**0:20–1:10 — Core workflow**
- Create a new file, type a few lines.
- Show the title changes to include `*` after edits.
- Save the file, show the `*` disappears and the filename appears in the status bar.

**1:10–1:50 — Safety features**
- Make an edit, attempt to close: show the unsaved changes prompt.
- (Optional) Briefly explain auto-save + recovery: “Notexio can write periodic recovery snapshots and restore the most recent one on startup.”

**1:50–2:40 — Power features**
- Use Find/Replace or Go To Line (quick showcase).
- Toggle line numbers and show they scroll in sync.
- Open a file and show “Open Recent” gets updated.

**2:40–3:10 — Wrap-up**
- “What I’m proud of: modular design (separate managers), graceful optional dependencies (PDF export/printing), and data-loss prevention.”
- “Thanks for watching—source and project report are in the repo and on the GitHub Pages site.”

