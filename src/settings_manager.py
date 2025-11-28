"""
Settings manager for Notexio text editor.
"""
import json
import os


class SettingsManager:
    """Manages application settings."""
    
    def __init__(self, config_file="config/settings.json"):
        self.config_file = config_file
        self.settings = self.load_settings()
        
    def load_settings(self):
        """Load settings from JSON file."""
        default_settings = {
            "theme": "light",
            "recent_files": [],
            "window_width": 800,
            "window_height": 600,
            "font_family": "Consolas",
            "font_size": 11,
            "word_wrap": True,
            "line_numbers": False,
            "auto_save": False,
            "auto_save_interval": 300
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_settings.update(settings)
                    return default_settings
        except Exception as e:
            print(f"Error loading settings: {e}")
            
        return default_settings
        
    def save_settings(self):
        """Save settings to JSON file."""
        try:
            # Ensure config directory exists
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
            
    def get_setting(self, key, default=None):
        """Get a setting value."""
        return self.settings.get(key, default)
        
    def set_setting(self, key, value):
        """Set a setting value."""
        self.settings[key] = value
        self.save_settings()
        
    def save_recent_files(self, recent_files):
        """Save recent files list."""
        self.set_setting("recent_files", recent_files)
        
    def load_recent_files(self):
        """Load recent files list."""
        return self.get_setting("recent_files", [])
        
    def save_theme(self, theme):
        """Save theme preference."""
        self.set_setting("theme", theme)
        
    def load_theme(self):
        """Load theme preference."""
        return self.get_setting("theme", "light")

