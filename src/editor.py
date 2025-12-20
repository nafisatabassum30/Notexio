"""
Main editor window class for Notexio text editor.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import os


class Editor:
    """Main editor window class."""
    
    def set_icon(self):
        """Set the application icon."""
        import os
        
        # Get project root directory (parent of src directory)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_paths = [
            os.path.join(project_root, "icon.ico"),  # Project root
            "icon.ico",  # Current directory
            os.path.join(project_root, "assets", "icon.ico"),  # Assets folder
            "assets/icon.ico"  # Relative assets
        ]
        
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                try:
                    self.root.iconbitmap(icon_path)
                    return
                except Exception:
                    continue
        
        # If no icon file found, try to create a simple one or use default
        try:
            # Try to create a simple icon programmatically
            self.create_simple_icon()
        except:
            pass  # Use default icon if creation fails
            
    def create_simple_icon(self):
        """Create a simple icon if PIL is available."""
        try:
            from PIL import Image, ImageDraw
            import os
            
            # Create icon directory if needed
            os.makedirs("assets", exist_ok=True)
            
            # Create a 256x256 icon
            size = 256
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Modern blue background circle
            draw.ellipse([20, 20, size-20, size-20], fill=(0, 120, 212, 255))  # Windows blue
            
            # Draw a stylized "N" for Notexio
            # Left vertical line
            draw.rectangle([80, 60, 100, size-60], fill=(255, 255, 255, 255))
            # Diagonal line
            points = [(100, 60), (size-100, size-60), (size-80, size-60), (80, 60)]
            draw.polygon(points, fill=(255, 255, 255, 255))
            # Right vertical line
            draw.rectangle([size-100, 60, size-80, size-60], fill=(255, 255, 255, 255))
            
            # Save as ICO with multiple sizes
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(project_root, "icon.ico")
            img.save(icon_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
            
            # Set the icon
            self.root.iconbitmap(icon_path)
        except ImportError:
            # PIL not available, skip icon creation
            pass
        except Exception:
            # Silently fail
            pass
            
    def __init__(self, root):
        self.root = root
        self.root.title("Notexio - Untitled")
        self.root.geometry("900x650")
        
        # Set application icon
        self.set_icon()
        
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
        
        # Enable mouse wheel scrolling
        self.text_widget.bind("<MouseWheel>", self.on_mousewheel)
        self.text_widget.bind("<Button-4>", self.on_mousewheel)  # Linux
        self.text_widget.bind("<Button-5>", self.on_mousewheel)  # Linux
        
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        # Windows and Mac
        if hasattr(event, 'delta') and event.delta:
            self.text_widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # Linux
        elif hasattr(event, 'num'):
            if event.num == 4:
                self.text_widget.yview_scroll(-1, "units")
            elif event.num == 5:
                self.text_widget.yview_scroll(1, "units")
        # Sync line numbers (if enabled)
        if self.ui_components and getattr(self.ui_components, "line_numbers_visible", False):
            try:
                self.ui_components.update_line_numbers()
            except Exception:
                pass
        return "break"
        
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

