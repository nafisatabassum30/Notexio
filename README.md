# 📝 Notexio Text Editor

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![License](https://img.shields.io/badge/license-Educational-orange.svg)

**A Modern, Feature-Rich Text Editor Built with Python & Tkinter**

*Demonstrating Operating System Concepts Through Practical Application*

</div>

---

## 🎯 Project Overview

**Notexio** is a lightweight yet powerful text editor that brings the simplicity of Windows Notepad together with professional-grade features. Built entirely in Python using Tkinter, this project demonstrates practical implementation of core Operating System concepts including:

- **File I/O Operations** — Reading, writing, and managing files across platforms
- **Process Management** — Background threading for auto-save functionality
- **Memory Management** — Efficient handling of large text documents
- **Event-Driven Programming** — Responsive GUI with keyboard shortcuts
- **Cross-Platform Compatibility** — Works on Windows, Linux, and macOS

---

## ✨ Key Features

### 📁 Smart File Management
- **New/Open/Save/Save As** with modern file dialogs
- **Recent Files** tracking (up to 10 files)
- **Auto-detect unsaved changes** before closing
- **Default .txt extension** support

### ✏️ Powerful Editing
- **Undo/Redo** with unlimited history
- **Cut/Copy/Paste** with system clipboard integration
- **Find & Replace** with highlight functionality
- **Go to Line** for quick navigation
- **Select All / Clear All** operations

### 🎨 Rich Formatting
- **Font Family & Size** selection
- **Text & Background Color** customization
- **Bold, Italic, Underline** styling
- **One-click Default Restore**

### 👁️ View Options
- **Zoom In/Out/Reset** (Ctrl+Plus/Minus/0)
- **Word Wrap** toggle
- **Line Numbers** display
- **Fullscreen Mode** (F11)

### 🛠️ Built-in Tools
- **Word/Character/Line Count**
- **Document Statistics** panel
- **Reading Time Estimate**
- **Duplicate Word Highlighter**
- **Extra Space Remover**

### 🎭 Theme Customization
- **Light Mode** — Clean, modern white theme
- **Dark Mode** — Easy on the eyes for night coding
- **Custom Theme** — Choose your own colors

### 🛡️ Safety Features
- **Auto-save** (configurable interval)
- **Recovery Files** — Never lose your work
- **Exit Warning** for unsaved changes

### 📤 Export & Print
- **Print Preview** — See before you print
- **Print File** — Direct printing support
- **Export as PDF** — Share documents easily

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/notexio.git
cd notexio

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Optional Enhancements

```bash
# For drag & drop support on Windows
pip install tkinterdnd2

# For print functionality on Windows
pip install pywin32
```

---

## ⌨️ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New File | `Ctrl+N` |
| Open File | `Ctrl+O` |
| Save | `Ctrl+S` |
| Save As | `Ctrl+Shift+S` |
| Undo | `Ctrl+Z` |
| Redo | `Ctrl+Y` |
| Cut | `Ctrl+X` |
| Copy | `Ctrl+C` |
| Paste | `Ctrl+V` |
| Select All | `Ctrl+A` |
| Find | `Ctrl+F` |
| Replace | `Ctrl+H` |
| Go to Line | `Ctrl+G` |
| Bold | `Ctrl+B` |
| Italic | `Ctrl+I` |
| Underline | `Ctrl+U` |
| Zoom In | `Ctrl++` |
| Zoom Out | `Ctrl+-` |
| Reset Zoom | `Ctrl+0` |
| Fullscreen | `F11` |
| Print | `Ctrl+P` |

---

## 📁 Project Architecture

```
Notexio/
├── 📄 main.py                  # Application entry point & orchestrator
├── 📁 src/
│   ├── 📄 __init__.py          # Package initializer
│   ├── 📄 editor.py            # Main editor window class
│   ├── 📄 file_manager.py      # File operations (Open, Save, Recent)
│   ├── 📄 edit_operations.py   # Edit features (Undo, Find, Replace)
│   ├── 📄 formatter.py         # Text formatting (Font, Color, Style)
│   ├── 📄 view_manager.py      # View options (Zoom, Wrap, Fullscreen)
│   ├── 📄 tools.py             # Tools (Word Count, Statistics)
│   ├── 📄 theme_manager.py     # Theme management (Light, Dark, Custom)
│   ├── 📄 safety_features.py   # Auto-save & Recovery system
│   ├── 📄 ui_components.py     # Toolbar & Status bar components
│   ├── 📄 settings_manager.py  # User preferences storage
│   └── 📄 misc_features.py     # Print, PDF export, Drag & Drop
├── 📁 config/
│   └── 📄 settings.json        # User preferences file
├── 📁 recovery/                # Auto-save recovery files
├── 📄 requirements.txt         # Python dependencies
├── 📄 CHALLENGES_REPORT.md     # Development challenges (STAR format)
└── 📄 README.md                # This file
```

---

## 🎓 Skills Demonstrated

This project showcases proficiency in:

| Category | Skills |
|----------|--------|
| **Programming** | Python, Object-Oriented Design, Modular Architecture |
| **GUI Development** | Tkinter, Event-Driven Programming, Widget Management |
| **OS Concepts** | File I/O, Threading, Process Management, Memory Handling |
| **Software Design** | MVC Pattern, Dependency Injection, Clean Code Principles |
| **UX/UI** | Modern Interface Design, Accessibility, Responsive Layouts |
| **Version Control** | Git, GitHub, Collaborative Development |

---

## 📊 Technical Highlights

### Modular Design
The application is split into **11 specialized modules**, each handling a specific responsibility:
- Separation of concerns for maintainability
- Easy to extend with new features
- Testable components

### Thread-Safe Auto-Save
Background thread implementation ensures:
- No UI freezing during save operations
- Configurable save intervals
- Automatic cleanup of old recovery files

### Cross-Platform Support
- UTF-8 encoding for international character support
- Platform-agnostic file operations
- Adaptive UI styling

### Modern UI/UX
- Windows 11-inspired design language
- Intuitive toolbar and menu layout
- Real-time status bar updates

---

## 🔧 Configuration

Settings are automatically saved to `config/settings.json`:

```json
{
  "theme": "light",
  "recent_files": [],
  "window_width": 900,
  "window_height": 650,
  "font_family": "Segoe UI",
  "font_size": 11
}
```

---

## 📸 Screenshots

*The application features a clean, modern interface inspired by Windows 11 Notepad*

- **Light Mode**: Clean white background with blue accents
- **Dark Mode**: Dark grey background, easy on the eyes
- **Custom Theme**: Personalize with your favorite colors

---

## 🤝 Contributing

This project was created for educational purposes. Feel free to:
- Fork the repository
- Submit issues for bugs
- Create pull requests for improvements

---

## 📜 License

This project is created for educational purposes as part of an Operating Systems course.

---

## 👨‍💻 Author

Created with ❤️ as a demonstration of Operating System concepts through practical software development.

---

<div align="center">

**⭐ Star this repository if you found it helpful! ⭐**

</div>
