"""
Safety features for Notexio text editor.
"""
import tkinter as tk
import os
import threading
import time
from datetime import datetime


class SafetyFeatures:
    """Manages safety features like auto-save and recovery."""
    
    def __init__(self, editor, file_manager, recovery_dir="recovery"):
        self.editor = editor
        self.file_manager = file_manager
        self.recovery_dir = recovery_dir
        self.auto_save_enabled = False
        self.auto_save_interval = 300  # 5 minutes in seconds
        self.auto_save_thread = None
        self.auto_save_running = False
        
        # Create recovery directory if it doesn't exist
        if not os.path.exists(self.recovery_dir):
            os.makedirs(self.recovery_dir)
            
    def enable_auto_save(self, interval=300):
        """Enable auto-save feature."""
        self.auto_save_enabled = True
        self.auto_save_interval = interval
        self.start_auto_save()
        
    def disable_auto_save(self):
        """Disable auto-save feature."""
        self.auto_save_enabled = False
        self.stop_auto_save()
        
    def start_auto_save(self):
        """Start auto-save thread."""
        if not self.auto_save_running and self.auto_save_enabled:
            self.auto_save_running = True
            self.auto_save_thread = threading.Thread(target=self._auto_save_loop, daemon=True)
            self.auto_save_thread.start()
            
    def stop_auto_save(self):
        """Stop auto-save thread."""
        self.auto_save_running = False
        
    def _auto_save_loop(self):
        """Auto-save loop running in background thread."""
        while self.auto_save_running and self.auto_save_enabled:
            time.sleep(self.auto_save_interval)
            if self.auto_save_running and self.editor.is_modified:
                # Tkinter widgets are not thread-safe; schedule snapshot on UI thread.
                self.request_recovery_file()
                
    def request_recovery_file(self):
        """Request a recovery file write from any thread (thread-safe)."""
        try:
            # Snapshot must happen on the Tkinter (UI) thread.
            self.editor.root.after(0, self._snapshot_and_write_recovery_file_async)
        except Exception:
            # If the root is already destroyed/shutting down, ignore.
            pass
            
    def _snapshot_and_write_recovery_file_async(self):
        """Snapshot editor content on UI thread, then write in background."""
        try:
            if not getattr(self.editor, "is_modified", False):
                return
            content = self.editor.text_widget.get(1.0, tk.END + "-1c")
            current_file = getattr(self.editor, "current_file", None)
            if not content.strip():
                return
            threading.Thread(
                target=self._write_recovery_file,
                args=(content, current_file),
                daemon=True
            ).start()
        except Exception as e:
            print(f"Error snapshotting recovery content: {e}")
            
    def create_recovery_file(self):
        """Create a recovery file (synchronous; call from UI thread)."""
        try:
            content = self.editor.text_widget.get(1.0, tk.END + "-1c")
            current_file = getattr(self.editor, "current_file", None)
            if not content.strip():
                return
            self._write_recovery_file(content, current_file)
        except Exception as e:
            print(f"Error creating recovery file: {e}")
            
    def _write_recovery_file(self, content, current_file):
        """Write a recovery file to disk (no Tkinter calls)."""
        # Generate recovery filename (include milliseconds to avoid collisions)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        if current_file:
            filename = os.path.basename(current_file)
            recovery_filename = f"{filename}_{timestamp}.recovery"
        else:
            recovery_filename = f"untitled_{timestamp}.recovery"
            
        recovery_path = os.path.join(self.recovery_dir, recovery_filename)
        
        # Save recovery file
        with open(recovery_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        # Keep only last N recovery files
        self.cleanup_old_recovery_files()
        
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

