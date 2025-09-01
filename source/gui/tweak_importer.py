import tkinter as tk
from tkinter import ttk


class TweakImporter:
    def __init__(self, parent):
        self.parent = parent
        self.dialog = None
        
        from utils.settings_manager import get_settings_manager
        self.settings_manager = get_settings_manager()
        self.settings_dir = self.settings_manager.get_tweak_files_dir()
    
    def show_importer(self):
        self.dialog = tk.Toplevel(self.parent.root)
        self.dialog.title("Tweak Importer")
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent.root)
        self.dialog.grab_set()
        
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (200 // 2)
        self.dialog.geometry(f"400x200+{x}+{y}")
        
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Tweak Importer", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 30))
        
        import_btn = ttk.Button(main_frame, text="Import Tweak Files", 
                               command=self.select_file_to_import, style='Help.TButton')
        import_btn.pack(pady=20, padx=20, fill=tk.X)
        
        close_btn = ttk.Button(main_frame, text="Close", command=self.close_importer)
        close_btn.pack(pady=(20, 0))
        
        self.dialog.focus_set()
        
    def select_file_to_import(self):
        from utils.file_import_helper import import_tweak_file
        import_tweak_file(self.parent, self.settings_dir, self.parent.refresh_application)
    
    def close_importer(self):
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
