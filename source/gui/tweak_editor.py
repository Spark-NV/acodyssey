import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from typing import Dict, Any, Optional, List
from pathlib import Path

from utils.settings_manager import get_settings_manager


class TweakEditor:
    def __init__(self, parent):
        self.parent = parent
        self.root = parent.root
        self.settings_manager = get_settings_manager()
        self.settings_dir = self.settings_manager.get_tweak_files_dir()
        self.settings_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_game_id = None
        self.current_tweak_data = {}
        self.editing_mode = None
        
    def show_editor(self):
        self.dialog = tk.Toplevel(self.parent.root)
        self.dialog.title("Tweak Editor")
        self.dialog.geometry("800x800")
        self.dialog.minsize(800, 800)
        self.dialog.resizable(True, True)
        self.dialog.transient(self.parent.root)
        self.dialog.grab_set()
        
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (800 // 2)
        self.dialog.geometry(f"800x800+{x}+{y}")
        
        self.dialog.bind_all("<MouseWheel>", self._on_mousewheel)
        
        self.create_main_interface()
        
    def create_main_interface(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        importer_frame = ttk.Frame(main_frame)
        importer_frame.pack(fill=tk.X, pady=(0, 30))
        
        importer_title = ttk.Label(importer_frame, text="Tweak Importer", font=("Arial", 16, "bold"))
        importer_title.pack(pady=(0, 20))
        
        import_btn = ttk.Button(importer_frame, text="Import Tweak Files", 
                               command=self.select_file_to_import, style='Help.TButton')
        import_btn.pack(pady=10, padx=20, fill=tk.X)
        
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=20)
        
        editor_frame = ttk.Frame(main_frame)
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        editor_title = ttk.Label(editor_frame, text="Tweak Editor", font=("Arial", 16, "bold"))
        editor_title.pack(pady=(0, 20))
        
        choice_frame = ttk.Frame(editor_frame)
        choice_frame.pack(expand=True)
        
        ttk.Label(choice_frame, text="What would you like to do?", font=("Arial", 12)).pack(pady=(0, 20))
        
        new_game_btn = ttk.Button(choice_frame, text="Add New Game", 
                                 command=self.create_new_game, style='Help.TButton')
        new_game_btn.pack(pady=10, padx=20, fill=tk.X)
        
        new_tweaks_btn = ttk.Button(choice_frame, text="Add Tweaks to Existing Game", 
                                   command=self.add_tweaks_to_game, style='Help.TButton')
        new_tweaks_btn.pack(pady=10, padx=20, fill=tk.X)
        
        edit_existing_btn = ttk.Button(choice_frame, text="Edit Existing Game", 
                                      command=self.edit_existing_game, style='Help.TButton')
        edit_existing_btn.pack(pady=10, padx=20, fill=tk.X)
        
        close_btn = ttk.Button(editor_frame, text="Close", command=self.close_editor)
        close_btn.pack(pady=(20, 0))
        
    def select_file_to_import(self):
        from utils.file_import_helper import import_tweak_file
        import_tweak_file(self.parent, self.settings_dir, self.parent.refresh_application)
        
    def create_new_game(self):
        self.editing_mode = 'new_game'
        self.clear_dialog()
        self.create_game_info_interface()
        
    def add_tweaks_to_game(self):
        self.editing_mode = 'new_tweaks'
        self.clear_dialog()
        self.create_game_selection_interface()
        
    def edit_existing_game(self):
        self.editing_mode = 'edit_game'
        self.clear_dialog()
        self.create_game_selection_interface()
        

        
    def clear_dialog(self):
        for widget in self.dialog.winfo_children():
            widget.destroy()
            
    def create_game_selection_interface(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_text = "Select Game" if self.editing_mode == 'new_tweaks' else "Edit Game"
        title_label = ttk.Label(main_frame, text=title_text, font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        ttk.Label(main_frame, text="Select a game:").pack(anchor=tk.W)
        
        self.game_var = tk.StringVar()
        game_combo = ttk.Combobox(main_frame, textvariable=self.game_var, state="readonly")
        game_combo.pack(fill=tk.X, pady=(5, 20))
        
        games = self.get_available_games()
        game_combo['values'] = [f"{game['name']} ({game_id})" for game_id, game in games.items()]
        
        if games:
            game_combo.current(0)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        if self.editing_mode == 'new_tweaks':
            continue_btn = ttk.Button(button_frame, text="Continue to Add Tweaks", 
                                    command=self.load_game_and_add_tweaks)
        else:
            continue_btn = ttk.Button(button_frame, text="Edit Game", 
                                    command=self.load_game_for_editing)
        
        continue_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        back_btn = ttk.Button(button_frame, text="Back", command=self.create_main_interface)
        back_btn.pack(side=tk.LEFT)
        
    def get_available_games(self) -> Dict[str, Dict[str, Any]]:
        games = {}
        
        for tweak_file in self.settings_dir.glob('*_tweaks.json'):
            try:
                with open(tweak_file, 'r') as f:
                    data = json.load(f)
                    if 'game_info' in data:
                        game_info = data['game_info']
                        game_id = game_info.get('game_id', tweak_file.stem.replace('_tweaks', ''))
                        games[game_id] = {
                            'name': game_info.get('name', 'Unknown Game'),
                            'source': 'settings',
                            'file_path': tweak_file
                        }
            except Exception as e:
                print(f"Error loading game {tweak_file}: {e}")
        
        return games
        
    def load_game_and_add_tweaks(self):
        selected = self.game_var.get()
        if not selected:
            messagebox.showerror("Error", "Please select a game")
            return
            
        game_id = selected.split('(')[-1].rstrip(')')
        self.current_game_id = game_id
        
        self.load_existing_tweak_data()
        
        self.clear_dialog()
        self.create_tweak_creation_interface()
        
    def load_game_for_editing(self):
        selected = self.game_var.get()
        if not selected:
            messagebox.showerror("Error", "Please select a game")
            return
            
        game_id = selected.split('(')[-1].rstrip(')')
        self.current_game_id = game_id
        
        self.load_existing_tweak_data()
        
        self.clear_dialog()
        self.create_game_editing_interface()
        
    def load_existing_tweak_data(self):
        self.current_tweak_data = {}
        
        tweak_file = self.settings_dir / f"{self.current_game_id}_tweaks.json"
        if tweak_file.exists():
            try:
                with open(tweak_file, 'r') as f:
                    self.current_tweak_data = json.load(f)
            except Exception as e:
                print(f"Error loading tweak file: {e}")
                
    def create_game_info_interface(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="New Game Information", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.game_info_vars = {}
        
        fields = [
            ("game_id", "Game ID (unique identifier):", "my_game"),
            ("name", "Full Game Name:", "My Game"),
            ("short_name", "Short Game Name:", "MyGame"),
            ("executable_name", "Executable Name:", "MyGame.exe"),
            ("steam_app_id", "Steam App ID (optional):", ""),
            ("nexus_mods_url", "Nexus Mods URL (optional):", ""),
            ("main_title", "Main Title:", "My Game Tweak Pack"),
            ("tweak_pack_version", "Tweak Pack Version:", "V1.0"),
            ("compatible_version", "Compatible Game Version:", "V1.0.0"),
            ("subtitle", "Subtitle:", "Compatible with My Game {compatible_version}")
        ]
        
        for field_id, label_text, default_value in fields:
            ttk.Label(scrollable_frame, text=label_text).pack(anchor=tk.W, pady=(10, 5))
            var = tk.StringVar(value=default_value)
            self.game_info_vars[field_id] = var
            entry = ttk.Entry(scrollable_frame, textvariable=var, width=50)
            entry.pack(fill=tk.X, pady=(0, 10))
        
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        continue_btn = ttk.Button(button_frame, text="Continue to Add Tweaks", 
                                command=self.save_game_info_and_continue)
        continue_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        back_btn = ttk.Button(button_frame, text="Back", command=self.create_main_interface)
        back_btn.pack(side=tk.LEFT)
        
    def save_game_info_and_continue(self):
        required_fields = ['game_id', 'name', 'short_name', 'executable_name']
        for field in required_fields:
            if not self.game_info_vars[field].get().strip():
                messagebox.showerror("Error", f"Please fill in the {field} field")
                return
        
        game_info = {}
        for field_id, var in self.game_info_vars.items():
            game_info[field_id] = var.get().strip()
        
        self.current_game_id = game_info['game_id']
        self.current_tweak_data = {
            'game_info': game_info
        }
        
        self.save_tweak_file(show_success=False, close_dialog=False)
        
        self.clear_dialog()
        self.create_tweak_creation_interface()
        
    def create_tweak_creation_interface(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        save_btn = ttk.Button(button_frame, text="Save All Changes", 
                             command=lambda: self.save_tweak_file(show_success=True, close_dialog=True))
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        add_tweak_btn = ttk.Button(button_frame, text="Add This Tweak", 
                                  command=self.add_current_tweak)
        add_tweak_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        back_btn = ttk.Button(button_frame, text="Back", command=self.create_main_interface)
        back_btn.pack(side=tk.LEFT)
        
        title_label = ttk.Label(main_frame, text="Add Tweaks", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        add_tweak_frame = ttk.Frame(notebook)
        notebook.add(add_tweak_frame, text="Add New Tweak")
        self.create_add_tweak_interface(add_tweak_frame)
        
        view_tweaks_frame = ttk.Frame(notebook)
        notebook.add(view_tweaks_frame, text="View All Tweaks")
        self.create_view_tweaks_interface(view_tweaks_frame)
        

        
    def create_add_tweak_interface(self, parent):
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.tweak_vars = {}
        
        field_configs = [
            ("name", "Tweak Name:", "My Tweak"),
            ("description", "Description:", "Description of what this tweak does, not shown to user"),
            ("type", "Type:", "bool"),
        ]
        
        for field_id, label_text, default_value in field_configs:
            field_frame = ttk.Frame(scrollable_frame)
            field_frame.pack(fill=tk.X, pady=(10, 0))
            
            label_frame = ttk.Frame(field_frame)
            label_frame.pack(fill=tk.X, pady=(0, 5))
            
            ttk.Label(label_frame, text=label_text).pack(side=tk.LEFT)
            
            help_btn = ttk.Button(label_frame, text="?", width=3,
                                 command=lambda f=field_id: self.show_field_help(f))
            help_btn.pack(side=tk.RIGHT, padx=(5, 0))
            
            if field_id == "type":
                var = tk.StringVar(value=default_value)
                self.tweak_vars[field_id] = var
                combo = ttk.Combobox(field_frame, textvariable=var, 
                                   values=["bool", "float", "int"], state="readonly")
                combo.set("bool")
                combo.pack(fill=tk.X, pady=(0, 10))
                
                combo.bind('<<ComboboxSelected>>', self.on_type_changed)
            elif field_id in ["description", "help"]:
                var = tk.StringVar(value=default_value)
                self.tweak_vars[field_id] = var
                text = tk.Text(field_frame, height=3, width=50)
                text.insert("1.0", default_value)
                text.pack(fill=tk.X, pady=(0, 10))
                self.tweak_vars[f"{field_id}_text"] = text
            else:
                var = tk.StringVar(value=default_value)
                self.tweak_vars[field_id] = var
                entry = ttk.Entry(field_frame, textvariable=var, width=50)
                entry.pack(fill=tk.X, pady=(0, 10))
        
        self.min_max_container = ttk.Frame(scrollable_frame)
        
        min_max_label_frame = ttk.Frame(self.min_max_container)
        min_max_label_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(min_max_label_frame, text="Min/Max Values:").pack(side=tk.LEFT)
        min_max_help_btn = ttk.Button(min_max_label_frame, text="?", width=3,
                                     command=lambda: self.show_field_help("min"))
        min_max_help_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        min_max_frame = ttk.Frame(self.min_max_container)
        min_max_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(min_max_frame, text="Min Value:").pack(side=tk.LEFT)
        self.min_var = tk.StringVar()
        ttk.Entry(min_max_frame, textvariable=self.min_var, width=10).pack(side=tk.LEFT, padx=(5, 20))
        
        ttk.Label(min_max_frame, text="Max Value:").pack(side=tk.LEFT)
        self.max_var = tk.StringVar()
        ttk.Entry(min_max_frame, textvariable=self.max_var, width=10).pack(side=tk.LEFT, padx=(5, 0))
        
        self.first_remaining_field = None
        
        remaining_fields = [
            ("originalByteArray", "Original Byte Array (hex):", "0x1234567890ABCDEF"),
            ("modifiedByteArray", "Modified Byte Array (hex):", "0xFEDCBA0987654321"),
            ("variableOffset", "Variable Offset:", "0"),
            ("help", "Help Text:", "Detailed help message for this tweak that is shown to user")
        ]
        
        for i, (field_id, label_text, default_value) in enumerate(remaining_fields):
            field_frame = ttk.Frame(scrollable_frame)
            field_frame.pack(fill=tk.X, pady=(10, 0))
            
            if i == 0:
                self.first_remaining_field = field_frame
            
            label_frame = ttk.Frame(field_frame)
            label_frame.pack(fill=tk.X, pady=(0, 5))
            
            ttk.Label(label_frame, text=label_text).pack(side=tk.LEFT)
            
            help_btn = ttk.Button(label_frame, text="?", width=3,
                                 command=lambda f=field_id: self.show_field_help(f))
            help_btn.pack(side=tk.RIGHT, padx=(5, 0))
            
            if field_id in ["description", "help"]:
                var = tk.StringVar(value=default_value)
                self.tweak_vars[field_id] = var
                text = tk.Text(field_frame, height=3, width=50)
                text.insert("1.0", default_value)
                text.pack(fill=tk.X, pady=(0, 10))
                self.tweak_vars[f"{field_id}_text"] = text
            else:
                var = tk.StringVar(value=default_value)
                self.tweak_vars[field_id] = var
                entry = ttk.Entry(field_frame, textvariable=var, width=50)
                entry.pack(fill=tk.X, pady=(0, 10))
        

        
        section_label_frame = ttk.Frame(scrollable_frame)
        section_label_frame.pack(fill=tk.X, pady=(10, 5))
        
        ttk.Label(section_label_frame, text="Section:").pack(side=tk.LEFT)
        section_help_btn = ttk.Button(section_label_frame, text="?", width=3,
                                     command=lambda: self.show_field_help("section"))
        section_help_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        section_frame = ttk.Frame(scrollable_frame)
        section_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.section_var = tk.StringVar(value="Player Mods")
        section_entry = ttk.Entry(section_frame, textvariable=self.section_var, width=35)
        section_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        existing_sections = self.get_existing_sections()
        if existing_sections:
            section_combo = ttk.Combobox(section_frame, values=existing_sections, width=15)
            section_combo.pack(side=tk.RIGHT, padx=(5, 0))
            section_combo.bind('<<ComboboxSelected>>', lambda e: self.section_var.set(section_combo.get()))
        
        group_label_frame = ttk.Frame(scrollable_frame)
        group_label_frame.pack(fill=tk.X, pady=(10, 5))
        
        ttk.Label(group_label_frame, text="Group:").pack(side=tk.LEFT)
        group_help_btn = ttk.Button(group_label_frame, text="?", width=3,
                                   command=lambda: self.show_field_help("group"))
        group_help_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        group_frame = ttk.Frame(scrollable_frame)
        group_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.group_var = tk.StringVar(value="my_tweak_group")
        group_entry = ttk.Entry(group_frame, textvariable=self.group_var, width=35)
        group_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        existing_groups = self.get_existing_groups()
        if existing_groups:
            group_combo = ttk.Combobox(group_frame, values=existing_groups, width=15)
            group_combo.pack(side=tk.RIGHT, padx=(5, 0))
            group_combo.bind('<<ComboboxSelected>>', lambda e: self.group_var.set(group_combo.get()))
        

        
        visible_label_frame = ttk.Frame(scrollable_frame)
        visible_label_frame.pack(fill=tk.X, pady=(10, 5))
        
        self.visible_var = tk.BooleanVar(value=True)
        visible_check = ttk.Checkbutton(visible_label_frame, text="Visible in GUI", 
                                       variable=self.visible_var)
        visible_check.pack(side=tk.LEFT)
        
        visible_help_btn = ttk.Button(visible_label_frame, text="?", width=3,
                                     command=lambda: self.show_field_help("visible"))
        visible_help_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Frame(scrollable_frame).pack(fill=tk.X, pady=(0, 20))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_field_help(self, field_name: str):
        help_texts = {
            "name": {
                "title": "Tweak Name",
                "description": "A short, descriptive name for this tweak that will be displayed in the main interface.",
                "hint": "Examples: 'Infinite Health', 'God Mode', 'Speed Boost'"
            },
            "description": {
                "title": "Description",
                "description": "A brief explanation of what this tweak does when enabled.",
                "hint": "Explain the effect for yourself later, this field isnt shown in the main interface."
            },
            "type": {
                "title": "Type",
                "description": "The data type that determines how this tweak behaves:",
                "details": [
                    "• bool: Simple on/off (Just finds and replaces bytes)",
                    "• int: Integer value that can be modified by user input",
                    "• float: Decimal value that can be modified by user input"
                ]
            },
            "originalByteArray": {
                "title": "Original Byte Array",
                "description": "The exact byte pattern to find in the game file before modification.",
                "hint": "Must be in hexadecimal format (e.g., 0x1234567890ABCDEF)"
            },
            "modifiedByteArray": {
                "title": "Modified Byte Array",
                "description": "The byte pattern that will replace the original pattern when the tweak is enabled.",
                "hint": "Must be in hexadecimal format and same length as original"
            },
            "variableOffset": {
                "title": "Variable Offset",
                "description": "Position within the modified byte array where user input values will be inserted.",
                "hint": "Use 0 for simple find-and-replace tweaks, or specify position for variable tweaks"
            },
            "help": {
                "title": "Help Text",
                "description": "Detailed help message shown when users click the help button for this tweak in the main interface.",
                "hint": "Provide detailed instructions, warnings, or additional information"
            },
            "section": {
                "title": "Section",
                "description": "The category/group this tweak will appear under in the main interface.",
                "hint": "Examples: 'Player Mods', 'Weapon Mods', 'Game Settings'"
            },
            "group": {
                "title": "Group",
                "description": "Links multiple tweaks together so they can be enabled/disabled as a unit.",
                "hint": "Use the same group name for related tweaks that should work together"
            },
            "min": {
                "title": "Min Value",
                "description": "Minimum allowed value for numeric tweaks (int/float types).",
                "hint": "Leave empty for no minimum limit"
            },
            "max": {
                "title": "Max Value",
                "description": "Maximum allowed value for numeric tweaks (int/float types).",
                "hint": "Leave empty for no maximum limit"
            },
            "visible": {
                "title": "Visible in GUI",
                "description": "Whether this tweak should be shown in the main interface.",
                "hint": "Uncheck to hide tweaks that are part of a group or secondary patches"
            }
        }
        
        if field_name not in help_texts:
            return
        
        help_info = help_texts[field_name]
        
        help_dialog = tk.Toplevel(self.dialog)
        help_dialog.title(f"Help: {help_info['title']}")
        help_dialog.geometry("500x400")
        help_dialog.resizable(True, True)
        help_dialog.transient(self.dialog)
        help_dialog.grab_set()
        
        help_dialog.update_idletasks()
        x = (help_dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (help_dialog.winfo_screenheight() // 2) - (400 // 2)
        help_dialog.geometry(f"500x400+{x}+{y}")
        
        main_frame = ttk.Frame(help_dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        title_label = ttk.Label(scrollable_frame, text=help_info['title'], 
                               font=("Arial", 14, "bold"))
        title_label.pack(anchor=tk.W, pady=(0, 15))
        
        desc_label = ttk.Label(scrollable_frame, text=help_info['description'], 
                              font=("Arial", 11), wraplength=450, justify=tk.LEFT)
        desc_label.pack(anchor=tk.W, pady=(0, 15))
        
        if 'details' in help_info:
            for detail in help_info['details']:
                detail_label = ttk.Label(scrollable_frame, text=detail, 
                                       font=("Arial", 10), wraplength=450, justify=tk.LEFT)
                detail_label.pack(anchor=tk.W, pady=(0, 5))
        
        if 'hint' in help_info:
            hint_frame = ttk.Frame(scrollable_frame)
            hint_frame.pack(fill=tk.X, pady=(15, 0))
            
            hint_label = ttk.Label(hint_frame, text="💡 Hint:", 
                                  font=("Arial", 10, "bold"), foreground="blue")
            hint_label.pack(anchor=tk.W)
            
            hint_text = ttk.Label(hint_frame, text=help_info['hint'], 
                                 font=("Arial", 10), wraplength=450, justify=tk.LEFT,
                                 foreground="blue")
            hint_text.pack(anchor=tk.W, pady=(5, 0))
        
        close_btn = ttk.Button(scrollable_frame, text="Close", 
                              command=help_dialog.destroy)
        close_btn.pack(pady=(20, 0))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        help_dialog.focus_set()
    
    def on_type_changed(self, event=None):
        selected_type = self.tweak_vars['type'].get()
        
        if selected_type in ['float', 'int']:
            if self.first_remaining_field:
                self.min_max_container.pack(fill=tk.X, pady=(0, 10), before=self.first_remaining_field)
            else:
                self.min_max_container.pack(fill=tk.X, pady=(0, 10))
        else:
            self.min_max_container.pack_forget()
        
    def add_current_tweak(self):
        required_fields = ['name', 'description', 'type', 'originalByteArray', 
                          'modifiedByteArray']
        for field in required_fields:
            if field in ['description', 'help']:
                text_widget = self.tweak_vars.get(f"{field}_text")
                if text_widget:
                    value = text_widget.get("1.0", tk.END).strip()
                else:
                    value = self.tweak_vars[field].get().strip()
            else:
                value = self.tweak_vars[field].get().strip()
            
            if not value:
                messagebox.showerror("Error", f"Please fill in the {field} field")
                return
        
        if not self.section_var.get().strip():
            messagebox.showerror("Error", "Please fill in the Section field")
            return
        
        if not self.group_var.get().strip():
            messagebox.showerror("Error", "Please fill in the Group field")
            return
        
        tweak_data = {}
        for field_id, var in self.tweak_vars.items():
            if field_id.endswith('_text'):
                continue
            if field_id in ['description', 'help']:
                text_widget = self.tweak_vars.get(f"{field_id}_text")
                if text_widget:
                    tweak_data[field_id] = text_widget.get("1.0", tk.END).strip()
                else:
                    tweak_data[field_id] = var.get().strip()
            else:
                tweak_data[field_id] = var.get().strip()
        
        tweak_data['section'] = self.section_var.get()
        tweak_data['group'] = self.group_var.get()
        
        if self.min_var.get().strip():
            try:
                tweak_data['min'] = float(self.min_var.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Min value must be a number")
                return
                
        if self.max_var.get().strip():
            try:
                tweak_data['max'] = float(self.max_var.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Max value must be a number")
                return
        
        tweak_data['visible'] = self.visible_var.get()
        
        try:
            tweak_data['variableOffset'] = int(tweak_data['variableOffset'])
        except ValueError:
            messagebox.showerror("Error", "Variable Offset must be a number")
            return
        
        total_tweaks = 0
        for category, category_tweaks in self.current_tweak_data.items():
            if category != 'game_info' and isinstance(category_tweaks, dict):
                total_tweaks += len(category_tweaks)
        tweak_id = f"tweak_{total_tweaks + 1}"
        
        section = tweak_data['section'].lower().replace(' ', '_')
        if section not in self.current_tweak_data:
            self.current_tweak_data[section] = {}
        
        self.current_tweak_data[section][tweak_id] = tweak_data
        
        messagebox.showinfo("Success", f"Tweak '{tweak_data['name']}' added successfully!")
        
        self.save_tweak_file(show_success=False, close_dialog=False)
        
        self.clear_tweak_form()
        self.refresh_tweak_creation_interface()
        
    def clear_tweak_form(self):
        for field_id, var in self.tweak_vars.items():
            if field_id.endswith('_text'):
                var.delete("1.0", tk.END)
                var.insert("1.0", "")
            else:
                var.set("")
        
        self.section_var.set("Player Mods")
        self.group_var.set("my_tweak_group")
        
        if hasattr(self, 'min_max_container'):
            self.min_max_container.pack_forget()
        
        self.min_var.set("")
        self.max_var.set("")
        self.visible_var.set(True)
        
    def create_view_tweaks_interface(self, parent):
        columns = ('Name', 'Type', 'Section', 'Group', 'Visible')
        tree = ttk.Treeview(parent, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        for category, category_tweaks in self.current_tweak_data.items():
            if category == 'game_info':
                continue
            if isinstance(category_tweaks, dict):
                for tweak_id, tweak_data in category_tweaks.items():
                    tree.insert('', 'end', values=(
                        tweak_data.get('name', 'Unknown'),
                        tweak_data.get('type', 'bool'),
                        tweak_data.get('section', 'Unknown'),
                        tweak_data.get('group', 'Unknown'),
                        'Yes' if tweak_data.get('visible', True) else 'No'
                    ))
        
    def create_game_editing_interface(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Edit Game Information", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.edit_game_info_vars = {}
        
        if 'game_info' in self.current_tweak_data:
            game_info = self.current_tweak_data['game_info']
        else:
            game_info = {}
        
        fields = [
            ("game_id", "Game ID:", game_info.get('game_id', '')),
            ("name", "Full Game Name:", game_info.get('name', '')),
            ("short_name", "Short Game Name:", game_info.get('short_name', '')),
            ("executable_name", "Executable Name:", game_info.get('executable_name', '')),
            ("steam_app_id", "Steam App ID:", game_info.get('steam_app_id', '')),
            ("nexus_mods_url", "Nexus Mods URL:", game_info.get('nexus_mods_url', '')),
            ("main_title", "Main Title:", game_info.get('main_title', '')),
            ("tweak_pack_version", "Tweak Pack Version:", game_info.get('tweak_pack_version', '')),
            ("compatible_version", "Compatible Game Version:", game_info.get('compatible_version', '')),
            ("subtitle", "Subtitle:", game_info.get('subtitle', ''))
        ]
        
        for field_id, label_text, current_value in fields:
            ttk.Label(scrollable_frame, text=label_text).pack(anchor=tk.W, pady=(10, 5))
            var = tk.StringVar(value=current_value)
            self.edit_game_info_vars[field_id] = var
            entry = ttk.Entry(scrollable_frame, textvariable=var, width=50)
            entry.pack(fill=tk.X, pady=(0, 10))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        save_btn = ttk.Button(button_frame, text="Save Changes", 
                             command=self.save_game_edits)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        back_btn = ttk.Button(button_frame, text="Back", command=self.create_main_interface)
        back_btn.pack(side=tk.LEFT)
        
    def save_game_edits(self):
        if 'game_info' not in self.current_tweak_data:
            self.current_tweak_data['game_info'] = {}
        
        for field_id, var in self.edit_game_info_vars.items():
            self.current_tweak_data['game_info'][field_id] = var.get().strip()
        
        self.save_tweak_file(show_success=False, close_dialog=False)
        
    def save_tweak_file(self, show_success=True, close_dialog=False):
        if not self.current_game_id:
            messagebox.showerror("Error", "No game selected")
            return
        
        if 'game_info' not in self.current_tweak_data:
            messagebox.showerror("Error", "No game information found")
            return
        
        file_path = self.settings_dir / f"{self.current_game_id}_tweaks.json"
        
        try:
            with open(file_path, 'w') as f:
                json.dump(self.current_tweak_data, f, indent=2)
            
            if show_success:
                messagebox.showinfo("Success", f"Tweak file saved successfully to:\n{file_path}")
            
            if close_dialog:
                self.close_editor()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tweak file:\n{str(e)}")
    
    def _on_mousewheel(self, event):
        for widget in self.dialog.winfo_children():
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Canvas):
                        child.yview_scroll(int(-1*(event.delta/120)), "units")
                        return
                    elif isinstance(child, ttk.Notebook):
                        for tab_id in child.tabs():
                            tab_widget = child.nametowidget(tab_id)
                            if hasattr(tab_widget, 'winfo_children'):
                                for tab_child in tab_widget.winfo_children():
                                    if isinstance(tab_child, tk.Canvas):
                                        tab_child.yview_scroll(int(-1*(event.delta/120)), "units")
                                        return
    
    def get_existing_sections(self) -> List[str]:
        sections = set()
        
        for category, category_tweaks in self.current_tweak_data.items():
            if category == 'game_info':
                continue
            if isinstance(category_tweaks, dict):
                for tweak_id, tweak_data in category_tweaks.items():
                    if isinstance(tweak_data, dict) and 'section' in tweak_data:
                        sections.add(tweak_data['section'])
        
        return sorted(list(sections))
    
    def get_existing_groups(self) -> List[str]:
        groups = set()
        
        for category, category_tweaks in self.current_tweak_data.items():
            if category == 'game_info':
                continue
            if isinstance(category_tweaks, dict):
                for tweak_id, tweak_data in category_tweaks.items():
                    if isinstance(tweak_data, dict) and 'group' in tweak_data:
                        groups.add(tweak_data['group'])
        
        return sorted(list(groups))
    
    def refresh_tweak_creation_interface(self):
        for widget in self.dialog.winfo_children():
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Notebook):
                        current_tab = child.select()
                        if current_tab:
                            tab_widget = child.nametowidget(current_tab)
                            for tab_child in tab_widget.winfo_children():
                                tab_child.destroy()
                            self.create_add_tweak_interface(tab_widget)
                        return
    
    def close_editor(self):
        self.dialog.unbind_all("<MouseWheel>")
        self.dialog.destroy()
        
        if hasattr(self.parent, 'refresh_application'):
            self.parent.refresh_application()
