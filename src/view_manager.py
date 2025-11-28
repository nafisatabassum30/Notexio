"""
View management for Notexio text editor.
"""
import tkinter as tk


class ViewManager:
    """Manages view options."""
    
    def __init__(self, editor):
        self.editor = editor
        self.zoom_level = 100  # Percentage
        self.word_wrap = True
        self.line_numbers_visible = False
        self.is_fullscreen = False
        self.base_font_size = 11
        
    def zoom_in(self):
        """Zoom in text."""
        if self.zoom_level < 200:
            self.zoom_level += 10
            self.apply_zoom()
            
    def zoom_out(self):
        """Zoom out text."""
        if self.zoom_level > 50:
            self.zoom_level -= 10
            self.apply_zoom()
            
    def reset_zoom(self):
        """Reset zoom to 100%."""
        self.zoom_level = 100
        self.apply_zoom()
        
    def apply_zoom(self):
        """Apply zoom level to text."""
        # Get current font
        current_font = self.editor.text_widget.cget("font")
        if isinstance(current_font, str):
            # Parse font string
            font_parts = current_font.split()
            if len(font_parts) >= 2:
                family = font_parts[0]
                size = int(font_parts[1])
            else:
                family = "Consolas"
                size = self.base_font_size
        else:
            family = current_font.actual()["family"]
            size = current_font.actual()["size"]
            
        # Calculate new size
        new_size = int(self.base_font_size * (self.zoom_level / 100))
        
        # Apply new font
        self.editor.text_widget.config(font=(family, new_size))
        
    def toggle_word_wrap(self):
        """Toggle word wrap."""
        self.word_wrap = not self.word_wrap
        if self.word_wrap:
            self.editor.text_widget.config(wrap=tk.WORD)
        else:
            self.editor.text_widget.config(wrap=tk.NONE)
            
    def toggle_line_numbers(self):
        """Toggle line numbers display."""
        self.line_numbers_visible = not self.line_numbers_visible
        # Line numbers are implemented in UI components
        # This method is kept for compatibility
        
    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.is_fullscreen = not self.is_fullscreen
        self.editor.root.attributes("-fullscreen", self.is_fullscreen)
        
        # Add escape key binding to exit fullscreen
        if self.is_fullscreen:
            self.editor.root.bind("<Escape>", lambda e: self.toggle_fullscreen())
        else:
            self.editor.root.unbind("<Escape>")

