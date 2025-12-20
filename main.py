"""
Notexio Text Editor - Main Application Entry Point
A lightweight, customizable text editor built with Python and Tkinter.
"""
import tkinter as tk
from tkinter import messagebox
import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.editor import Editor
from src.file_manager import FileManager
from src.edit_operations import EditOperations
from src.formatter import Formatter
from src.view_manager import ViewManager
from src.tools import Tools
from src.theme_manager import ThemeManager
from src.safety_features import SafetyFeatures
from src.ui_components import UIComponents
from src.settings_manager import SettingsManager
from src.misc_features import MiscFeatures


class NotexioApp:
    """Main application class."""
    
    def __init__(self, root):
        self.root = root
        self.settings_manager = SettingsManager()
        
        # Set modern window styling
        root.configure(bg="#FFFFFF")
        
        # Initialize editor
        self.editor = Editor(root)
        
        # Initialize managers
        self.file_manager = FileManager(self.editor, self.settings_manager)
        # Set app reference for recent files menu updates
        self.file_manager.app = self
        
        # Set editor reference for UI components (circular reference)
        self.editor.ui_components = None  # Will be set below
        self.edit_operations = EditOperations(self.editor)
        self.formatter = Formatter(self.editor)
        self.view_manager = ViewManager(self.editor)
        # Set references for cross-module communication
        self.editor.view_manager = self.view_manager
        self.editor.formatter = self.formatter
        self.tools = Tools(self.editor)
        self.theme_manager = ThemeManager(self.editor, self.settings_manager)
        self.safety_features = SafetyFeatures(self.editor, self.file_manager)
        self.ui_components = UIComponents(self.editor)
        self.misc_features = MiscFeatures(self.editor, self.file_manager)
        
        # Connect app reference to UI components
        self.ui_components.app = self
        # Set UI components reference in editor for status bar updates
        self.editor.ui_components = self.ui_components
        
        # Setup UI
        self.setup_menu()
        self.ui_components.create_toolbar()
        self.ui_components.create_status_bar()
        
        # Connect toolbar commands
        self.connect_toolbar_commands()
        
        # Enable drag and drop
        self.misc_features.enable_drag_drop()
        
        # Load settings
        self.load_settings()
        
        # Check for recovery files
        self.check_recovery_files()
        
        # Bind keyboard shortcuts
        self.bind_shortcuts()
        
        # Bind mouse wheel to entire window
        self.root.bind_all("<MouseWheel>", self.on_window_mousewheel)
        self.root.bind_all("<Button-4>", self.on_window_mousewheel)
        self.root.bind_all("<Button-5>", self.on_window_mousewheel)
        
    def on_window_mousewheel(self, event):
        """Handle mouse wheel on entire window."""
        # Focus on text widget if mouse is over it
        widget = event.widget
        if hasattr(widget, 'winfo_class'):
            if widget.winfo_class() == 'Text' or 'text' in str(widget).lower():
                # Let the text widget handle it
                return
        # Otherwise, scroll the text widget
        if hasattr(self.editor, 'text_widget'):
            if hasattr(event, 'delta') and event.delta:
                self.editor.text_widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif hasattr(event, 'num'):
                if event.num == 4:
                    self.editor.text_widget.yview_scroll(-1, "units")
                elif event.num == 5:
                    self.editor.text_widget.yview_scroll(1, "units")
        
    def setup_menu(self):
        """Setup Windows Notepad-style menu bar."""
        menubar = tk.Menu(
            self.root,
            tearoff=0,
            bg="#FAFAFA",
            fg="#000000",
            activebackground="#0078D4",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 9),
            borderwidth=0
        )
        self.root.config(menu=menubar)
        
        # File menu - Windows Notepad style
        file_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg="#FFFFFF",
            fg="#000000",
            activebackground="#0078D4",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 9),
            borderwidth=0
        )
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.file_manager.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.file_manager.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.file_manager.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.file_manager.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        
        # Recent files submenu
        self.recent_menu = tk.Menu(
            file_menu,
            tearoff=0,
            bg="#FFFFFF",
            fg="#000000",
            activebackground="#0078D4",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 9),
            borderwidth=0
        )
        file_menu.add_cascade(label="Open Recent", menu=self.recent_menu)
        self.update_recent_files_menu(self.recent_menu)
        
        file_menu.add_separator()
        file_menu.add_command(label="Print Preview...", command=self.misc_features.print_preview)
        file_menu.add_command(label="Print...", command=self.misc_features.print_file, accelerator="Ctrl+P")
        file_menu.add_separator()
        file_menu.add_command(label="Export as PDF...", command=self.misc_features.export_as_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Edit menu
        edit_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg="#FFFFFF",
            fg="#000000",
            activebackground="#0078D4",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 9),
            borderwidth=0
        )
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.edit_operations.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.edit_operations.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.edit_operations.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.edit_operations.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.edit_operations.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.edit_operations.select_all, accelerator="Ctrl+A")
        edit_menu.add_command(label="Clear All", command=self.edit_operations.clear_all)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find...", command=self.edit_operations.find, accelerator="Ctrl+F")
        edit_menu.add_command(label="Replace...", command=self.edit_operations.replace, accelerator="Ctrl+H")
        edit_menu.add_command(label="Go to Line...", command=self.edit_operations.go_to_line, accelerator="Ctrl+G")
        
        # Format menu
        format_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg="#FFFFFF",
            fg="#000000",
            activebackground="#0078D4",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 9),
            borderwidth=0
        )
        menubar.add_cascade(label="Format", menu=format_menu)
        format_menu.add_command(label="Font Family...", command=self.formatter.change_font_family)
        format_menu.add_command(label="Font Size...", command=self.formatter.change_font_size)
        format_menu.add_separator()
        format_menu.add_command(label="Text Color...", command=self.formatter.change_text_color)
        format_menu.add_command(label="Background Color...", command=self.formatter.change_bg_color)
        format_menu.add_separator()
        format_menu.add_command(label="Bold", command=self.formatter.toggle_bold, accelerator="Ctrl+B")
        format_menu.add_command(label="Italic", command=self.formatter.toggle_italic, accelerator="Ctrl+I")
        format_menu.add_command(label="Underline", command=self.formatter.toggle_underline, accelerator="Ctrl+U")
        format_menu.add_separator()
        format_menu.add_command(label="Restore Default Formatting", command=self.formatter.restore_default_formatting)
        
        # View menu
        view_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg="#FFFFFF",
            fg="#000000",
            activebackground="#0078D4",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 9),
            borderwidth=0
        )
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self.view_manager.zoom_in, accelerator="Ctrl+Plus")
        view_menu.add_command(label="Zoom Out", command=self.view_manager.zoom_out, accelerator="Ctrl+Minus")
        view_menu.add_command(label="Reset Zoom", command=self.view_manager.reset_zoom, accelerator="Ctrl+0")
        view_menu.add_separator()
        view_menu.add_command(label="Word Wrap", command=self.view_manager.toggle_word_wrap)
        view_menu.add_command(label="Line Numbers", command=self.toggle_line_numbers)
        view_menu.add_command(label="Fullscreen", command=self.view_manager.toggle_fullscreen, accelerator="F11")
        
        # Tools menu
        tools_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg="#FFFFFF",
            fg="#000000",
            activebackground="#0078D4",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 9),
            borderwidth=0
        )
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Word Count", command=lambda: messagebox.showinfo("Word Count", f"Words: {self.tools.get_word_count():,}"))
        tools_menu.add_command(label="Character Count", command=lambda: messagebox.showinfo("Character Count", f"Characters: {self.tools.get_character_count():,}"))
        tools_menu.add_command(label="Line Count", command=lambda: messagebox.showinfo("Line Count", f"Lines: {self.tools.get_line_count():,}"))
        tools_menu.add_command(label="Document Statistics", command=self.tools.show_statistics)
        tools_menu.add_separator()
        tools_menu.add_command(label="Reading Time Estimate", command=lambda: messagebox.showinfo("Reading Time", f"Estimated reading time: {self.tools.get_reading_time()}"))
        tools_menu.add_command(label="Highlight Duplicate Words", command=self.tools.highlight_duplicate_words)
        tools_menu.add_command(label="Remove Extra Spaces", command=self.tools.remove_extra_spaces)
        
        # Theme menu
        theme_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg="#FFFFFF",
            fg="#000000",
            activebackground="#0078D4",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 9),
            borderwidth=0
        )
        menubar.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_command(label="Light Mode", command=self.theme_manager.set_light_mode)
        theme_menu.add_command(label="Dark Mode", command=self.theme_manager.set_dark_mode)
        theme_menu.add_command(label="Customize Theme...", command=self.theme_manager.customize_theme)
        
        # Help menu
        help_menu = tk.Menu(
            menubar,
            tearoff=0,
            bg="#FFFFFF",
            fg="#000000",
            activebackground="#0078D4",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 9),
            borderwidth=0
        )
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def update_recent_files_menu(self, recent_menu):
        """Update recent files menu."""
        recent_files = self.file_manager.get_recent_files()
        recent_menu.delete(0, tk.END)
        
        if recent_files:
            for filepath in recent_files:
                filename = os.path.basename(filepath)
                recent_menu.add_command(
                    label=filename,
                    command=lambda fp=filepath: self.file_manager.open_file(fp)
                )
        else:
            recent_menu.add_command(label="No recent files", state=tk.DISABLED)
            
    def connect_toolbar_commands(self):
        """Connect toolbar buttons to commands."""
        # Toolbar commands are connected via UIComponents._toolbar_command
        # which references self.app, so they're already connected
        pass
        
    def load_settings(self):
        """Load application settings."""
        # Load theme
        self.theme_manager.load_theme()
        
        # Load recent files
        self.file_manager.load_recent_files()
        
        # Load window size
        width = self.settings_manager.get_setting("window_width", 800)
        height = self.settings_manager.get_setting("window_height", 600)
        self.root.geometry(f"{width}x{height}")

        # Load auto-save preference
        if self.settings_manager.get_setting("auto_save", False):
            interval = self.settings_manager.get_setting("auto_save_interval", 300)
            try:
                self.safety_features.enable_auto_save(interval=interval)
            except Exception:
                # Auto-save is a convenience feature; don't block startup
                pass
        
    def check_recovery_files(self):
        """Check for recovery files on startup."""
        recovery_files = self.safety_features.check_recovery_files()
        if recovery_files:
            response = messagebox.askyesno(
                "Recovery Files Found",
                f"Found {len(recovery_files)} recovery file(s).\nDo you want to restore the most recent one?",
                icon=messagebox.QUESTION
            )
            if response:
                self.safety_features.restore_recovery_file(recovery_files[0][0])
                
    def bind_shortcuts(self):
        """Bind keyboard shortcuts."""
        # File shortcuts
        self.root.bind("<Control-n>", lambda e: self.file_manager.new_file())
        self.root.bind("<Control-o>", lambda e: self.file_manager.open_file())
        self.root.bind("<Control-s>", lambda e: self.file_manager.save_file())
        self.root.bind("<Control-S>", lambda e: self.file_manager.save_as_file())  # Ctrl+Shift+S
        
        # Edit shortcuts
        self.root.bind("<Control-z>", lambda e: self.edit_operations.undo())
        self.root.bind("<Control-y>", lambda e: self.edit_operations.redo())
        self.root.bind("<Control-x>", lambda e: self.edit_operations.cut())
        self.root.bind("<Control-c>", lambda e: self.edit_operations.copy())
        self.root.bind("<Control-v>", lambda e: self.edit_operations.paste())
        self.root.bind("<Control-a>", lambda e: self.edit_operations.select_all())
        self.root.bind("<Control-f>", lambda e: self.edit_operations.find())
        self.root.bind("<Control-h>", lambda e: self.edit_operations.replace())
        self.root.bind("<Control-g>", lambda e: self.edit_operations.go_to_line())
        
        # Format shortcuts
        self.root.bind("<Control-b>", lambda e: self.formatter.toggle_bold())
        self.root.bind("<Control-i>", lambda e: self.formatter.toggle_italic())
        self.root.bind("<Control-u>", lambda e: self.formatter.toggle_underline())
        
        # View shortcuts
        self.root.bind("<F11>", lambda e: self.view_manager.toggle_fullscreen())
        self.root.bind("<Control-plus>", lambda e: self.view_manager.zoom_in())
        self.root.bind("<Control-equal>", lambda e: self.view_manager.zoom_in())  # Ctrl+= is same as Ctrl++
        self.root.bind("<Control-minus>", lambda e: self.view_manager.zoom_out())
        self.root.bind("<Control-0>", lambda e: self.view_manager.reset_zoom())
        
        # Print shortcut
        self.root.bind("<Control-p>", lambda e: self.misc_features.print_file())
        
    def toggle_line_numbers(self):
        """Toggle line numbers display."""
        self.ui_components.toggle_line_numbers()
        self.view_manager.line_numbers_visible = self.ui_components.line_numbers_visible
        
    def on_closing(self):
        """Handle application closing."""
        if self.safety_features.warn_on_exit():
            # Stop auto-save scheduling
            try:
                self.safety_features.disable_auto_save()
            except Exception:
                pass

            # Save window size
            self.settings_manager.set_setting("window_width", self.root.winfo_width())
            self.settings_manager.set_setting("window_height", self.root.winfo_height())
            self.settings_manager.save_settings()
            
            # Create final recovery file
            if self.editor.is_modified:
                self.safety_features.create_recovery_file()
                
            self.root.destroy()
            
    def show_about(self):
        """Show about dialog."""
        about_text = """Notexio Text Editor
Version 1.0.0

A lightweight, customizable text editor
built with Python and Tkinter.

© 2025"""
        messagebox.showinfo("About Notexio", about_text)


def main():
    """Main entry point."""
    root = tk.Tk()
    app = NotexioApp(root)
    
    # Override window close protocol
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    root.mainloop()


if __name__ == "__main__":
    main()

