"""
Main editor window class for Notexio text editor.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import os


class Editor:
    """Main editor window class."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Notexio - Untitled")
        self.root.geometry("900x650")
        # Modern Windows 11 Notepad style - clean white background
        self.root.configure(bg="#FFFFFF")
        # Remove window border for cleaner look (optional)
        try:
            self.root.attributes("-toolwindow", False)
        except:
            pass
        
        # Current file path
        self.current_file = None
        self.is_modified = False
        
        # UI components reference (will be set by main app)
        self.ui_components = None
        
        # Initialize UI components
        self.setup_ui()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_ui(self):
        """Setup the user interface."""
        # Menu bar will be added by main.py
        # Create container frame for text widget (allows line numbers to be added later)
        self.text_container = tk.Frame(self.root)
        self.text_container.pack(fill=tk.BOTH, expand=True)
        
        # Modern Windows Notepad-style text widget - clean and minimal
        self.text_widget = scrolledtext.ScrolledText(
            self.text_container,
            wrap=tk.WORD,
            undo=True,
            font=("Segoe UI", 11),  # Modern Windows 11 font
            bg="#FFFFFF",
            fg="#000000",
            selectbackground="#0078D4",  # Windows blue selection
            selectforeground="#FFFFFF",
            insertbackground="#000000",
            borderwidth=0,
            highlightthickness=0,
            padx=15,
            pady=15,
            spacing1=0,  # Tight line spacing like Notepad
            spacing2=0,
            spacing3=0,
            relief=tk.FLAT
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Track modifications
        self.text_widget.bind("<<Modified>>", self.on_text_modified)
        
    def on_text_modified(self, event=None):
        """Handle text modification events."""
        if self.text_widget.edit_modified():
            self.is_modified = True
            self.update_title()
            self.text_widget.edit_modified(False)
            # Update status bar if available
            if self.ui_components and hasattr(self.ui_components, 'update_status_bar'):
                self.ui_components.update_status_bar()
            # Update line numbers if visible
            if self.ui_components and hasattr(self.ui_components, 'line_numbers_visible'):
                if self.ui_components.line_numbers_visible:
                    self.ui_components.update_line_numbers()
            
    def update_title(self):
        """Update window title with filename and unsaved indicator."""
        if self.current_file:
            filename = os.path.basename(self.current_file)
            title = f"Notexio - {filename}"
        else:
            title = "Notexio - Untitled"
            
        if self.is_modified:
            title += " *"
            
        self.root.title(title)
        
    def on_closing(self):
        """Handle window closing event."""
        # Will be enhanced with unsaved changes check
        self.root.destroy()

