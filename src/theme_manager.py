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
                "bg": "#202020",  # Modern Notepad dark background
                "fg": "#D4D4D4",  # Light text
                "select_bg": "#0078D4",  # Windows blue selection
                "select_fg": "#FFFFFF",
                "insert_bg": "#D4D4D4",
                "menu_bg": "#2D2D30",  # Dark menu bar
                "menu_fg": "#CCCCCC",
                "toolbar_bg": "#2D2D30",  # Dark toolbar
                "status_bg": "#007ACC",  # Blue status bar like Notepad
                "border": "#3E3E42",
                "status_fg": "#FFFFFF"  # White text on status bar
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
        
        # Apply to UI components if available - modern Notepad style
        if hasattr(self.editor, 'ui_components') and self.editor.ui_components:
            if hasattr(self.editor.ui_components, 'toolbar_frame') and self.editor.ui_components.toolbar_frame:
                toolbar_bg = theme.get("toolbar_bg", theme["menu_bg"])
                toolbar_fg = theme.get("menu_fg", theme["fg"])
                    
                self.editor.ui_components.toolbar_frame.config(bg=toolbar_bg)
                # Update toolbar buttons
                for widget in self.editor.ui_components.toolbar_frame.winfo_children():
                    if isinstance(widget, tk.Frame):
                        widget.config(bg=toolbar_bg)
                        for btn in widget.winfo_children():
                            if isinstance(btn, tk.Button):
                                if theme_name == "dark":
                                    btn.config(bg="#3E3E42", fg="#CCCCCC", activebackground="#505050", activeforeground="#FFFFFF")
                                else:
                                    btn.config(bg="#FAFAFA", fg="#000000", activebackground="#E8E8E8", activeforeground="#000000")
                                    
            if hasattr(self.editor.ui_components, 'status_bar') and self.editor.ui_components.status_bar:
                status_bg = theme.get("status_bg", theme["menu_bg"])
                status_fg = theme.get("status_fg", theme.get("menu_fg", theme["fg"]))
                    
                self.editor.ui_components.status_bar.config(bg=status_bg)
                # Update status bar border
                if hasattr(self.editor.ui_components, 'status_border'):
                    if theme_name == "dark":
                        self.editor.ui_components.status_border.config(bg="#4A9EFF")
                    else:
                        self.editor.ui_components.status_border.config(bg="#D0D0D0")
                        
                # Update all status bar labels directly
                status_labels = [
                    'status_text', 'position_label', 'word_count_label', 
                    'file_type_label', 'zoom_label', 'line_ending_label', 'encoding_label'
                ]
                for label_name in status_labels:
                    if hasattr(self.editor.ui_components, label_name):
                        label = getattr(self.editor.ui_components, label_name)
                        if label:
                            label.config(bg=status_bg, fg=status_fg)
                        
                # Update status bar labels and separators in frames
                for widget in self.editor.ui_components.status_bar.winfo_children():
                    if isinstance(widget, tk.Frame):
                        widget.config(bg=status_bg)
                        for child in widget.winfo_children():
                            if isinstance(child, tk.Label):
                                child.config(bg=status_bg, fg=status_fg)
                            elif isinstance(child, tk.Frame):  # Separator
                                if theme_name == "dark":
                                    child.config(bg="#4A9EFF")  # Lighter blue for separator
                                else:
                                    child.config(bg="#D0D0D0")
        
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
        dialog.geometry("400x250")
        dialog.transient(self.editor.root)
        dialog.configure(bg="#FAFAFA")
        
        # Initialize color variables
        self.custom_bg = None
        self.custom_fg = None
        
        # Background color section
        bg_frame = tk.Frame(dialog, bg="#FAFAFA")
        bg_frame.pack(pady=15, padx=20, fill=tk.X)
        tk.Label(bg_frame, text="Background Color:", bg="#FAFAFA", font=("Segoe UI", 9)).pack(side=tk.LEFT)
        bg_preview = tk.Label(bg_frame, text="  ", bg="#FFFFFF", relief=tk.SUNKEN, width=5)
        bg_preview.pack(side=tk.LEFT, padx=10)
        
        def choose_bg():
            color = colorchooser.askcolor(title="Choose Background Color", parent=dialog)
            if color[1]:
                self.custom_bg = color[1]
                bg_preview.config(bg=color[1])
                
        bg_button = tk.Button(bg_frame, text="Choose", command=choose_bg, width=10)
        bg_button.pack(side=tk.LEFT, padx=5)
        
        # Text color section
        fg_frame = tk.Frame(dialog, bg="#FAFAFA")
        fg_frame.pack(pady=15, padx=20, fill=tk.X)
        tk.Label(fg_frame, text="Text Color:", bg="#FAFAFA", font=("Segoe UI", 9)).pack(side=tk.LEFT)
        fg_preview = tk.Label(fg_frame, text="  ", bg="#000000", relief=tk.SUNKEN, width=5)
        fg_preview.pack(side=tk.LEFT, padx=10)
        
        def choose_fg():
            color = colorchooser.askcolor(title="Choose Text Color", parent=dialog)
            if color[1]:
                self.custom_fg = color[1]
                fg_preview.config(bg=color[1])
                
        fg_button = tk.Button(fg_frame, text="Choose", command=choose_fg, width=10)
        fg_button.pack(side=tk.LEFT, padx=5)
        
        # Button frame
        button_frame = tk.Frame(dialog, bg="#FAFAFA")
        button_frame.pack(pady=20)
        
        def apply_theme():
            if self.custom_bg and self.custom_fg:
                self.set_custom_theme(self.custom_bg, self.custom_fg)
                dialog.destroy()
            else:
                from tkinter import messagebox
                messagebox.showwarning("Warning", "Please select both background and text colors.")
                
        tk.Button(button_frame, text="Apply", command=apply_theme, width=12, height=1).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, width=12, height=1).pack(side=tk.LEFT, padx=5)
            
    def load_theme(self):
        """Load theme from settings."""
        theme = self.settings_manager.load_theme()
        if theme:
            self.apply_theme(theme)

