"""
Edit operations for Notexio text editor.
"""
import tkinter as tk
from tkinter import simpledialog, messagebox
import re


class EditOperations:
    """Manages edit operations."""
    
    def __init__(self, editor):
        self.editor = editor
        self.search_dialog = None
        self.replace_dialog = None
        self.search_entry = None
        self.replace_entry = None
        self.search_case_sensitive = False
        
    def undo(self):
        """Undo last action."""
        try:
            self.editor.text_widget.edit_undo()
        except tk.TclError:
            pass
            
    def redo(self):
        """Redo last undone action."""
        try:
            self.editor.text_widget.edit_redo()
        except tk.TclError:
            pass
            
    def cut(self):
        """Cut selected text."""
        try:
            self.editor.text_widget.event_generate("<<Cut>>")
        except tk.TclError:
            pass
            
    def copy(self):
        """Copy selected text."""
        try:
            self.editor.text_widget.event_generate("<<Copy>>")
        except tk.TclError:
            pass
            
    def paste(self):
        """Paste text from clipboard."""
        try:
            self.editor.text_widget.event_generate("<<Paste>>")
        except tk.TclError:
            pass
            
    def select_all(self):
        """Select all text."""
        self.editor.text_widget.tag_add(tk.SEL, "1.0", tk.END)
        self.editor.text_widget.mark_set(tk.INSERT, "1.0")
        self.editor.text_widget.see(tk.INSERT)
        
    def clear_all(self):
        """Clear all text."""
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all text?"):
            self.editor.text_widget.delete(1.0, tk.END)
            
    def find(self):
        """Open find dialog."""
        if self.search_dialog is None or not self.search_dialog.winfo_exists():
            self.create_search_dialog()
        else:
            self.search_dialog.lift()
            
    def create_search_dialog(self):
        """Create search dialog window."""
        self.search_dialog = tk.Toplevel(self.editor.root)
        self.search_dialog.title("Find")
        self.search_dialog.geometry("400x150")
        self.search_dialog.transient(self.editor.root)
        
        # Search entry
        tk.Label(self.search_dialog, text="Find:").pack(pady=5)
        self.search_entry = tk.Entry(self.search_dialog, width=40)
        self.search_entry.pack(pady=5)
        self.search_entry.focus()
        
        # Case sensitive checkbox
        self.case_var = tk.BooleanVar()
        tk.Checkbutton(
            self.search_dialog,
            text="Case sensitive",
            variable=self.case_var
        ).pack()
        
        # Buttons
        button_frame = tk.Frame(self.search_dialog)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Find Next",
            command=self.find_next
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Find Previous",
            command=self.find_previous
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Close",
            command=self.search_dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        self.search_entry.bind("<Return>", lambda e: self.find_next())
        
    def find_next(self):
        """Find next occurrence."""
        if not self.search_entry:
            return
            
        search_term = self.search_entry.get()
        if not search_term:
            return
            
        self.search_case_sensitive = self.case_var.get()
        
        # Get current cursor position
        start_pos = self.editor.text_widget.index(tk.INSERT)
        
        # Search from cursor position
        content = self.editor.text_widget.get(start_pos, tk.END)
        
        if not self.search_case_sensitive:
            search_term_lower = search_term.lower()
            content_lower = content.lower()
            idx = content_lower.find(search_term_lower)
        else:
            idx = content.find(search_term)
            
        if idx != -1:
            # Calculate absolute position
            start_line, start_col = map(int, start_pos.split('.'))
            lines = content[:idx].split('\n')
            line_offset = len(lines) - 1
            col_offset = len(lines[-1]) if lines else 0
            
            if line_offset == 0:
                end_pos = f"{start_line}.{start_col + idx + len(search_term)}"
                start_pos = f"{start_line}.{start_col + idx}"
            else:
                start_pos = f"{start_line + line_offset}.{col_offset}"
                end_pos = f"{start_line + line_offset}.{col_offset + len(search_term)}"
                
            # Select found text
            self.editor.text_widget.tag_remove(tk.SEL, 1.0, tk.END)
            self.editor.text_widget.tag_add(tk.SEL, start_pos, end_pos)
            self.editor.text_widget.mark_set(tk.INSERT, end_pos)
            self.editor.text_widget.see(tk.INSERT)
        else:
            messagebox.showinfo("Find", "No more occurrences found.")
            
    def find_previous(self):
        """Find previous occurrence."""
        if not self.search_entry:
            return
            
        search_term = self.search_entry.get()
        if not search_term:
            return
            
        self.search_case_sensitive = self.case_var.get()
        
        # Get current cursor position
        end_pos = self.editor.text_widget.index(tk.INSERT)
        
        # Search backwards from cursor position
        content = self.editor.text_widget.get(1.0, end_pos)
        
        if not self.search_case_sensitive:
            search_term_lower = search_term.lower()
            content_lower = content.lower()
            idx = content_lower.rfind(search_term_lower)
        else:
            idx = content.rfind(search_term)
            
        if idx != -1:
            # Calculate absolute position
            lines = content[:idx].split('\n')
            line_num = len(lines)
            col_num = len(lines[-1]) if lines else idx
            
            start_pos = f"{line_num}.{col_num}"
            end_pos = f"{line_num}.{col_num + len(search_term)}"
            
            # Select found text
            self.editor.text_widget.tag_remove(tk.SEL, 1.0, tk.END)
            self.editor.text_widget.tag_add(tk.SEL, start_pos, end_pos)
            self.editor.text_widget.mark_set(tk.INSERT, start_pos)
            self.editor.text_widget.see(tk.INSERT)
        else:
            messagebox.showinfo("Find", "No more occurrences found.")
            
    def replace(self):
        """Open replace dialog."""
        if self.replace_dialog is None or not self.replace_dialog.winfo_exists():
            self.create_replace_dialog()
        else:
            self.replace_dialog.lift()
            
    def create_replace_dialog(self):
        """Create replace dialog window."""
        self.replace_dialog = tk.Toplevel(self.editor.root)
        self.replace_dialog.title("Find and Replace")
        self.replace_dialog.geometry("400x200")
        self.replace_dialog.transient(self.editor.root)
        
        # Find entry
        tk.Label(self.replace_dialog, text="Find:").pack(pady=5)
        self.search_entry = tk.Entry(self.replace_dialog, width=40)
        self.search_entry.pack(pady=5)
        
        # Replace entry
        tk.Label(self.replace_dialog, text="Replace with:").pack(pady=5)
        self.replace_entry = tk.Entry(self.replace_dialog, width=40)
        self.replace_entry.pack(pady=5)
        
        # Case sensitive checkbox
        self.case_var = tk.BooleanVar()
        tk.Checkbutton(
            self.replace_dialog,
            text="Case sensitive",
            variable=self.case_var
        ).pack()
        
        # Buttons
        button_frame = tk.Frame(self.replace_dialog)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Find Next",
            command=self.find_next
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Replace",
            command=self.replace_one
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Replace All",
            command=self.replace_all
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Close",
            command=self.replace_dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
        
    def replace_one(self):
        """Replace current selection."""
        if not self.replace_entry:
            return
            
        try:
            sel_start = self.editor.text_widget.index(tk.SEL_FIRST)
            sel_end = self.editor.text_widget.index(tk.SEL_LAST)
            replace_text = self.replace_entry.get()
            self.editor.text_widget.delete(sel_start, sel_end)
            self.editor.text_widget.insert(sel_start, replace_text)
            self.find_next()
        except tk.TclError:
            self.find_next()
            
    def replace_all(self):
        """Replace all occurrences."""
        if not self.search_entry or not self.replace_entry:
            return
            
        search_term = self.search_entry.get()
        replace_term = self.replace_entry.get()
        
        if not search_term:
            return
            
        self.search_case_sensitive = self.case_var.get()
        
        # Get all content
        content = self.editor.text_widget.get(1.0, tk.END)
        
        if not self.search_case_sensitive:
            # Case-insensitive replace
            content_new = re.sub(
                re.escape(search_term),
                replace_term,
                content,
                flags=re.IGNORECASE
            )
        else:
            # Case-sensitive replace
            content_new = content.replace(search_term, replace_term)
            
        if content_new != content:
            self.editor.text_widget.delete(1.0, tk.END)
            self.editor.text_widget.insert(1.0, content_new)
            messagebox.showinfo("Replace", "Replace completed.")
        else:
            messagebox.showinfo("Replace", "No occurrences found.")
            
    def go_to_line(self):
        """Go to specific line number."""
        line_str = simpledialog.askstring(
            "Go to Line",
            "Enter line number:",
            parent=self.editor.root
        )
        
        if line_str:
            try:
                line_num = int(line_str)
                if line_num < 1:
                    messagebox.showerror("Error", "Line number must be greater than 0.")
                    return
                    
                # Get total lines
                total_lines = int(self.editor.text_widget.index(tk.END).split('.')[0]) - 1
                if line_num > total_lines:
                    messagebox.showerror("Error", f"Line number exceeds total lines ({total_lines}).")
                    return
                    
                # Go to line
                pos = f"{line_num}.0"
                self.editor.text_widget.mark_set(tk.INSERT, pos)
                self.editor.text_widget.see(pos)
                self.editor.text_widget.focus()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid line number.")

