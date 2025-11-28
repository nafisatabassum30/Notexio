"""
Miscellaneous features for Notexio text editor.
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys


class MiscFeatures:
    """Manages miscellaneous features like drag & drop, print, and PDF export."""
    
    def __init__(self, editor, file_manager):
        self.editor = editor
        self.file_manager = file_manager
        
    def enable_drag_drop(self):
        """Enable drag and drop file opening."""
        # Windows-specific drag and drop
        if sys.platform == "win32":
            try:
                import tkinterdnd2 as tkdnd
                self.dnd = tkdnd
                self.editor.root.drop_target_register(tkdnd.DND_FILES)
                self.editor.root.dnd_bind('<<Drop>>', self.on_drop)
            except ImportError:
                # Fallback: use Tkinter's built-in drop (limited support)
                self.editor.root.bind("<Button-1>", self.on_drop_click)
        else:
            # For other platforms, use file dialog fallback
            self.editor.root.bind("<Button-1>", self.on_drop_click)
            
    def on_drop(self, event):
        """Handle file drop event."""
        if sys.platform == "win32" and hasattr(self, 'dnd'):
            files = self.editor.root.tk.splitlist(event.data)
            if files:
                filepath = files[0]
                if os.path.isfile(filepath):
                    self.file_manager.open_file(filepath)
        else:
            # Fallback implementation
            pass
            
    def on_drop_click(self, event):
        """Fallback for drag and drop (opens file dialog on click)."""
        # This is a simple fallback - full drag & drop requires tkinterdnd2
        pass
        
    def print_file(self):
        """Print the current file."""
        try:
            # Get content
            content = self.editor.text_widget.get(1.0, tk.END + "-1c")
            
            # Create print dialog
            from tkinter import simpledialog
            response = messagebox.askyesno(
                "Print",
                "This will send the document to your default printer.\n\nDo you want to continue?",
                icon=messagebox.QUESTION
            )
            
            if response:
                # For Windows, use win32print
                if sys.platform == "win32":
                    try:
                        import win32print
                        import win32api
                        
                        # Get default printer
                        printer_name = win32print.GetDefaultPrinter()
                        
                        # Save to temporary file
                        import tempfile
                        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
                        temp_file.write(content)
                        temp_file.close()
                        
                        # Print file
                        win32api.ShellExecute(
                            0,
                            "print",
                            temp_file.name,
                            f'/d:"{printer_name}"',
                            ".",
                            0
                        )
                        
                        messagebox.showinfo("Print", "Document sent to printer.")
                    except ImportError:
                        messagebox.showwarning(
                            "Print",
                            "Print functionality requires pywin32.\nInstall it with: pip install pywin32"
                        )
                else:
                    # For other platforms, use system print command
                    import tempfile
                    import subprocess
                    
                    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
                    temp_file.write(content)
                    temp_file.close()
                    
                    # Try to print using system command
                    try:
                        if sys.platform == "darwin":  # macOS
                            subprocess.run(["lpr", temp_file.name])
                        else:  # Linux
                            subprocess.run(["lp", temp_file.name])
                        messagebox.showinfo("Print", "Document sent to printer.")
                    except Exception as e:
                        messagebox.showerror("Print Error", f"Failed to print:\n{str(e)}")
                        
        except Exception as e:
            messagebox.showerror("Print Error", f"Failed to print:\n{str(e)}")
            
    def print_preview(self):
        """Show print preview (simplified - shows content in message box)."""
        content = self.editor.text_widget.get(1.0, tk.END + "-1c")
        
        # Create preview window
        preview = tk.Toplevel(self.editor.root)
        preview.title("Print Preview")
        preview.geometry("600x700")
        
        # Create text widget for preview
        from tkinter import scrolledtext
        preview_text = scrolledtext.ScrolledText(
            preview,
            wrap=tk.WORD,
            font=("Courier", 10)
        )
        preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        preview_text.insert(1.0, content)
        preview_text.config(state=tk.DISABLED)
        
        # Print button
        button_frame = tk.Frame(preview)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Print",
            command=lambda: [preview.destroy(), self.print_file()]
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Close",
            command=preview.destroy
        ).pack(side=tk.LEFT, padx=5)
        
    def export_as_pdf(self):
        """Export document as PDF."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.units import inch
            
            # Get content
            content = self.editor.text_widget.get(1.0, tk.END + "-1c")
            
            # Ask for save location
            filepath = filedialog.asksaveasfilename(
                title="Export as PDF",
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
            )
            
            if filepath:
                # Create PDF
                doc = SimpleDocTemplate(filepath, pagesize=letter)
                styles = getSampleStyleSheet()
                story = []
                
                # Split content into paragraphs
                paragraphs = content.split('\n')
                
                for para in paragraphs:
                    if para.strip():
                        p = Paragraph(para.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), styles['Normal'])
                        story.append(p)
                        story.append(Spacer(1, 0.2*inch))
                    else:
                        story.append(Spacer(1, 0.1*inch))
                        
                # Build PDF
                doc.build(story)
                
                messagebox.showinfo("Export PDF", f"Document exported successfully to:\n{filepath}")
                
        except ImportError:
            messagebox.showerror(
                "Export PDF",
                "PDF export requires reportlab.\nInstall it with: pip install reportlab"
            )
        except Exception as e:
            messagebox.showerror("Export PDF Error", f"Failed to export PDF:\n{str(e)}")

