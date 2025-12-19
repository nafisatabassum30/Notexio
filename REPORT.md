# Project Report: Notexio Text Editor

## Challenge Description (STAR Format)

### Situation
The development of **Notexio**, a Python-based text editor, began with the goal of creating a lightweight yet feature-rich alternative to standard system editors. As the feature set expanded to include rich text formatting, file operations, view customization, and analysis tools, the codebase complexity increased significantly. Initially, handling all these operations within a single main application class led to code bloat, making navigation difficult and increasing the risk of regression bugs when modifying existing features.

### Task
The primary task was to restructure the application's architecture to support scalability and maintainability. I needed to decouple distinct functionalities—such as file handling, text editing, formatting, and UI components—into separate, specialized modules. The goal was to ensure that the main editor class served primarily as a coordinator, delegating specific tasks to these modules while maintaining a shared state (the text widget and application settings).

### Action
I implemented a modular architecture by creating a `src/` package with dedicated classes for each major functional area:

*   **`file_manager.py`**: Encapsulated all file I/O operations (Open, Save, Export), handling file paths and error states independently.
*   **`edit_operations.py`**: Isolated text manipulation logic like Undo, Redo, Cut, Copy, and Paste.
*   **`formatter.py`** & **`theme_manager.py`**: Managed visual styles, fonts, and application themes, allowing for dynamic updates without reloading the app.
*   **`tools.py`**: Offloaded analysis tasks (word count, statistics) to keep the core editing logic clean.

I refactored the main `Editor` class in `editor.py` to initialize these helper classes, passing the necessary references (like the main text widget or root window) to them. This required careful design of the dependency injection to avoid circular imports and ensure that modules could interact with the UI elements they needed to control.

### Result
The result is a highly maintainable and organized codebase. The modular design allowed for the seamless addition of advanced features, such as the "Safety Features" (auto-save/recovery) and "View Manager" (zoom/fullscreen), without disrupting the core editor logic. Debugging became significantly easier as issues could be traced to specific modules. The project now serves as a robust demonstration of object-oriented design principles in a practical GUI application, fulfilling the original goal of being an educational yet functional tool.
