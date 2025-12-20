"""
Safety features for Notexio text editor.
"""
import tkinter as tk
import os
from datetime import datetime


class SafetyFeatures:
    """Manages safety features like auto-save and recovery."""
    
    def __init__(self, editor, file_manager, recovery_dir="recovery"):
        self.editor = editor
        self.file_manager = file_manager
        self.recovery_dir = recovery_dir
        self.auto_save_enabled = False
        self.auto_save_interval = 300  # 5 minutes in seconds
        self._auto_save_after_id = None
        
        # Create recovery directory if it doesn't exist
        if not os.path.exists(self.recovery_dir):
            os.makedirs(self.recovery_dir)
            
    def enable_auto_save(self, interval=300):
        """Enable auto-save feature."""
        self.auto_save_enabled = True
        self.auto_save_interval = int(interval)
        self.start_auto_save()
        
    def disable_auto_save(self):
        """Disable auto-save feature."""
        self.auto_save_enabled = False
        self.stop_auto_save()
        
    def start_auto_save(self):
        """Start auto-save scheduling (Tk main thread)."""
        if not self.auto_save_enabled:
            return
        if self._auto_save_after_id is None:
            self._schedule_next_auto_save()
            
    def stop_auto_save(self):
        """Stop auto-save scheduling."""
        if self._auto_save_after_id is not None:
            try:
                self.editor.root.after_cancel(self._auto_save_after_id)
            except Exception:
                pass
            finally:
                self._auto_save_after_id = None

    def _schedule_next_auto_save(self):
        """Schedule the next auto-save tick on Tk event loop."""
        if not self.auto_save_enabled:
            return
        interval_ms = max(1, int(self.auto_save_interval * 1000))
        self._auto_save_after_id = self.editor.root.after(interval_ms, self._auto_save_tick)

    def _auto_save_tick(self):
        """One auto-save tick (runs in Tk main thread)."""
        # Clear id first so stop_auto_save can cancel cleanly.
        self._auto_save_after_id = None
        if self.auto_save_enabled and self.editor.is_modified:
            self.create_recovery_file()
        self._schedule_next_auto_save()
                
    def create_recovery_file(self):
        """Create a recovery file."""
        try:
            content = self.editor.text_widget.get(1.0, tk.END + "-1c")
            
            if not content.strip():
                return
                
            # Generate recovery filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if self.editor.current_file:
                filename = os.path.basename(self.editor.current_file)
                recovery_filename = f"{filename}_{timestamp}.recovery"
            else:
                recovery_filename = f"untitled_{timestamp}.recovery"
                
            recovery_path = os.path.join(self.recovery_dir, recovery_filename)
            
            # Save recovery file
            with open(recovery_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            # Keep only last 10 recovery files
            self.cleanup_old_recovery_files()
            
        except Exception as e:
            print(f"Error creating recovery file: {e}")
            
    def cleanup_old_recovery_files(self, keep=10):
        """Clean up old recovery files, keeping only the most recent ones."""
        try:
            recovery_files = []
            for filename in os.listdir(self.recovery_dir):
                if filename.endswith('.recovery'):
                    filepath = os.path.join(self.recovery_dir, filename)
                    recovery_files.append((filepath, os.path.getmtime(filepath)))
                    
            # Sort by modification time (newest first)
            recovery_files.sort(key=lambda x: x[1], reverse=True)
            
            # Remove old files
            for filepath, _ in recovery_files[keep:]:
                try:
                    os.remove(filepath)
                except Exception:
                    pass
                    
        except Exception as e:
            print(f"Error cleaning up recovery files: {e}")
            
    def check_recovery_files(self):
        """Check for recovery files on startup."""
        recovery_files = []
        try:
            for filename in os.listdir(self.recovery_dir):
                if filename.endswith('.recovery'):
                    filepath = os.path.join(self.recovery_dir, filename)
                    recovery_files.append((filepath, os.path.getmtime(filepath)))
                    
            if recovery_files:
                # Sort by modification time (newest first)
                recovery_files.sort(key=lambda x: x[1], reverse=True)
                return recovery_files
        except Exception:
            pass
            
        return []
        
    def restore_recovery_file(self, recovery_path):
        """Restore content from a recovery file."""
        try:
            with open(recovery_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self.editor.text_widget.delete(1.0, tk.END)
            self.editor.text_widget.insert(1.0, content)
            self.editor.is_modified = True
            self.editor.update_title()
            
            return True
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to restore recovery file:\n{str(e)}")
            return False
            
    def warn_on_exit(self):
        """Check for unsaved changes and warn user before exit."""
        return self.file_manager.check_unsaved_changes()

