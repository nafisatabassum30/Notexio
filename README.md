# Notexio Text Editor

Notexio is a lightweight, customizable and user-friendly text editor built with Python and Tkinter. It is designed as an OS-based project to demonstrate practical concepts of file I/O, GUI development, event-driven programming and basic operating system interactions.

## Features

### File Operations
- New File (Ctrl+N)
- Open File (Ctrl+O)
- Save (Ctrl+S)
- Save As (Ctrl+Shift+S)
- Open Recent Files
- Auto-detect unsaved changes before closing
- Default .txt extension support

### Edit Operations
- Undo/Redo (Ctrl+Z / Ctrl+Y)
- Cut/Copy/Paste (Ctrl+X / Ctrl+C / Ctrl+V)
- Select All (Ctrl+A)
- Clear All
- Find (Ctrl+F)
- Replace (Ctrl+H)
- Go to Line (Ctrl+G)

### Formatting
- Font Family selection
- Font Size adjustment
- Text Color
- Background Color
- Bold/Italic/Underline (Ctrl+B / Ctrl+I / Ctrl+U)
- Restore Default Formatting

### View Options
- Zoom In/Out/Reset (Ctrl+Plus / Ctrl+Minus / Ctrl+0)
- Word Wrap toggle
- Line Numbers
- Fullscreen (F11)

### Tools
- Word Count
- Character Count (with/without spaces)
- Line Count
- Document Statistics
- Reading Time Estimate
- Highlight Duplicate Words
- Remove Extra Spaces

### UI Components
- Toolbar with common actions
- Status Bar (shows line, column, word count, file status)
- Window title updates with filename and unsaved indicator (*)

### Theme Customization
- Light Mode
- Dark Mode
- Custom Theme Colors

### File Safety Features
- Auto-save (optional)
- Recovery file creation
- Warn on exit if unsaved changes exist

### Miscellaneous Features
- Drag & Drop file opening (Windows with tkinterdnd2)
- Print Preview
- Print File (Ctrl+P)
- Export as PDF

## Installation

1. Clone or download this repository

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) For enhanced drag & drop on Windows:
```bash
pip install tkinterdnd2
```

4. (Optional) For print functionality on Windows:
```bash
pip install pywin32
```

## Usage

Run the application:
```bash
python main.py
```

## STAR Report + GitHub Pages Submission

This repo includes a ready-to-publish GitHub Pages site with:
- a **STAR-formatted report** (Situation / Task / Action / Result)
- a **2–5 minute demo script** you can record against

### Publish the report on GitHub Pages

1. In GitHub: **Settings → Pages**
2. Under **Build and deployment**, choose **Deploy from a branch**
3. Select your default branch (often `main`)
4. Select folder: **`/docs`**
5. Save, wait for the site to publish, then submit the Pages URL.

The site content is in `docs/index.html`.

## Keyboard Shortcuts

- **Ctrl+N**: New File
- **Ctrl+O**: Open File
- **Ctrl+S**: Save
- **Ctrl+Shift+S**: Save As
- **Ctrl+Z**: Undo
- **Ctrl+Y**: Redo
- **Ctrl+X**: Cut
- **Ctrl+C**: Copy
- **Ctrl+V**: Paste
- **Ctrl+A**: Select All
- **Ctrl+F**: Find
- **Ctrl+H**: Replace
- **Ctrl+G**: Go to Line
- **Ctrl+B**: Bold
- **Ctrl+I**: Italic
- **Ctrl+U**: Underline
- **Ctrl+Plus**: Zoom In
- **Ctrl+Minus**: Zoom Out
- **Ctrl+0**: Reset Zoom
- **F11**: Toggle Fullscreen
- **Ctrl+P**: Print

## Project Structure

```
Notexio/
├── main.py                 # Main application entry point
├── src/
│   ├── __init__.py
│   ├── editor.py          # Main editor window class
│   ├── file_manager.py    # File operations
│   ├── edit_operations.py # Edit features
│   ├── formatter.py       # Formatting options
│   ├── view_manager.py    # View options
│   ├── tools.py           # Tools and statistics
│   ├── theme_manager.py   # Theme management
│   ├── safety_features.py # Safety features
│   ├── ui_components.py   # UI components
│   ├── settings_manager.py # Settings management
│   └── misc_features.py   # Miscellaneous features
├── config/
│   └── settings.json      # User preferences
├── recovery/              # Auto-save and recovery files
├── requirements.txt       # Dependencies
└── README.md
```

## Configuration

Settings are stored in `config/settings.json` and include:
- Theme preference
- Recent files list
- Window size
- Font settings
- View preferences

## License

This project is created for educational purposes.

## Version

Version 1.0.0
