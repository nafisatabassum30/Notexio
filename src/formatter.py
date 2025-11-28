"""
Formatting operations for Notexio text editor.
"""
import tkinter as tk
from tkinter import font, colorchooser
import tkinter.font as tkfont


class Formatter:
    """Manages text formatting."""
    
    def __init__(self, editor):
        self.editor = editor
        self.current_font_family = "Segoe UI"
        self.current_font_size = 11
        self.current_text_color = "#000000"
        self.current_bg_color = "#FFFFFF"
        self.current_font_weight = "normal"
        self.current_font_slant = "roman"
        self.current_font_underline = False
        
        # Default formatting - Windows Notepad style
        self.default_font_family = "Segoe UI"
        self.default_font_size = 11
        self.default_text_color = "#000000"
        self.default_bg_color = "#FFFFFF"
        
        self.update_font()
        
    def update_font(self):
        """Update the font configuration."""
        font_config = (
            self.current_font_family,
            self.current_font_size,
            self.current_font_weight,
            self.current_font_slant
        )
        
        # Configure text widget font
        self.editor.text_widget.config(
            font=font_config,
            foreground=self.current_text_color,
            background=self.current_bg_color,
            insertbackground=self.current_text_color
        )
        
    def change_font_family(self):
        """Change font family."""
        dialog = tk.Toplevel(self.editor.root)
        dialog.title("Font Family")
        dialog.geometry("300x400")
        dialog.transient(self.editor.root)
        
        # Get available fonts
        available_fonts = sorted(tkfont.families())
        
        # Listbox with scrollbar
        frame = tk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        
        for f in available_fonts:
            listbox.insert(tk.END, f)
            
        # Select current font
        try:
            index = available_fonts.index(self.current_font_family)
            listbox.selection_set(index)
            listbox.see(index)
        except ValueError:
            pass
            
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        def apply_font():
            selection = listbox.curselection()
            if selection:
                self.current_font_family = available_fonts[selection[0]]
                self.update_font()
                dialog.destroy()
                
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="OK", command=apply_font).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
    def change_font_size(self):
        """Change font size."""
        from tkinter import simpledialog, messagebox
        size_str = simpledialog.askstring(
            "Font Size",
            "Enter font size:",
            initialvalue=str(self.current_font_size),
            parent=self.editor.root
        )
        
        if size_str:
            try:
                size = int(size_str)
                if 8 <= size <= 72:
                    self.current_font_size = size
                    self.update_font()
                else:
                    messagebox.showerror("Error", "Font size must be between 8 and 72.")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")
                
    def change_text_color(self):
        """Change text color."""
        color = colorchooser.askcolor(
            title="Choose Text Color",
            color=self.current_text_color,
            parent=self.editor.root
        )
        
        if color[1]:  # User didn't cancel
            self.current_text_color = color[1]
            self.update_font()
            
    def change_bg_color(self):
        """Change background color."""
        color = colorchooser.askcolor(
            title="Choose Background Color",
            color=self.current_bg_color,
            parent=self.editor.root
        )
        
        if color[1]:  # User didn't cancel
            self.current_bg_color = color[1]
            self.update_font()
            
    def toggle_bold(self):
        """Toggle bold formatting."""
        if self.current_font_weight == "normal":
            self.current_font_weight = "bold"
        else:
            self.current_font_weight = "normal"
        self.update_font()
        
    def toggle_italic(self):
        """Toggle italic formatting."""
        if self.current_font_slant == "roman":
            self.current_font_slant = "italic"
        else:
            self.current_font_slant = "roman"
        self.update_font()
        
    def toggle_underline(self):
        """Toggle underline formatting."""
        self.current_font_underline = not self.current_font_underline
        # Note: Tkinter Text widget doesn't support underline directly
        # This would require tag-based implementation for selected text
        # For now, we'll just track the state
        
    def apply_formatting_to_selection(self, tag_name="formatted"):
        """Apply formatting to selected text using tags."""
        try:
            sel_start = self.editor.text_widget.index(tk.SEL_FIRST)
            sel_end = self.editor.text_widget.index(tk.SEL_LAST)
            
            # Create font for tag
            tag_font = tkfont.Font(
                family=self.current_font_family,
                size=self.current_font_size,
                weight=self.current_font_weight,
                slant=self.current_font_slant,
                underline=self.current_font_underline
            )
            
            # Configure tag
            self.editor.text_widget.tag_configure(
                tag_name,
                font=tag_font,
                foreground=self.current_text_color
            )
            
            # Apply tag to selection
            self.editor.text_widget.tag_add(tag_name, sel_start, sel_end)
        except tk.TclError:
            pass  # No selection
            
    def restore_default_formatting(self):
        """Restore default formatting."""
        self.current_font_family = self.default_font_family
        self.current_font_size = self.default_font_size
        self.current_text_color = self.default_text_color
        self.current_bg_color = self.default_bg_color
        self.current_font_weight = "normal"
        self.current_font_slant = "roman"
        self.current_font_underline = False
        self.update_font()

