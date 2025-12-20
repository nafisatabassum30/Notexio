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
        # Get initial font size from text widget
        try:
            current_font = self.editor.text_widget.cget("font")
            if isinstance(current_font, (tuple, list)):
                self.base_font_size = current_font[1]
            elif isinstance(current_font, str):
                font_parts = current_font.split()
                self.base_font_size = int(font_parts[1]) if len(font_parts) >= 2 else 11
            else:
                self.base_font_size = current_font.actual()["size"]
        except:
            self.base_font_size = 11
        
    def zoom_in(self):
        """Zoom in text."""
        if self.zoom_level < 200:
            self.zoom_level += 10
            self.apply_zoom()
            self.update_zoom_label()
            
    def zoom_out(self):
        """Zoom out text."""
        if self.zoom_level > 50:
            self.zoom_level -= 10
            self.apply_zoom()
            self.update_zoom_label()
            
    def reset_zoom(self):
        """Reset zoom to 100%."""
        self.zoom_level = 100
        self.apply_zoom()
        self.update_zoom_label()
        
    def update_zoom_label(self):
        """Update zoom label in status bar."""
        if hasattr(self.editor, 'ui_components') and self.editor.ui_components:
            if hasattr(self.editor.ui_components, 'zoom_label'):
                self.editor.ui_components.zoom_label.config(text=f"{self.zoom_level}%")
        
    def apply_zoom(self):
        """Apply zoom level to text."""
        # Get current font family
        try:
            current_font = self.editor.text_widget.cget("font")
            if isinstance(current_font, (tuple, list)):
                family = current_font[0]
            elif isinstance(current_font, str):
                font_parts = current_font.split()
                family = font_parts[0] if font_parts else "Segoe UI"
            else:
                family = current_font.actual()["family"]
        except:
            family = "Segoe UI"
            
        # Calculate new size based on base font size
        new_size = int(self.base_font_size * (self.zoom_level / 100))
        
        # Apply new font
        self.editor.text_widget.config(font=(family, new_size))
        
        # Update line numbers if visible
        if hasattr(self.editor, 'ui_components') and self.editor.ui_components:
            if hasattr(self.editor.ui_components, 'line_numbers') and self.editor.ui_components.line_numbers:
                self.editor.ui_components.line_numbers.config(font=(family, new_size))
        
    def toggle_word_wrap(self):
        """Toggle word wrap."""
        self.word_wrap = not self.word_wrap
        if self.word_wrap:
            self.editor.text_widget.config(wrap=tk.WORD)
        else:
            self.editor.text_widget.config(wrap=tk.NONE)
        # Force update
        self.editor.text_widget.update()
            
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

