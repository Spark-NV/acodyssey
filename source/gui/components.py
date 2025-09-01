import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional, Callable, List

from config.settings import FONT_CONFIG, DIALOG_DIMENSIONS


class CollapsibleSection:
    def __init__(self, parent, title: str, tweaks_list: List):
        self.parent = parent
        self.title = title
        self.tweaks_list = tweaks_list
        self.expanded = False
        self.widgets = {}
        
        self.create_section()
    
    def create_section(self):
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.header_frame = ttk.Frame(self.frame)
        self.header_frame.pack(fill=tk.X)
        
        self.toggle_button = ttk.Button(
            self.header_frame, 
            text=f"▶ {self.title}", 
            command=self.toggle,
            style='Help.TButton'
        )
        self.toggle_button.pack(side=tk.LEFT, anchor=tk.W)
        
        self.content_frame = ttk.Frame(self.frame)
        
        self.create_tweak_widgets()
    
    def create_tweak_widgets(self):
        for tweak_config in self.tweaks_list:
            tweak_id, tweak_name, tweak_type = tweak_config[0], tweak_config[1], tweak_config[2]
            
            tweak_frame = ttk.Frame(self.content_frame)
            tweak_frame.pack(fill=tk.X, padx=10, pady=2)
            
            name_label = ttk.Label(tweak_frame, text=tweak_name, font=FONT_CONFIG['tweak_name'])
            name_label.pack(anchor=tk.W)
            
            status_var = tk.StringVar(value="Unknown")
            status_label = ttk.Label(tweak_frame, textvariable=status_var, font=FONT_CONFIG['status'])
            status_label.pack(anchor=tk.W, padx=(20, 0))
            
            button_frame = ttk.Frame(tweak_frame)
            button_frame.pack(anchor=tk.W, padx=(20, 0), pady=(5, 0))
            
            enable_btn = ttk.Button(button_frame, text="Enable", style='Help.TButton')
            enable_btn.pack(side=tk.LEFT, padx=(0, 5))
            
            disable_btn = ttk.Button(button_frame, text="Disable", style='Help.TButton')
            disable_btn.pack(side=tk.LEFT, padx=(0, 5))
            
            help_btn = ttk.Button(button_frame, text="?", style='Help.TButton')
            help_btn.pack(side=tk.LEFT)
            
            self.widgets[tweak_id] = {
                "status_var": status_var,
                "status_label": status_label,
                "enable_btn": enable_btn,
                "disable_btn": disable_btn,
                "help_btn": help_btn,
                "type": tweak_type
            }
            
            if len(tweak_config) > 3:
                self.widgets[tweak_id]["min"] = tweak_config[3]
            if len(tweak_config) > 4:
                self.widgets[tweak_id]["max"] = tweak_config[4]
    
    def toggle(self):
        if self.expanded:
            self.content_frame.pack_forget()
            self.toggle_button.config(text=f"▶ {self.title}")
            self.expanded = False
        else:
            self.content_frame.pack(fill=tk.X, pady=(5, 0))
            self.toggle_button.config(text=f"▼ {self.title}")
            self.expanded = True
    
    def get_widgets(self):
        return self.widgets


class GameSelector:
    def __init__(self, parent, on_game_changed: Callable[[str], None]):
        self.parent = parent
        self.on_game_changed = on_game_changed
        self.current_game_id = None
        
        self.create_selector()
    
    def create_selector(self):
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.X, padx=5, pady=5)
        
        from config.settings import UI_TEXT
        label = ttk.Label(self.frame, text=UI_TEXT['game_selector_label'], font=FONT_CONFIG['section'])
        label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.game_var = tk.StringVar()
        self.combobox = ttk.Combobox(
            self.frame, 
            textvariable=self.game_var,
            state="readonly",
            font=FONT_CONFIG['button']
        )
        self.combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.combobox.bind('<<ComboboxSelected>>', self.on_selection_changed)
        
        self.load_games()
    
    def load_games(self):
        from config.game_config import get_game_configs
        
        game_configs = get_game_configs()
        game_names = []
        self.game_ids = []
        default_game_id = None
        
        for game_id, config in game_configs.items():
            game_names.append(config['name'])
            self.game_ids.append(game_id)
            if config.get('default', False):
                default_game_id = game_id
        
        self.combobox['values'] = game_names
        
        if game_names:
            if default_game_id and default_game_id in self.game_ids:
                index = self.game_ids.index(default_game_id)
                self.combobox.current(index)
                self.current_game_id = default_game_id
                self.game_var.set(game_names[index])
            else:
                self.combobox.current(0)
                self.current_game_id = self.game_ids[0]
                self.game_var.set(game_names[0])
    
    def on_selection_changed(self, event=None):
        selected_index = self.combobox.current()
        if selected_index >= 0 and selected_index < len(self.game_ids):
            new_game_id = self.game_ids[selected_index]
            if new_game_id != self.current_game_id:
                self.current_game_id = new_game_id
                self.on_game_changed(new_game_id)
    
    def get_current_game_id(self):
        return self.current_game_id
    
    def set_current_game(self, game_id: str):
        if game_id in self.game_ids:
            index = self.game_ids.index(game_id)
            self.combobox.current(index)
            self.current_game_id = game_id
    
    def refresh_games(self):
        current_selection = self.current_game_id
        
        self.load_games()
        
        if current_selection and current_selection in self.game_ids:
            self.set_current_game(current_selection)


class LoadingDialog:
    def __init__(self, parent, title: str, message: str, width: int, height: int):
        self.parent = parent
        self.title = title
        self.message = message
        self.width = width
        self.height = height
        
        self.create_dialog()
    
    def create_dialog(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.geometry(f"{self.width}x{self.height}")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.height // 2)
        self.dialog.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.message_label = ttk.Label(main_frame, text=self.message, font=FONT_CONFIG['info'])
        self.message_label.pack(pady=(0, 10))
        
        self.progress_label = ttk.Label(main_frame, text="", font=FONT_CONFIG['text'])
        self.progress_label.pack(pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        cancel_button = ttk.Button(main_frame, text="Cancel", command=self.close)
        cancel_button.pack()
        
        self.dialog.protocol("WM_DELETE_WINDOW", self.close)
        self.dialog.focus_set()
    
    def update_progress(self, current: int, total: int, message: str = None):
        if message:
            self.progress_label.config(text=message)
        
        progress = (current / total) * 100 if total > 0 else 0
        self.progress_bar['value'] = progress
        self.dialog.update()
    
    def set_message(self, message: str):
        self.message_label.config(text=message)
        self.dialog.update()
    
    def close(self):
        if hasattr(self, 'dialog'):
            self.dialog.destroy()


class ValueInputDialog:
    def __init__(self, parent, title: str, description: str, value_type: str, min_val=None, max_val=None):
        self.parent = parent
        self.title = title
        self.description = description
        self.value_type = value_type
        self.min_val = min_val
        self.max_val = max_val
        self.result = {"cancelled": True, "value": None}
        
        self.create_dialog()
    
    def create_dialog(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)
        self.dialog.geometry(DIALOG_DIMENSIONS['value_input'])
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (int(DIALOG_DIMENSIONS['value_input'].split('x')[0]) // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (int(DIALOG_DIMENSIONS['value_input'].split('x')[1]) // 2)
        self.dialog.geometry(f"{DIALOG_DIMENSIONS['value_input']}+{x}+{y}")
        
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        desc_label = ttk.Label(main_frame, text=self.description, font=FONT_CONFIG['text'], wraplength=350)
        desc_label.pack(pady=(0, 15))
        
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(input_frame, text="Value:", font=FONT_CONFIG['button']).pack(side=tk.LEFT, padx=(0, 10))
        
        self.value_var = tk.StringVar()
        self.entry = ttk.Entry(input_frame, textvariable=self.value_var, font=FONT_CONFIG['button'])
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.focus_set()
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        from config.settings import UI_TEXT
        ok_button = ttk.Button(button_frame, text=UI_TEXT['ok_button'], command=self.ok_clicked)
        ok_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        cancel_button = ttk.Button(button_frame, text=UI_TEXT['cancel_button'], command=self.cancel_clicked)
        cancel_button.pack(side=tk.RIGHT)
        
        self.entry.bind('<Return>', lambda e: self.ok_clicked())
        self.entry.bind('<Escape>', lambda e: self.cancel_clicked())
        
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel_clicked)
        
        self.dialog.wait_window()
    
    def ok_clicked(self):
        try:
            value_str = self.value_var.get().strip()
            if not value_str:
                return
            
            if self.value_type == "float":
                value = float(value_str)
            elif self.value_type == "int":
                value = int(value_str)
            else:
                value = value_str
            
            if self.min_val is not None and value < self.min_val:
                return
            if self.max_val is not None and value > self.max_val:
                return
            
            self.result = {"cancelled": False, "value": value}
            self.dialog.destroy()
            
        except ValueError:
            pass
    
    def cancel_clicked(self):
        self.dialog.destroy()
    
    def get_result(self):
        return self.result
