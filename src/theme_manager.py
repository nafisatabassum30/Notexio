"""
Theme management for Notexio text editor.
"""
import tkinter as tk


class ThemeManager:
    """Manages themes."""
    
    def __init__(self, editor, settings_manager):
        self.editor = editor
        self.settings_manager = settings_manager
        self.current_theme = "light"
        
        # Windows Notepad-style theme color schemes
        self.themes = {
            "light": {
                "bg": "#FFFFFF",
                "fg": "#000000",
                "select_bg": "#0078D4",
                "select_fg": "#FFFFFF",
                "insert_bg": "#000000",
                "menu_bg": "#FAFAFA",
                "menu_fg": "#000000",
                "toolbar_bg": "#FAFAFA",
                "status_bg": "#F0F0F0",
                "border": "#E5E5E5"
            },
            "dark": {
                "bg": "#1E1E1E",
                "fg": "#D4D4D4",
                "select_bg": "#0078D4",
                "select_fg": "#FFFFFF",
                "insert_bg": "#D4D4D4",
                "menu_bg": "#252526",
                "menu_fg": "#CCCCCC",
                "toolbar_bg": "#2D2D30",
                "status_bg": "#007ACC",
                "border": "#3E3E42"
            }
        }
        
        # Custom theme (user-defined)
        self.custom_theme = None
        
    def apply_theme(self, theme_name):
        """Apply a theme."""
        if theme_name == "custom" and self.custom_theme:
            theme = self.custom_theme
        elif theme_name in self.themes:
            theme = self.themes[theme_name]
        else:
            theme = self.themes["light"]
            
        self.current_theme = theme_name
        
        # Apply to text widget
        self.editor.text_widget.config(
            bg=theme["bg"],
            fg=theme["fg"],
            selectbackground=theme["select_bg"],
            selectforeground=theme["select_fg"],
            insertbackground=theme["insert_bg"]
        )
        
        # Apply to root window
        self.editor.root.config(bg=theme["bg"])
        
        # Apply to UI components if available
        if hasattr(self.editor, 'ui_components') and self.editor.ui_components:
            if hasattr(self.editor.ui_components, 'toolbar_frame') and self.editor.ui_components.toolbar_frame:
                self.editor.ui_components.toolbar_frame.config(bg=theme.get("toolbar_bg", theme["menu_bg"]))
                # Update toolbar buttons
                for widget in self.editor.ui_components.toolbar_frame.winfo_children():
                    if isinstance(widget, tk.Frame):
                        for btn in widget.winfo_children():
                            if isinstance(btn, tk.Button):
                                if theme_name == "dark":
                                    btn.config(bg="#3E3E42", fg="#CCCCCC", activebackground="#505050")
                                else:
                                    btn.config(bg="#FFFFFF", fg="#333333", activebackground="#E8E8E8")
                                    
            if hasattr(self.editor.ui_components, 'status_bar') and self.editor.ui_components.status_bar:
                status_bg = theme.get("status_bg", theme["menu_bg"])
                self.editor.ui_components.status_bar.config(bg=status_bg)
                # Update status bar labels
                for widget in self.editor.ui_components.status_bar.winfo_children():
                    if isinstance(widget, tk.Frame):
                        widget.config(bg=status_bg)
                        for label in widget.winfo_children():
                            if isinstance(label, tk.Label):
                                label.config(bg=status_bg, fg=theme["menu_fg"])
        
        # Store theme preference
        self.settings_manager.save_theme(theme_name)
        
    def set_light_mode(self):
        """Set light mode."""
        self.apply_theme("light")
        
    def set_dark_mode(self):
        """Set dark mode."""
        self.apply_theme("dark")
        
    def set_custom_theme(self, bg_color, fg_color, select_bg=None, select_fg=None):
        """Set custom theme colors."""
        self.custom_theme = {
            "bg": bg_color,
            "fg": fg_color,
            "select_bg": select_bg or "#316AC5",
            "select_fg": select_fg or "#FFFFFF",
            "insert_bg": fg_color,
            "menu_bg": bg_color,
            "menu_fg": fg_color
        }
        self.apply_theme("custom")
        
    def customize_theme(self):
        """Open theme customization dialog."""
        from tkinter import colorchooser
        
        dialog = tk.Toplevel(self.editor.root)
        dialog.title("Customize Theme")
        dialog.geometry("400x300")
        dialog.transient(self.editor.root)
        
        # Background color
        tk.Label(dialog, text="Background Color:").pack(pady=5)
        bg_button = tk.Button(dialog, text="Choose", command=lambda: self.choose_color("bg", dialog))
        bg_button.pack(pady=5)
        
        # Foreground color
        tk.Label(dialog, text="Text Color:").pack(pady=5)
        fg_button = tk.Button(dialog, text="Choose", command=lambda: self.choose_color("fg", dialog))
        fg_button.pack(pady=5)
        
        # Apply button
        tk.Button(dialog, text="Apply", command=lambda: self.apply_custom_from_dialog(dialog)).pack(pady=20)
        
        self.custom_dialog = dialog
        self.custom_bg = None
        self.custom_fg = None
        
    def choose_color(self, color_type, dialog):
        """Choose a color for custom theme."""
        color = colorchooser.askcolor(title=f"Choose {color_type.upper()} Color", parent=dialog)
        if color[1]:
            if color_type == "bg":
                self.custom_bg = color[1]
            else:
                self.custom_fg = color[1]
                
    def apply_custom_from_dialog(self, dialog):
        """Apply custom theme from dialog."""
        if self.custom_bg and self.custom_fg:
            self.set_custom_theme(self.custom_bg, self.custom_fg)
            dialog.destroy()
        else:
            from tkinter import messagebox
            messagebox.showwarning("Warning", "Please select both background and text colors.")
            
    def load_theme(self):
        """Load theme from settings."""
        theme = self.settings_manager.load_theme()
        if theme:
            self.apply_theme(theme)

