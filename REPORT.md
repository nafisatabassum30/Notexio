# Project Report: Notexio Text Editor

## Challenges Faced (STAR Format)

### Challenge 1: Implementing a Robust Undo/Redo System

*   **Situation:** The standard text editing experience requires a reliable way to revert mistakes. However, directly managing the state of text changes can be complex and error-prone, potentially leading to application crashes if the undo stack is empty or corrupted.
*   **Task:** Implement a stable Undo (Ctrl+Z) and Redo (Ctrl+Y) feature that mimics standard text editor behavior and handles edge cases gracefully.
*   **Action:** I leveraged the native `undo=True` capability of the Tkinter Text widget but enhanced it by wrapping the `edit_undo()` and `edit_redo()` calls in `try...except` blocks to catch `tk.TclError`. This ensures that attempting to undo when the stack is empty doesn't crash the program. I also mapped these actions to standard keyboard shortcuts.
*   **Result:** The application now supports seamless undo/redo operations with error protection, providing a frustration-free editing experience for users.

### Challenge 2: Advanced Search and Replace Functionality

*   **Situation:** Users often need to find specific text or replace multiple occurrences. Implementing this requires handling text selection, cursor positioning, and different search modes (case-sensitive vs. insensitive) which involves complex coordinate math (line.column).
*   **Task:** Create a "Find and Replace" dialog that allows users to search for text, highlight matches, and perform single or bulk replacements.
*   **Action:** I implemented a custom `EditOperations` class with `find_next`, `find_previous`, and `replace_all` methods. I used Python's `re` module for powerful pattern matching (especially for "Replace All") and Tkinter's tagging system (`tag_add`, `tag_remove`) to visually highlight search results. I also wrote logic to convert between absolute string indices and Tkinter's "line.column" coordinate system.
*   **Result:** A fully functional Find/Replace system that supports "Find Next", "Find Previous", and "Replace All" with optional case sensitivity, significantly enhancing the editor's utility.

### Challenge 3: Real-time Data Visualization (Document Statistics)

*   **Situation:** Users writing essays or code need to track their progress (word count, line count) without disrupting their workflow. Calculating these metrics accurately for large texts can be slow if not optimized.
*   **Task:** Provide a suite of tools to calculate and display document statistics and reading time estimates.
*   **Action:** I developed a dedicated `Tools` module. Instead of complex parsing, I utilized Python's efficient string `split()` and `len()` methods to calculate word and character counts. I also added a "Reading Time" estimator based on an average reading speed of 225 words per minute, converting the result into a human-readable format (minutes/seconds).
*   **Result:** A "Tools" menu that offers instant insights into the document, including a "Highlight Duplicate Words" feature that helps users improve their writing quality.

---

## Github Page Submission Details

### Project Introduction
**Notexio** is a modern, lightweight, and customizable text editor built with Python and Tkinter. Designed to be both an educational resource and a practical tool, Notexio demonstrates the power of Python for GUI development. It features a clean interface, robust file management (including auto-save and recovery), and a suite of writing tools like word count and reading time estimation. Whether you're coding or writing prose, Notexio provides a distraction-free environment with essential features like "Dark Mode", "Find/Replace", and "PDF Export".

### Key Features
*   **Smart Editing:** Undo/Redo, Cut/Copy/Paste, and Find/Replace.
*   **Format Control:** Customizable fonts, colors, and text styles (Bold/Italic/Underline).
*   **Safety First:** Auto-save recovery system to prevent data loss.
*   **Developer Friendly:** Line numbers, syntax-highlighting-ready structure.
*   **Cross-Platform:** Runs on Windows, Linux, and macOS.
