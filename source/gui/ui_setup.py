import tkinter as tk
from tkinter import ttk
from typing import Dict, Any
import os

from config.settings import CURRENT_VERSION, GUI_STYLES, MAIN_WINDOW_SIZE, MAIN_WINDOW_MIN_SIZE, UI_TEXT, get_current_game_settings
from gui.components import CollapsibleSection
from gui.dialogs import FileSelectionDialog, NexusDialog


class UISetup:
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.root = main_window.root
        
        self.main_frame = None
        self.main_content_frame = None
        self.file_label = None
        self.status_label = None
        self.active_title = None
        self.active_tweaks_frame = None
        self.canvas = None
        self.scrollbar = None
        self.scrollable_frame = None
        self.info_button = None
        
        self.sections = {}
        self.status_vars = {}
        self.tweak_buttons = {}
        self.tweak_info = {}
    
    def setup_styles(self):
        style = ttk.Style()
        
        for style_name, style_config in GUI_STYLES.items():
            style.configure(style_name, **style_config)
    
    def setup_ui(self):
        self.container_frame = ttk.Frame(self.root)
        self.container_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.main_frame = ttk.Frame(self.container_frame, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.container_frame.columnconfigure(0, weight=1)
        self.container_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        self.setup_header()
        self.setup_file_status()
        self.setup_main_content()
        self.setup_bottom_buttons()
        
        self.main_frame.rowconfigure(4, weight=1)
    
    def setup_header(self):
        current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        game_settings = get_current_game_settings(current_game_id)
        title_text = f"{game_settings.get('main_title', 'Game Tweak Pack')} {game_settings.get('tweak_pack_version', 'V1.0')}"
        
        self.title_label = tk.Label(self.main_frame, text=title_text, 
                                   font=("Arial", 16, "bold"), fg="blue", cursor="hand2")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        self.title_label.bind("<Button-1>", self.open_nexus_page)
        self.title_label.bind("<Enter>", lambda e: self.title_label.config(fg="purple"))
        self.title_label.bind("<Leave>", lambda e: self.title_label.config(fg="blue"))
        
        self.subtitle_label = ttk.Label(self.main_frame, text="", font=("Arial", 10))
        self.subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 5))
        self.update_game_info()
    
    def setup_file_status(self):
        self.file_label = ttk.Label(self.main_frame, text="Searching for game executable...", 
                                   foreground="blue", font=("Arial", 9), cursor="hand2")
        self.file_label.grid(row=2, column=0, columnspan=3, pady=(0, 20))
        self.file_label.bind("<Button-1>", self.on_file_label_click)
        
        self.status_label = ttk.Label(self.main_frame, text="Available Tweaks", 
                                      font=("Arial", 14, "bold"))
        self.status_label.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
    
    def setup_main_content(self):
        self.main_content_frame = ttk.Frame(self.main_frame)
        self.main_content_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        left_panel = ttk.Frame(self.main_content_frame, relief="flat", borderwidth=0)
        left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=(0, 5))
        
        self.setup_scrollable_tweaks(left_panel)
        
        right_panel = ttk.Frame(self.main_content_frame)
        right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=(5, 0))
        
        right_panel.rowconfigure(1, weight=1)
        right_panel.columnconfigure(0, weight=1)
        
        self.active_title = ttk.Label(right_panel, text="Active Tweaks (0)", font=("Arial", 14, "bold"))
        self.active_title.grid(row=0, column=0, pady=(0, 10))
        
        self.active_tweaks_frame = ttk.Frame(right_panel)
        self.active_tweaks_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.main_content_frame.columnconfigure(0, weight=3)
        self.main_content_frame.columnconfigure(1, weight=2)
        self.main_content_frame.rowconfigure(0, weight=1)
    
    def setup_scrollable_tweaks(self, parent):
        self.canvas = tk.Canvas(parent, highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def setup_bottom_buttons(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)
        
        left_buttons = ttk.Frame(button_frame)
        left_buttons.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(left_buttons, text="Run Game", style='Large.TButton', 
                  command=self.main_window.run_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(left_buttons, text="Create Backup", style='Large.TButton', 
                  command=self.main_window.create_backup).pack(side=tk.LEFT, padx=5)
        ttk.Button(left_buttons, text="Restore Backup", style='Large.TButton', 
                  command=self.main_window.restore_backup).pack(side=tk.LEFT, padx=5)
        ttk.Button(left_buttons, text="Disable All", style='Large.TButton', 
                  command=self.main_window.disable_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(left_buttons, text="Refresh Status", style='Large.TButton', 
                  command=self.main_window.refresh_status).pack(side=tk.LEFT, padx=5)
        ttk.Button(left_buttons, text="Add/Edit Games", style='Large.TButton', 
                  command=self.main_window.show_tweak_editor).pack(side=tk.LEFT, padx=5)
        
        self.info_button = ttk.Button(button_frame, text="ℹ Info", style='Large.TButton', 
                                     command=self.main_window.toggle_info_overlay)
        self.info_button.pack(side=tk.RIGHT, padx=5)
    
    def clear_tweak_sections(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.sections.clear()
        self.status_vars.clear()
        self.tweak_buttons.clear()
        self.tweak_info.clear()
    
    def create_tweak_sections(self):
        if not self.main_window.file_name:
            self.show_no_executable_message()
            return
        
        from core.tweak_manager import load_tweak_definitions
        
        current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        tweak_defs = load_tweak_definitions(current_game_id)
        
        sections_data = {}
        for category, category_tweaks in tweak_defs.items():
            if category == 'game_info':
                continue
            if isinstance(category_tweaks, dict):
                for tweak_id, tweak_data in category_tweaks.items():
                    if isinstance(tweak_data, dict):
                        section_name = tweak_data.get('section', 'Other')
                        
                        is_visible = tweak_data.get('visible', False)
                        has_group = 'group' in tweak_data
                        
                        if not has_group or is_visible:
                            if section_name not in sections_data:
                                sections_data[section_name] = []
                            
                            tweak_config = [tweak_id, tweak_data['name'], tweak_data['type']]
                            
                            if 'min' in tweak_data:
                                tweak_config.append(tweak_data['min'])
                            if 'max' in tweak_data:
                                tweak_config.append(tweak_data['max'])
                            
                            sections_data[section_name].append(tuple(tweak_config))
        
        for section_title, tweaks_list in sections_data.items():
            section = CollapsibleSection(self.scrollable_frame, section_title, tweaks_list)
            self.sections[section_title] = section
            
            widgets = section.get_widgets()
            for tweak_name, widget_data in widgets.items():
                self.status_vars[tweak_name] = widget_data["status_var"]
                self.tweak_buttons[tweak_name] = {
                    "enable": widget_data["enable_btn"],
                    "disable": widget_data["disable_btn"]
                }
                self.tweak_info[tweak_name] = {
                    "type": widget_data["type"],
                    "min": widget_data.get("min"),
                    "max": widget_data.get("max")
                }
                
                widget_data["enable_btn"].config(command=lambda name=tweak_name: self.main_window.enable_tweak(name))
                widget_data["disable_btn"].config(command=lambda name=tweak_name: self.main_window.disable_tweak(name))
                widget_data["help_btn"].config(command=lambda name=tweak_name: self.main_window.show_help(name))
    
    def show_no_executable_message(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        message_frame = ttk.Frame(self.scrollable_frame)
        message_frame.pack(fill=tk.BOTH, expand=True, pady=50)
        
        current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        game_settings = get_current_game_settings(current_game_id)
        executable_name = game_settings.get('executable_name', 'game.exe')
        
        main_message = f"⚠️  Game Executable Not Found\n\n"
        main_message += f"To use tweaks for this game, you need to select the game executable file.\n\n"
        main_message += f"Expected file: {executable_name}\n\n"
        
        message_label = ttk.Label(message_frame, text=main_message, 
                                 font=("Arial", 12), 
                                 foreground="orange",
                                 justify=tk.CENTER,
                                 wraplength=400)
        message_label.pack(pady=20)
        
        info_text = "Once you select the correct executable file, the tweak options will appear here."
        info_label = ttk.Label(message_frame, text=info_text,
                              font=("Arial", 10),
                              foreground="gray",
                              justify=tk.CENTER,
                              wraplength=400)
        info_label.pack(pady=10)
    
    def show_no_executable_active_message(self):
        message_frame = ttk.Frame(self.active_tweaks_frame)
        message_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        message_text = "No active tweaks\n\nSelect a game executable to enable tweaks"
        
        message_label = ttk.Label(message_frame, text=message_text,
                                 font=("Arial", 11),
                                 foreground="gray",
                                 justify=tk.CENTER,
                                 wraplength=300)
        message_label.pack(pady=20)
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def update_active_tweaks_display(self):
        for widget in self.active_tweaks_frame.winfo_children():
            widget.destroy()
        
        if not self.main_window.file_name:
            self.show_no_executable_active_message()
            return
        
        active_tweaks = []
        
        from core.tweak_manager import GameModification, load_tweak_definitions
        

        current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        tweak_defs = load_tweak_definitions(current_game_id)
        

        active_tweaks_by_group = {}
        individual_active_tweaks = []
        
        for tweak_name, tweak in self.main_window.tweaks.items():
            if isinstance(tweak, GameModification) and tweak.status == 'Active':

                current_group = None
                for category, category_tweaks in tweak_defs.items():
                    if isinstance(category_tweaks, dict) and tweak_name in category_tweaks:
                        current_group = category_tweaks[tweak_name].get('group')
                        break
                
                if current_group:
                    if current_group not in active_tweaks_by_group:
                        active_tweaks_by_group[current_group] = []
                    active_tweaks_by_group[current_group].append(tweak_name)
                else:
                    individual_active_tweaks.append(tweak_name)
        

        for group_name, group_tweaks in active_tweaks_by_group.items():

            main_tweak_name = None
            for category, category_tweaks in tweak_defs.items():
                if category == 'game_info':
                    continue
                if isinstance(category_tweaks, dict):
                    for group_tweak_name, group_tweak_data in category_tweaks.items():
                        if (group_tweak_data.get('group') == group_name and 
                            group_tweak_data.get('visible', False)):
                            main_tweak_name = group_tweak_name
                            break
                    if main_tweak_name:
                        break
            
            if main_tweak_name:
                display_name = self.get_display_name(main_tweak_name)
                

                value = ""
                if main_tweak_name in self.tweak_info:
                    tweak_info = self.tweak_info[main_tweak_name]
                    if tweak_info.get("type") in ["float", "int"]:
    
                        for active_tweak_name in group_tweaks:
                            if active_tweak_name in self.main_window.tweaks:
                                active_tweak = self.main_window.tweaks[active_tweak_name]
                                if hasattr(active_tweak, 'statustext') and active_tweak.statustext:
                                    import re
                                    match = re.search(r'\(([^)]+)\)', active_tweak.statustext)
                                    if match:
                                        value = f" = {match.group(1)}"
                                        break
                
                active_tweaks.append((display_name, value))
        

        for tweak_name in individual_active_tweaks:

            should_hide = self.should_hide_from_active_list(tweak_name, tweak_defs)
            if should_hide:
                continue
            
            display_name = self.get_display_name(tweak_name)
            
            value = ""
            if tweak_name in self.tweak_info:
                tweak_info = self.tweak_info[tweak_name]
                if tweak_info.get("type") in ["float", "int"]:
                    if hasattr(tweak, 'statustext') and tweak.statustext:
                        import re
                        match = re.search(r'\(([^)]+)\)', tweak.statustext)
                        if match:
                            value = f" = {match.group(1)}"
            
            active_tweaks.append((display_name, value))
        
        self.active_title.config(text=f"Active Tweaks ({len(active_tweaks)})")
        
        if not active_tweaks:
            no_tweaks_label = ttk.Label(self.active_tweaks_frame, text="No tweaks active", 
                                       font=("Arial", 15, "bold"), foreground="gray")
            no_tweaks_label.pack(pady=(20, 5))
            
            help_label = ttk.Label(self.active_tweaks_frame, text="Enable one using options to the left", 
                                   font=("Arial", 12), foreground="gray")
            help_label.pack()
        else:
            self.create_active_tweaks_list(active_tweaks)
    
    def create_active_tweaks_list(self, active_tweaks: list):
        active_canvas = tk.Canvas(self.active_tweaks_frame, height=300)
        active_scrollbar = ttk.Scrollbar(self.active_tweaks_frame, orient="vertical", command=active_canvas.yview)
        active_content_frame = ttk.Frame(active_canvas)
        
        active_content_frame.bind(
            "<Configure>",
            lambda e: active_canvas.configure(scrollregion=active_canvas.bbox("all"))
        )
        
        active_canvas.create_window((0, 0), window=active_content_frame, anchor="nw")
        active_canvas.configure(yscrollcommand=active_scrollbar.set)
        
        active_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        active_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        for i, (display_name, value) in enumerate(active_tweaks):
            tweak_frame = ttk.Frame(active_content_frame)
            tweak_frame.pack(fill=tk.X, padx=5, pady=2)
            
            name_label = ttk.Label(tweak_frame, text=display_name, font=("Arial", 12, "bold"))
            name_label.pack(anchor=tk.W)
            
            if value:
                value_label = ttk.Label(tweak_frame, text=value, font=("Arial", 11), foreground="blue")
                value_label.pack(anchor=tk.W, padx=(10, 0))
            
            if i < len(active_tweaks) - 1:
                separator = ttk.Separator(tweak_frame, orient='horizontal')
                separator.pack(fill=tk.X, pady=5)
    
    def should_hide_from_active_list(self, tweak_name: str, tweak_defs: Dict) -> bool:
        for category, category_tweaks in tweak_defs.items():
            if category == 'game_info':
                continue
            if isinstance(category_tweaks, dict) and tweak_name in category_tweaks:
                tweak_data = category_tweaks[tweak_name]
                if isinstance(tweak_data, dict):
            
                    if not tweak_data.get('visible', False):
                        return True
                    
            
                    if tweak_data.get('bounds_logic') == 'disable_lower_bound':
                        return True
                    
            
                    if tweak_name.endswith('2') or tweak_name.endswith('Patch 2'):
                        return True
        
        return False
    
    def get_main_tweak_display_name(self, tweak_name: str) -> str:
        from core.tweak_manager import load_tweak_definitions
        
        current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        tweak_defs = load_tweak_definitions(current_game_id)
        

        current_group = None
        for category, category_tweaks in tweak_defs.items():
            if category == 'game_info':
                continue
            if isinstance(category_tweaks, dict) and tweak_name in category_tweaks:
                current_group = category_tweaks[tweak_name].get('group')
                break
        
        if current_group:

            for category, category_tweaks in tweak_defs.items():
                if category == 'game_info':
                    continue
                if isinstance(category_tweaks, dict):
                    for group_tweak_name, group_tweak_data in category_tweaks.items():
                        if (group_tweak_data.get('group') == current_group and 
                            group_tweak_data.get('visible', False)):
                            return group_tweak_data.get('name', group_tweak_name)
        

        return self.get_display_name(tweak_name)
    
    def get_display_name(self, tweak_name: str) -> str:
        from core.tweak_manager import load_tweak_definitions
        
        try:
            current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
            tweak_defs = load_tweak_definitions(current_game_id)
            
            for category, category_tweaks in tweak_defs.items():
                if category == 'game_info':
                    continue
                if isinstance(category_tweaks, dict) and tweak_name in category_tweaks:
                    tweak_data = category_tweaks[tweak_name]
                    if isinstance(tweak_data, dict) and 'name' in tweak_data:
                        return tweak_data['name']
            
            return tweak_name
            
        except Exception:
            return tweak_name
    
    def update_game_info(self, game_id: str = None):
        if game_id is None:
            game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        
        game_settings = get_current_game_settings(game_id)
        
        if hasattr(self, 'title_label') and self.title_label is not None:
            title_text = f"{game_settings.get('main_title', 'Game Tweak Pack')} {game_settings.get('tweak_pack_version', 'V1.0')}"
            self.title_label.config(text=title_text)
        
        if hasattr(self, 'subtitle_label') and self.subtitle_label is not None:
            subtitle_text = game_settings.get('subtitle', 'Compatible with {game_name} {compatible_version}').format(
                game_name=game_settings.get('name', 'Unknown Game'),
                compatible_version=game_settings.get('compatible_version', 'V1.0.0')
            )
            self.subtitle_label.config(text=subtitle_text)
        
        if hasattr(self, 'file_label') and self.file_label is not None:
            if not self.main_window.file_name:
                executable_name = game_settings.get('executable_name', 'game.exe')
                self.file_label.config(text=f"Couldn't automatically find {executable_name}, please click me to find it manually.", foreground="red")
    
    def on_file_label_click(self, event=None):
        self.main_window.file_operations.prompt_for_file()
    
    def open_nexus_page(self, event=None):
        current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        NexusDialog.open_nexus_page(current_game_id)
