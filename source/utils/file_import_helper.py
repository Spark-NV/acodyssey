import json
import shutil
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Optional, Callable


def import_tweak_file(parent, settings_dir: Path, on_success_callback: Optional[Callable] = None) -> bool:
    file_path = filedialog.askopenfilename(
        title="Select Tweak JSON File to Import",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        initialdir="."
    )
    
    if not file_path:
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'game_info' not in data:
            messagebox.showerror("Invalid File", 
                               "The selected file does not appear to be a valid tweak file.\n"
                               "It must contain a 'game_info' section.")
            return False
        
        game_id = data['game_info'].get('game_id', '')
        if not game_id:
            messagebox.showerror("Invalid File", 
                               "The selected file does not have a valid game_id in the game_info section.")
            return False
        
        target_file = settings_dir / f"{game_id}_tweaks.json"
        if target_file.exists():
            result = messagebox.askyesno("File Exists", 
                                       f"A tweak file for '{game_id}' already exists.\n"
                                       f"Would you like to overwrite it?")
            if not result:
                return False
        
        shutil.copy2(file_path, target_file)
        
        messagebox.showinfo("Import Successful", 
                          f"Successfully imported '{target_file}'.\n"
                          f"The tweaks are now available for use.")
        
        if on_success_callback:
            on_success_callback()
        
        return True
        
    except json.JSONDecodeError:
        messagebox.showerror("Invalid JSON", 
                           "The selected file is not a valid JSON file.")
        return False
    except Exception as e:
        messagebox.showerror("Import Error", 
                           f"An error occurred while importing the file:\n{str(e)}")
        return False
