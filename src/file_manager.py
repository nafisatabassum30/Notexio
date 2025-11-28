"""
File operations manager for Notexio text editor.
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json


class FileManager:
    """Manages file operations."""
    
    def __init__(self, editor, settings_manager):
        self.editor = editor
        self.settings_manager = settings_manager
        self.recent_files = []
        self.max_recent_files = 10
        
    def new_file(self):
        """Create a new file."""
        if self.check_unsaved_changes():
            self.editor.current_file = None
            self.editor.text_widget.delete(1.0, tk.END)
            self.editor.is_modified = False
            self.editor.update_title()
            # Update status bar if available
            if hasattr(self.editor, 'ui_components') and self.editor.ui_components:
                if hasattr(self.editor.ui_components, 'update_status_bar'):
                    self.editor.ui_components.update_status_bar()
            
    def open_file(self, filepath=None):
        """Open a file."""
        if self.check_unsaved_changes():
            if not filepath:
                filepath = filedialog.askopenfilename(
                    title="Open File",
                    filetypes=[
                        ("Text Files", "*.txt"),
                        ("All Files", "*.*")
                    ]
                )
                
            if filepath:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    self.editor.text_widget.delete(1.0, tk.END)
                    self.editor.text_widget.insert(1.0, content)
                    self.editor.current_file = filepath
                    self.editor.is_modified = False
                    self.editor.update_title()
                    self.add_to_recent_files(filepath)
                    # Update status bar if available
                    if hasattr(self.editor, 'ui_components') and self.editor.ui_components:
                        if hasattr(self.editor.ui_components, 'update_status_bar'):
                            self.editor.ui_components.update_status_bar()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open file:\n{str(e)}")
                    
    def save_file(self):
        """Save current file."""
        if self.editor.current_file:
            try:
                with open(self.editor.current_file, 'w', encoding='utf-8') as f:
                    content = self.editor.text_widget.get(1.0, tk.END + "-1c")
                    f.write(content)
                self.editor.is_modified = False
                self.editor.update_title()
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
                return False
        else:
            return self.save_as_file()
            
    def save_as_file(self):
        """Save file with a new name."""
        filepath = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    content = self.editor.text_widget.get(1.0, tk.END + "-1c")
                    f.write(content)
                self.editor.current_file = filepath
                self.editor.is_modified = False
                self.editor.update_title()
                self.add_to_recent_files(filepath)
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
                return False
        return False
        
    def check_unsaved_changes(self):
        """Check for unsaved changes and prompt user."""
        if self.editor.is_modified:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save them?",
                icon=messagebox.WARNING
            )
            if response is None:  # Cancel
                return False
            elif response:  # Yes
                return self.save_file()
            else:  # No
                return True
        return True
        
    def add_to_recent_files(self, filepath):
        """Add file to recent files list."""
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)
        self.recent_files.insert(0, filepath)
        self.recent_files = self.recent_files[:self.max_recent_files]
        self.settings_manager.save_recent_files(self.recent_files)
        # Update recent files menu if app reference is available
        if hasattr(self, 'app') and self.app:
            if hasattr(self.app, 'recent_menu'):
                self.app.update_recent_files_menu(self.app.recent_menu)
        
    def get_recent_files(self):
        """Get list of recent files."""
        return self.recent_files
        
    def load_recent_files(self):
        """Load recent files from settings."""
        self.recent_files = self.settings_manager.load_recent_files()

