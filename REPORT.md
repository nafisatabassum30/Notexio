# Notexio Project Report

## Project Introduction

Notexio is a lightweight, customizable, and user-friendly text editor built with Python and Tkinter. Designed to provide a modern editing experience similar to Windows Notepad but with enhanced capabilities, Notexio features a clean interface, dark/light mode theming, rich text formatting, and essential tools like word counting and reading time estimation. 

The project demonstrates practical application of operating system concepts including file I/O operations, event-driven GUI programming, and process management. Key features include robust file safety mechanisms (auto-save and recovery), drag-and-drop support, and a modular architecture that separates concerns between view management, file operations, and editing logic.

## Challenges Report (STAR Format)

### Challenge: Implementing Synchronized Line Numbers

**Situation (The Challenge)**  
The standard Tkinter `Text` widget provides a powerful interface for editing text but lacks built-in support for a line number margin. Users, especially those writing code or technical documents, found it difficult to reference specific parts of their document without visible line indicators. The challenge was to create a line number bar that looks native and stays perfectly synchronized with the text content.

**Task (The Objective)**  
The goal was to implement a toggleable line number column on the left side of the editor that:
1. Automatically updates when new lines are added or removed.
2. Scrolls in perfect synchronization with the main text area.
3. Maintains visual consistency with the current theme (light/dark mode).

**Action (The Solution)**  
To address this, I implemented a solution involving a composite UI component:
1.  **Dual-Widget Architecture**: I created a separate `Canvas` widget placed directly to the left of the main `ScrolledText` widget to serve as the line number bar.
2.  **Event Binding**: I bound specific events (`<KeyRelease>`, `<Return>`, and `<BackSpace>`) to a custom update function. This ensures that every time the user modifies the text, the line numbers are recalculated.
3.  **Scroll Synchronization**: I linked the Y-scroll command of the line number widget to the main text widget's yview, ensuring that scrolling one widget automatically scrolls the other.
4.  **Dynamic Redrawing**: I wrote an algorithm that calculates the number of lines in the text widget and draws corresponding numbers on the canvas, adjusting for font size and spacing to match the text editor exactly.

**Result (The Outcome)**  
The result is a seamless line number feature that users can toggle on or off. The line numbers update instantly as the user types and scroll smoothly alongside the document content. This feature significantly improved the editor's usability for coding and technical writing tasks, making navigation and referencing much more efficient.
