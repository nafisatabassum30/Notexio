"""
Tools and statistics for Notexio text editor.
"""
import tkinter as tk
from tkinter import messagebox
import re


class Tools:
    """Manages tools and statistics."""
    
    def __init__(self, editor):
        self.editor = editor
        
    def get_word_count(self):
        """Get word count."""
        content = self.editor.text_widget.get(1.0, tk.END + "-1c")
        words = content.split()
        return len(words)
        
    def get_character_count(self, include_spaces=True):
        """Get character count."""
        content = self.editor.text_widget.get(1.0, tk.END + "-1c")
        if include_spaces:
            return len(content)
        else:
            return len(content.replace(" ", "").replace("\n", "").replace("\t", ""))
            
    def get_line_count(self):
        """Get line count."""
        content = self.editor.text_widget.get(1.0, tk.END)
        return len(content.split("\n"))
        
    def get_reading_time(self):
        """Estimate reading time in minutes."""
        word_count = self.get_word_count()
        # Average reading speed: 200-250 words per minute
        # Using 225 as average
        minutes = word_count / 225.0
        if minutes < 1:
            return f"{int(minutes * 60)} seconds"
        else:
            return f"{minutes:.1f} minutes"
            
    def show_statistics(self):
        """Show document statistics."""
        word_count = self.get_word_count()
        char_count_with_spaces = self.get_character_count(include_spaces=True)
        char_count_without_spaces = self.get_character_count(include_spaces=False)
        line_count = self.get_line_count()
        reading_time = self.get_reading_time()
        
        stats = f"""Document Statistics:

Words: {word_count:,}
Characters (with spaces): {char_count_with_spaces:,}
Characters (without spaces): {char_count_without_spaces:,}
Lines: {line_count:,}
Reading time: {reading_time}"""
        
        messagebox.showinfo("Document Statistics", stats)
        
    def highlight_duplicate_words(self):
        """Highlight duplicate words in the document."""
        content = self.editor.text_widget.get(1.0, tk.END + "-1c")
        
        # Find all words
        words = re.findall(r'\b\w+\b', content.lower())
        
        # Count word occurrences
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
            
        # Find duplicates (words that appear more than once)
        duplicates = {word: count for word, count in word_count.items() if count > 1}
        
        if not duplicates:
            messagebox.showinfo("Duplicate Words", "No duplicate words found.")
            return
            
        # Highlight duplicates
        self.editor.text_widget.tag_remove("duplicate", 1.0, tk.END)
        self.editor.text_widget.tag_config("duplicate", background="#FFFF00")
        
        # Find and highlight all occurrences of duplicate words
        content_lower = content.lower()
        for word in duplicates.keys():
            pattern = r'\b' + re.escape(word) + r'\b'
            for match in re.finditer(pattern, content_lower):
                start_pos = f"1.0 + {match.start()} chars"
                end_pos = f"1.0 + {match.end()} chars"
                self.editor.text_widget.tag_add("duplicate", start_pos, end_pos)
                
        messagebox.showinfo(
            "Duplicate Words",
            f"Found {len(duplicates)} duplicate word(s). Highlighted in yellow."
        )
        
    def remove_duplicate_highlights(self):
        """Remove duplicate word highlights."""
        self.editor.text_widget.tag_remove("duplicate", 1.0, tk.END)
        
    def remove_extra_spaces(self):
        """Remove extra spaces from document."""
        content = self.editor.text_widget.get(1.0, tk.END + "-1c")
        
        # Remove multiple spaces, but preserve single spaces
        content_new = re.sub(r' +', ' ', content)
        # Remove spaces at start of lines
        content_new = re.sub(r'\n +', '\n', content_new)
        # Remove trailing spaces
        content_new = re.sub(r' +\n', '\n', content_new)
        
        if content_new != content:
            self.editor.text_widget.delete(1.0, tk.END)
            self.editor.text_widget.insert(1.0, content_new)
            messagebox.showinfo("Remove Extra Spaces", "Extra spaces removed.")
        else:
            messagebox.showinfo("Remove Extra Spaces", "No extra spaces found.")

