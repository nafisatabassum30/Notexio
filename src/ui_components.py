"""
UI components for Notexio text editor.
"""
import tkinter as tk
from tkinter import ttk
import os


class UIComponents:
    """Manages UI components like toolbar, status bar, and tabs."""
    
    def __init__(self, editor):
        self.editor = editor
        self.toolbar_frame = None
        self.status_bar = None
        self.notebook = None
        self.tabs = {}  # Dictionary to track open tabs
        self.line_numbers = None
        self.line_numbers_visible = False
        self.app = None  # Will be set by main app
        
    def create_toolbar(self):
        """Create Windows Notepad-style minimal toolbar."""
        # Clean, minimal toolbar matching Windows Notepad
        self.toolbar_frame = tk.Frame(
            self.editor.root,
            bg="#FAFAFA",
            height=40,
            relief=tk.FLAT
        )
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X, padx=0, pady=0)
        self.toolbar_frame.pack_propagate(False)
        
        # Subtle bottom border for separation
        border = tk.Frame(self.toolbar_frame, height=1, bg="#E1E1E1")
        border.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Inner frame with proper spacing
        inner_frame = tk.Frame(self.toolbar_frame, bg="#FAFAFA")
        inner_frame.pack(side=tk.LEFT, padx=8, pady=6)
        
        # Clean toolbar buttons - Windows Notepad style
        buttons = [
            ("New", "new_file"),
            ("Open", "open_file"),
            ("Save", "save_file"),
            ("", None),  # Separator
            ("Cut", "cut"),
            ("Copy", "copy"),
            ("Paste", "paste"),
            ("", None),  # Separator
            ("Undo", "undo"),
            ("Redo", "redo"),
        ]
        
        for text, command in buttons:
            if text == "":
                # Clean separator
                sep = tk.Frame(inner_frame, width=1, bg="#D0D0D0", height=20)
                sep.pack(side=tk.LEFT, padx=4, pady=2, fill=tk.Y)
            else:
                # Windows Notepad-style button
                btn = tk.Button(
                    inner_frame,
                    text=text,
                    width=10,
                    height=1,
                    command=lambda cmd=command: self._toolbar_command(cmd) if cmd else None,
                    bg="#FAFAFA",
                    fg="#000000",
                    activebackground="#E8E8E8",
                    activeforeground="#000000",
                    relief=tk.FLAT,
                    borderwidth=0,
                    padx=12,
                    pady=4,
                    font=("Segoe UI", 9),
                    cursor="hand2"
                )
                btn.pack(side=tk.LEFT, padx=1, pady=0)
                
                # Smooth hover effect
                def on_enter(e, b=btn):
                    if b.cget("state") != tk.DISABLED:
                        b.config(bg="#E8E8E8")
                        
                def on_leave(e, b=btn):
                    if b.cget("state") != tk.DISABLED:
                        b.config(bg="#FAFAFA")
                        
                btn.bind("<Enter>", on_enter)
                btn.bind("<Leave>", on_leave)
                
    def _toolbar_command(self, command):
        """Handle toolbar button commands."""
        # This will be connected to editor methods via app reference
        if hasattr(self, 'app'):
            if command == "new_file":
                self.app.file_manager.new_file()
            elif command == "open_file":
                self.app.file_manager.open_file()
            elif command == "save_file":
                self.app.file_manager.save_file()
            elif command == "cut":
                self.app.edit_operations.cut()
            elif command == "copy":
                self.app.edit_operations.copy()
            elif command == "paste":
                self.app.edit_operations.paste()
            elif command == "undo":
                self.app.edit_operations.undo()
            elif command == "redo":
                self.app.edit_operations.redo()
        
    def create_status_bar(self):
        """Create Windows Notepad-style status bar."""
        # Clean, minimal status bar - Windows Notepad style
        self.status_bar = tk.Frame(
            self.editor.root,
            bg="#F0F0F0",
            height=22,
            relief=tk.FLAT
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
        self.status_bar.pack_propagate(False)
        
        # Top border - will be themed
        self.status_border = tk.Frame(self.status_bar, height=1, bg="#D0D0D0")
        self.status_border.pack(side=tk.TOP, fill=tk.X)
        
        # Content frame
        content_frame = tk.Frame(self.status_bar, bg="#F0F0F0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Left side - file status
        self.status_text = tk.Label(
            content_frame,
            text="Ready",
            anchor=tk.W,
            padx=10,
            pady=2,
            bg="#F0F0F0",
            fg="#000000",
            font=("Segoe UI", 9)
        )
        self.status_text.pack(side=tk.LEFT)
        
        # Right side - position and stats (like modern Notepad)
        right_frame = tk.Frame(content_frame, bg="#F0F0F0")
        right_frame.pack(side=tk.RIGHT)
        
        # Encoding (like Notepad) - UTF-8
        self.encoding_label = tk.Label(
            right_frame,
            text="UTF-8",
            anchor=tk.E,
            padx=8,
            pady=2,
            bg="#F0F0F0",
            fg="#000000",
            font=("Segoe UI", 9)
        )
        self.encoding_label.pack(side=tk.RIGHT)
        
        # Separator
        sep3 = tk.Frame(right_frame, width=1, bg="#D0D0D0", height=14)
        sep3.pack(side=tk.RIGHT, padx=4, pady=4, fill=tk.Y)
        
        # Line endings (like Notepad) - Windows (CRLF)
        self.line_ending_label = tk.Label(
            right_frame,
            text="Windows (CRLF)",
            anchor=tk.E,
            padx=8,
            pady=2,
            bg="#F0F0F0",
            fg="#000000",
            font=("Segoe UI", 9)
        )
        self.line_ending_label.pack(side=tk.RIGHT)
        
        # Separator
        sep2 = tk.Frame(right_frame, width=1, bg="#D0D0D0", height=14)
        sep2.pack(side=tk.RIGHT, padx=4, pady=4, fill=tk.Y)
        
        # Zoom level (like Notepad)
        self.zoom_label = tk.Label(
            right_frame,
            text="100%",
            anchor=tk.E,
            padx=8,
            pady=2,
            bg="#F0F0F0",
            fg="#000000",
            font=("Segoe UI", 9)
        )
        self.zoom_label.pack(side=tk.RIGHT)
        
        # Separator
        sep1 = tk.Frame(right_frame, width=1, bg="#D0D0D0", height=14)
        sep1.pack(side=tk.RIGHT, padx=4, pady=4, fill=tk.Y)
        
        # File type (like Notepad)
        self.file_type_label = tk.Label(
            right_frame,
            text="Plain text",
            anchor=tk.E,
            padx=8,
            pady=2,
            bg="#F0F0F0",
            fg="#000000",
            font=("Segoe UI", 9)
        )
        self.file_type_label.pack(side=tk.RIGHT)
        
        # Separator
        sep0 = tk.Frame(right_frame, width=1, bg="#D0D0D0", height=14)
        sep0.pack(side=tk.RIGHT, padx=4, pady=4, fill=tk.Y)
        
        # Character count
        self.word_count_label = tk.Label(
            right_frame,
            text="0 characters",
            anchor=tk.E,
            padx=8,
            pady=2,
            bg="#F0F0F0",
            fg="#000000",
            font=("Segoe UI", 9)
        )
        self.word_count_label.pack(side=tk.RIGHT)
        
        # Separator - will be themed
        self.status_sep = tk.Frame(right_frame, width=1, bg="#D0D0D0", height=14)
        self.status_sep.pack(side=tk.RIGHT, padx=4, pady=4, fill=tk.Y)
        
        # Line/Column info - Windows Notepad style
        self.position_label = tk.Label(
            right_frame,
            text="Ln 1, Col 1",
            anchor=tk.E,
            padx=10,
            pady=2,
            bg="#F0F0F0",
            fg="#000000",
            font=("Segoe UI", 9)
        )
        self.position_label.pack(side=tk.RIGHT)
        
        # Update status bar on text changes
        self.editor.text_widget.bind("<KeyRelease>", self.update_status_bar)
        self.editor.text_widget.bind("<Button-1>", self.update_status_bar)
        self.editor.text_widget.bind("<Key>", lambda e: self.editor.root.after(10, self.update_status_bar))
        
    def update_status_bar(self, event=None):
        """Update status bar information - Windows Notepad style."""
        # Get cursor position
        cursor_pos = self.editor.text_widget.index(tk.INSERT)
        line, col = cursor_pos.split('.')
        
        # Update position label - Windows Notepad format
        # Tk's column is 0-based; Notepad-style UI is 1-based.
        try:
            col_display = int(col) + 1
        except Exception:
            col_display = col
        self.position_label.config(text=f"Ln {line}, Col {col_display}")
        
        # Update character count - Windows Notepad style
        content = self.editor.text_widget.get(1.0, tk.END + "-1c")
        char_count = len(content)
        if char_count == 1:  # Just the newline
            char_count = 0
        # Format like Windows Notepad (no commas for small numbers)
        if char_count < 1000:
            self.word_count_label.config(text=f"{char_count} characters")
        else:
            self.word_count_label.config(text=f"{char_count:,} characters")
        
        # Update file status - clean and minimal like Notepad
        if self.editor.current_file:
            filename = os.path.basename(self.editor.current_file)
            status = filename
            if self.editor.is_modified:
                status += " *"
        else:
            status = "Untitled"
            if self.editor.is_modified:
                status += " *"
                
        self.status_text.config(text=status)
        
    def create_tabs(self):
        """Create tabbed interface for multiple files."""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.editor.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create initial tab
        self.add_tab("Untitled", None)
        
    def add_tab(self, title, filepath):
        """Add a new tab."""
        # Create frame for tab content
        tab_frame = tk.Frame(self.notebook)
        
        # Create text widget in tab
        from tkinter import scrolledtext
        text_widget = scrolledtext.ScrolledText(
            tab_frame,
            wrap=tk.WORD,
            undo=True,
            font=("Consolas", 11)
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Add tab to notebook
        self.notebook.add(tab_frame, text=title)
        
        # Store tab info
        tab_id = len(self.tabs)
        self.tabs[tab_id] = {
            "frame": tab_frame,
            "text_widget": text_widget,
            "filepath": filepath,
            "title": title,
            "is_modified": False
        }
        
        # Select the new tab
        self.notebook.select(tab_id)
        
        return tab_id
        
    def close_tab(self, tab_id):
        """Close a tab."""
        if tab_id in self.tabs:
            self.notebook.forget(tab_id)
            del self.tabs[tab_id]
            
    def get_current_tab(self):
        """Get current active tab."""
        try:
            selected = self.notebook.index(self.notebook.select())
            return self.tabs.get(selected)
        except:
            return None
            
    def update_tab_title(self, tab_id, title, modified=False):
        """Update tab title."""
        if tab_id in self.tabs:
            if modified:
                title += " *"
            self.notebook.tab(tab_id, text=title)
            self.tabs[tab_id]["title"] = title
            
    def create_line_numbers(self):
        """Create modern line numbers sidebar."""
        if self.line_numbers_visible and not self.line_numbers:
            # Get the container frame (text_container)
            if hasattr(self.editor, 'text_container'):
                text_parent = self.editor.text_container
            else:
                text_parent = self.editor.text_widget.master
            
            # Clean line numbers frame - Windows Notepad style
            line_frame = tk.Frame(text_parent, width=50, bg="#FAFAFA")
            # Pack to left side
            line_frame.pack(side=tk.LEFT, fill=tk.Y)
            
            # Subtle right border
            border = tk.Frame(line_frame, width=1, bg="#E5E5E5")
            border.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Repack text widget to ensure proper layout
            self.editor.text_widget.pack_forget()
            self.editor.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Clean line numbers text widget
            self.line_numbers = tk.Text(
                line_frame,
                width=4,
                bg="#FAFAFA",
                fg="#808080",
                state=tk.DISABLED,
                font=("Segoe UI", 11),
                padx=6,
                pady=12,
                wrap=tk.NONE,
                borderwidth=0,
                highlightthickness=0
            )
            self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
            
            # Mouse wheel is handled in editor.py, just sync line numbers on scroll
            def on_scroll(event):
                self.on_text_scroll(event)
                
            # Bind to text widget's scrollbar
            try:
                scrollbar = self.editor.text_widget.cget("yscrollcommand")
                if scrollbar:
                    # The scrollbar will trigger updates
                    pass
            except:
                pass
            
            # Bind text changes
            self.editor.text_widget.bind("<<Modified>>", lambda e: self.update_line_numbers())
            
            # Update line numbers
            self.update_line_numbers()
            
    def on_text_scroll(self, event):
        """Handle text widget scroll to sync line numbers."""
        if self.line_numbers:
            self.update_line_numbers()
            
    def update_line_numbers(self):
        """Update line numbers display."""
        if not self.line_numbers or not self.line_numbers_visible:
            return
            
        # Get total lines
        total_lines = int(self.editor.text_widget.index(tk.END).split('.')[0]) - 1
        
        # Update line numbers
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        
        for i in range(1, total_lines + 1):
            self.line_numbers.insert(tk.END, f"{i}\n")
            
        self.line_numbers.config(state=tk.DISABLED)
        
        # Sync scroll position
        try:
            # Get scroll position
            yview = self.editor.text_widget.yview()
            self.line_numbers.yview_moveto(yview[0])
        except:
            pass
            
    def toggle_line_numbers(self):
        """Toggle line numbers display."""
        self.line_numbers_visible = not self.line_numbers_visible
        if self.line_numbers_visible:
            if not self.line_numbers:
                self.create_line_numbers()
        else:
            if self.line_numbers:
                line_frame = self.line_numbers.master
                self.line_numbers.destroy()
                line_frame.destroy()
                self.line_numbers = None

