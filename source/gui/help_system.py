import tkinter as tk
from tkinter import ttk

from config.settings import CURRENT_VERSION, UI_TEXT, get_current_game_settings


class HelpSystem:
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.root = main_window.root
        
        self.help_frame = None
        self.help_active = False
    
    def show_help(self, tweak_name: str):
        from core.tweak_manager import load_tweak_definitions
        
        current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        tweak_defs = load_tweak_definitions(current_game_id)
        
        help_message = "No help available for this tweak."
        target_tweak_name = tweak_name
        
        current_group = None
        for category, category_tweaks in tweak_defs.items():
            if isinstance(category_tweaks, dict) and tweak_name in category_tweaks:
                current_tweak = category_tweaks[tweak_name]
                current_group = current_tweak.get('group')
                if 'help' in current_tweak:
                    help_message = current_tweak['help']
                    break
                break
        
        if help_message == "No help available for this tweak." and current_group:
            for category, category_tweaks in tweak_defs.items():
                if category == 'game_info':
                    continue
                if isinstance(category_tweaks, dict):
                    for group_tweak_name, group_tweak_data in category_tweaks.items():
                        if (group_tweak_data.get('group') == current_group and 
                            'help' in group_tweak_data):
                            help_message = group_tweak_data['help']
                            target_tweak_name = group_tweak_name
                            break
                    if help_message != "No help available for this tweak.":
                        break
        
        help_text = help_message
        
        self.show_help_overlay(tweak_name, help_text)
    
    def show_help_overlay(self, tweak_name: str, help_text: str):
        if self.help_active and self.help_frame:
            self.help_frame.destroy()
            self.help_frame = None
        
        self.main_window.ui_setup.active_tweaks_frame.grid_remove()
        
        self.help_frame = ttk.Frame(self.main_window.ui_setup.active_tweaks_frame.master)
        self.help_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.help_frame.columnconfigure(0, weight=1)
        self.help_frame.rowconfigure(1, weight=1)
        
        header_frame = ttk.Frame(self.help_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        close_button = ttk.Button(header_frame, text=UI_TEXT['close_help'], 
                                command=self.hide_help_overlay, style='Large.TButton')
        close_button.grid(row=0, column=0, sticky=tk.W)
        

        display_name = self.main_window.ui_setup.get_display_name(tweak_name)
        title_label = ttk.Label(header_frame, text=UI_TEXT['help_title'].format(tweak_name=display_name), 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=20)
        
        content_frame = ttk.Frame(self.help_frame)
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        text_widget = tk.Text(content_frame, wrap=tk.WORD, font=("Consolas", 9), 
                             bg="white", fg="black", relief=tk.SUNKEN, borderwidth=1)
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        self.help_active = True
        
        text_widget.focus_set()
    
    def hide_help_overlay(self):
        if self.help_frame:
            self.help_frame.destroy()
            self.help_frame = None
        
        self.main_window.ui_setup.active_tweaks_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.help_active = False
    
    def toggle_info_overlay(self):
        if self.main_window.overlay_frame:
            self.hide_info_overlay()
        else:
            self.show_app_info()
    
    def show_app_info(self):
        self.main_window.ui_setup.main_content_frame.grid_remove()
        
        self.main_window.overlay_frame = ttk.Frame(self.main_window.ui_setup.main_frame)
        self.main_window.overlay_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        self.main_window.overlay_frame.columnconfigure(0, weight=1)
        self.main_window.overlay_frame.rowconfigure(1, weight=1)
        
        header_frame = ttk.Frame(self.main_window.overlay_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(1, weight=1)
        
        back_button = ttk.Button(header_frame, text="← Back to Main", 
                                command=self.hide_info_overlay, style='Large.TButton')
        back_button.grid(row=0, column=0, sticky=tk.W)
        
        title_label = ttk.Label(header_frame, text="Application Information", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=20)
        
        content_frame = ttk.Frame(self.main_window.overlay_frame)
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        text_widget = tk.Text(content_frame, wrap=tk.WORD, font=("Consolas", 9), 
                             bg="white", fg="black", relief=tk.SUNKEN, borderwidth=1)
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        game_settings = get_current_game_settings()
        compatible_version = game_settings.get('compatible_version', 'V1.0.0')
        
        info_text = f"""{UI_TEXT['info_title']}

Application Information:
• Version: {CURRENT_VERSION}
• Built with: Python 3.13
• Developer: SparkNV

About This Application:
This is a dynamic tweak/mod management app. 
The application reads all tweak configurations from a JSON file, making 
it easy to add new tweaks without modifying any Python code.

Required Fields:
• name: Display name for the tweak
• type: Data type (bool, float, int)
• description: Brief description
• originalByteArray: Original game bytes (hex format)
• modifiedByteArray: Modified game bytes (hex format)
• variableOffset: Memory offset for variable tweaks
• variableType: Data type for variable tweaks
• group: Unique group identifier, this is used to group related tweaks together.
• visible: Whether to show in GUI
• section: Which GUI section to display the tweak in

Optional Fields:
• help: Detailed help message (only for visible tweaks)
• min: Minimum value for numeric tweaks
• max: Maximum value for numeric tweaks

JSON Structure Example:

  "category_name": 
    "tweak_id": 
      "name": "Tweak Display Name",
      "type": "bool",
      "description": "Brief description",
      "originalByteArray": "0x1234567890ABCDEF",
      "modifiedByteArray": "0xFEDCBA0987654321",
      "variableOffset": 0,
      "variableType": "bool",
      "group": "unique_group_name",
      "visible": true,
      "section": "Section Name",
      "help": "Detailed help message"
    
  


Grouping System:
• Every tweak must have a 'group' field
• Set 'visible: true' for the main tweak in a group
• Set 'visible: false' (or omit) for secondary patches
• Only visible tweaks appear in the GUI
• Enabling a visible tweak automatically applies all tweaks in its group

The system automatically:
• Counts unique tweak groups for progress indicators
• Organizes tweaks by section in the GUI
• Provides help messages for visible tweaks
• Handles grouped tweak activation/deactivation

Bounds Logic System:
The 'bounds_logic' field enables automatic management of dependent tweaks based on values.

Available Bounds Logic Types:
• "disable_lower_bound": Automatically applies/removes tweaks based on multiplier values

How Bounds Logic Works:
When a tweak has "bounds_logic": "disable_lower_bound":
• If the main tweak's value is < 1.0: The bounds tweak is automatically applied
• If the main tweak's value is ≥ 1.0: The bounds tweak is automatically removed

Example - XP Multiplier:

  "customXPMultiplier": 
    "name": "Custom XP Multiplier",
    "type": "float",
    "group": "xp_multiplier",
    "visible": true

  "customXPMultiplierDisableLowerBound1": 
    "name": "Disable Lower Bound 1",
    "type": "bool", 
    "group": "xp_multiplier",
    "bounds_logic": "disable_lower_bound",
    "visible": false
  


When you set XP Multiplier to 0.5 (< 1.0):
• Main tweak applies with value 0.5
• All "disable_lower_bound" tweaks automatically apply

When you set XP Multiplier to 2.0 (≥ 1.0):
• Main tweak applies with value 2.0  
• All "disable_lower_bound" tweaks automatically remove

Benefits:
• No manual management of dependent tweaks
• Clean UI (bounds tweaks are hidden from active list)
• Automatic handling of complex game validation logic
• Extensible for future bounds logic types"""
        
        text_widget.insert(tk.END, info_text)
        text_widget.config(state=tk.DISABLED)
        
        text_widget.focus_set()
        
        self.main_window.ui_setup.info_button.config(text="← Back")
    
    def hide_info_overlay(self):
        if self.main_window.overlay_frame:
            self.main_window.overlay_frame.destroy()
            self.main_window.overlay_frame = None
        
        self.main_window.ui_setup.main_content_frame.grid()
        
        self.main_window.ui_setup.info_button.config(text="ℹ Info")
