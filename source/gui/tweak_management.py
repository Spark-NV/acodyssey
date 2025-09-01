import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, List

from gui.components import LoadingDialog, ValueInputDialog
from gui.dialogs import ErrorDialog, SimpleLoadingDialog
from core.tweak_manager import GameModification, initialize_game_modifications, count_active_modifications, apply_value_tweak
from config.settings import MESSAGES, UI_TEXT


class TweakManagement:
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.root = main_window.root
    
    def initialize_tweaks(self):
        if not self.main_window.file_name:
            return
        
        self.main_window.ui_setup.clear_tweak_sections()
        self.main_window.ui_setup.create_tweak_sections()
        
        current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        
        from config.game_config import get_game_config
        game_config = get_game_config(current_game_id)
        game_name = game_config['name'] if game_config else "Game"
        
        loading_dialog = LoadingDialog(
            self.root, 
            UI_TEXT['loading_text'].format(game_name=game_name),
            UI_TEXT['loading_description'],
            400, 150
        )
        
        try:
            GameModification.clear_file_cache()
            
            def progress_callback(current, total):
                loading_dialog.update_progress(current, total, f"Initializing tweak {current} of {total}...")
            
            self.main_window.tweaks = initialize_game_modifications(
                self.main_window.file_name, 
                progress_callback, 
                current_game_id
            )
            
            for tweak_name, tweak in self.main_window.tweaks.items():
                if isinstance(tweak, GameModification):
                    tweak.check_modification_status()
            
            self.update_all_status()
            from config.settings import count_tweaks_from_json
            dynamic_count = count_tweaks_from_json(current_game_id)
            self.main_window.ui_setup.status_label.config(text=f"Available Tweaks ({dynamic_count})")
            
        except Exception as e:
            ErrorDialog.show_operation_failed("initialize tweaks", str(e))
            self.main_window.ui_setup.status_label.config(text="Initialization failed")
        finally:
            loading_dialog.close()
    
    def update_all_status(self):
        for tweak_name, status_var in self.main_window.ui_setup.status_vars.items():
            if tweak_name in self.main_window.tweaks:
                tweak = self.main_window.tweaks[tweak_name]
                if tweak.status == 'Active':
                    status_var.set("Active")
                    self.update_button_states(tweak_name, True)
                elif tweak.status == 'Inactive':
                    status_var.set("Inactive")
                    self.update_button_states(tweak_name, False)
                else:
                    status_var.set("Error")
                    self.update_button_states(tweak_name, False)
        
        self.main_window.ui_setup.update_active_tweaks_display()
        self.update_status_colors()
    
    def update_status_colors(self):
        for section in self.main_window.ui_setup.sections.values():
            widgets = section.get_widgets()
            for tweak_name, widget_data in widgets.items():
                status_text = widget_data["status_var"].get()
                if status_text == "Active":
                    widget_data["status_label"].configure(foreground="green")
                elif status_text == "Inactive":
                    widget_data["status_label"].configure(foreground="red")
                elif status_text == "Error":
                    widget_data["status_label"].configure(foreground="orange")
                else:
                    widget_data["status_label"].configure(foreground="black")
    
    def update_button_states(self, tweak_name: str, is_active: bool):
        if tweak_name not in self.main_window.ui_setup.tweak_buttons:
            return
        
        enable_btn = self.main_window.ui_setup.tweak_buttons[tweak_name]["enable"]
        disable_btn = self.main_window.ui_setup.tweak_buttons[tweak_name]["disable"]
        tweak_info = self.main_window.ui_setup.tweak_info.get(tweak_name, {})
        
        if is_active:
            if tweak_info.get("type") in ["float", "int"]:
                enable_btn.config(text="Change Value", state="normal")
                enable_btn.config(command=lambda name=tweak_name: self.change_tweak_value(name))
            else:
                enable_btn.config(text="Enable", state="disabled")
            disable_btn.config(state="normal")
        else:
            enable_btn.config(text="Enable", state="normal")
            enable_btn.config(command=lambda name=tweak_name: self.enable_tweak(name))
            disable_btn.config(state="disabled")
    
    def enable_tweak(self, tweak_name: str):
        if self.main_window.help_active:
            self.main_window.hide_help_overlay()
        
        if not self.main_window.file_name:
            current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
            ErrorDialog.show_file_not_found(current_game_id)
            return
        
        if tweak_name not in self.main_window.tweaks:
            ErrorDialog.show_operation_failed("enable tweak", f"Tweak {tweak_name} not found")
            return
        
        tweak = self.main_window.tweaks[tweak_name]
        tweak_info = self.main_window.ui_setup.tweak_info.get(tweak_name, {})
        
        if tweak.status == 'Inactive':
            try:
                if tweak_info.get("type") == "bool":
                    display_name = self.get_main_tweak_display_name(tweak_name)
                    loading_dialog = SimpleLoadingDialog(self.root, "Enabling", display_name)
                    try:
                        self.apply_simple_tweak(tweak_name)
                    finally:
                        loading_dialog.close()
                elif tweak_info.get("type") in ["float", "int"]:
                    self.prompt_for_value_and_apply(tweak_name, tweak_info)
            except Exception as e:
                ErrorDialog.show_operation_failed("enable tweak", str(e))
        else:
            messagebox.showinfo("Info", MESSAGES['already_active'].format(tweak_name=tweak_name))
    
    def disable_tweak(self, tweak_name: str):
        if self.main_window.help_active:
            self.main_window.hide_help_overlay()
        
        if not self.main_window.file_name:
            current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
            ErrorDialog.show_file_not_found(current_game_id)
            return
        
        if tweak_name not in self.main_window.tweaks:
            ErrorDialog.show_operation_failed("disable tweak", f"Tweak {tweak_name} not found")
            return
        
        tweak = self.main_window.tweaks[tweak_name]
        
        if tweak.status == 'Active':
            display_name = self.get_main_tweak_display_name(tweak_name)
            loading_dialog = SimpleLoadingDialog(self.root, "Disabling", display_name)
            
            try:
                self.remove_grouped_tweak(tweak_name)
                self.update_all_status()
            except Exception as e:
                ErrorDialog.show_operation_failed("disable tweak", str(e))
            finally:
                loading_dialog.close()
        else:
            messagebox.showinfo("Info", MESSAGES['not_active'].format(tweak_name=tweak_name))
    
    def change_tweak_value(self, tweak_name: str):
        if not self.main_window.file_name:
            current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
            ErrorDialog.show_file_not_found(current_game_id)
            return
        
        if tweak_name not in self.main_window.tweaks:
            ErrorDialog.show_operation_failed("change tweak", f"Tweak {tweak_name} not found")
            return
        
        tweak = self.main_window.tweaks[tweak_name]
        tweak_info = self.main_window.ui_setup.tweak_info.get(tweak_name, {})
        
        if tweak.status != 'Active':
            messagebox.showinfo("Info", MESSAGES['not_active'].format(tweak_name=tweak_name))
            return
        
        if tweak_info.get("type") not in ["float", "int"]:
            messagebox.showinfo("Info", MESSAGES['no_value_changes'].format(tweak_name=tweak_name))
            return
        
        self.prompt_for_value_and_apply(tweak_name, tweak_info, is_change=True)
    
    def apply_simple_tweak(self, tweak_name: str):
        try:
            from core.tweak_manager import load_tweak_definitions
            
            current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
            tweak_defs = load_tweak_definitions(current_game_id)
            current_group = self.get_tweak_group(tweak_defs, tweak_name)
            
            tweak = self.main_window.tweaks[tweak_name]
            tweak.apply_modification()
            

            if current_group:
                self.apply_group_tweaks(current_group, tweak_name, exclude_main=True)
            
            self.update_all_status()
        except Exception as e:
            ErrorDialog.show_operation_failed("enable tweak", str(e))
    
    def remove_grouped_tweak(self, tweak_name: str):
        try:
            from core.tweak_manager import load_tweak_definitions
            
            current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
            tweak_defs = load_tweak_definitions(current_game_id)
            current_group = self.get_tweak_group(tweak_defs, tweak_name)
            
            tweak = self.main_window.tweaks[tweak_name]
            tweak.remove_modification()
            

            if current_group:
                self.remove_group_tweaks(current_group, tweak_name, exclude_main=True)
        except Exception as e:
            ErrorDialog.show_operation_failed("disable tweak", str(e))
    
    def get_tweak_group(self, tweak_defs: Dict, tweak_name: str) -> str:
        for category, category_tweaks in tweak_defs.items():
            if category == 'game_info':
                continue
            if isinstance(category_tweaks, dict) and tweak_name in category_tweaks:
                return category_tweaks[tweak_name].get('group')
        return None
    
    def get_main_tweak_display_name(self, tweak_name: str) -> str:
        from core.tweak_manager import load_tweak_definitions
        
        current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        tweak_defs = load_tweak_definitions(current_game_id)
        current_group = self.get_tweak_group(tweak_defs, tweak_name)
        
        if current_group:
    
            for category, category_tweaks in tweak_defs.items():
                if category == 'game_info':
                    continue
                if isinstance(category_tweaks, dict):
                    for group_tweak_name, group_tweak_data in category_tweaks.items():
                        if (group_tweak_data.get('group') == current_group and 
                            group_tweak_data.get('visible', False)):
                            return group_tweak_data.get('name', group_tweak_name)
        

        return self.main_window.ui_setup.get_display_name(tweak_name)
    
    def get_group_tweaks(self, group_name: str) -> List[str]:
        from core.tweak_manager import load_tweak_definitions
        
        current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        tweak_defs = load_tweak_definitions(current_game_id)
        group_tweaks = []
        
        for category, category_tweaks in tweak_defs.items():
            if category == 'game_info':
                continue
            if isinstance(category_tweaks, dict):
                for tweak_id, tweak_data in category_tweaks.items():
                    if tweak_data.get('group') == group_name:
                        group_tweaks.append(tweak_id)
        
        return group_tweaks
    
    def group_has_bounds_logic(self, group_name: str, tweak_defs: Dict) -> bool:
        for category, category_tweaks in tweak_defs.items():
            if category == 'game_info':
                continue
            if isinstance(category_tweaks, dict):
                for tweak_id, tweak_data in category_tweaks.items():
                    if (tweak_data.get('group') == group_name and 
                        'bounds_logic' in tweak_data):
                        return True
        return False
    
    def apply_group_tweaks(self, group_name: str, main_tweak_name: str = None, exclude_main: bool = False):
        group_tweaks = self.get_group_tweaks(group_name)
        
        for tweak_name in group_tweaks:
            if tweak_name in self.main_window.tweaks:
                if exclude_main and tweak_name == main_tweak_name:
                    continue
                
                tweak = self.main_window.tweaks[tweak_name]
                if tweak.status == 'Inactive':
                    tweak.apply_modification()
    
    def remove_group_tweaks(self, group_name: str, main_tweak_name: str = None, exclude_main: bool = False):
        group_tweaks = self.get_group_tweaks(group_name)
        
        for tweak_name in group_tweaks:
            if tweak_name in self.main_window.tweaks:
                if exclude_main and tweak_name == main_tweak_name:
                    continue
                
                tweak = self.main_window.tweaks[tweak_name]
                if tweak.status == 'Active':
                    tweak.remove_modification()
    
    def prompt_for_value_and_apply(self, tweak_name: str, tweak_info: dict, is_change: bool = False):
        value_type = tweak_info.get("type")
        min_val = tweak_info.get("min")
        max_val = tweak_info.get("max")
        
        if is_change:
            title = f"Change Value for {self.main_window.ui_setup.get_display_name(tweak_name)}"
        else:
            title = f"Enter Value for {self.main_window.ui_setup.get_display_name(tweak_name)}"
        
        if is_change:
            description = MESSAGES['change_value'].format(tweak_name=self.main_window.ui_setup.get_display_name(tweak_name))
        else:
            description = MESSAGES['enter_value'].format(tweak_name=self.main_window.ui_setup.get_display_name(tweak_name))
            
        if min_val is not None and max_val is not None:
            description += f"\n{MESSAGES['valid_range'].format(min_val=min_val, max_val=max_val)}"
        elif min_val is not None:
            description += f"\n{MESSAGES['min_value'].format(min_val=min_val)}"
        elif max_val is not None:
            description += f"\n{MESSAGES['max_value'].format(max_val=max_val)}"
        
        if value_type == "float":
            description += f"\n{MESSAGES['float_description']}"
        elif value_type == "int":
            description += f"\n{MESSAGES['int_description']}"
        
        dialog = ValueInputDialog(self.root, title, description, value_type, min_val, max_val)
        result = dialog.get_result()
        
        if result["cancelled"]:
            return
        
        if is_change:
            display_name = self.get_main_tweak_display_name(tweak_name)
            loading_dialog = SimpleLoadingDialog(self.root, "Changing", display_name)
        else:
            display_name = self.get_main_tweak_display_name(tweak_name)
            loading_dialog = SimpleLoadingDialog(self.root, "Enabling", display_name)
        
        try:
            self.apply_value_tweak(tweak_name, tweak_info, result["value"])
        finally:
            loading_dialog.close()
    
    def apply_value_tweak(self, tweak_name: str, tweak_info: dict, value: float):
        try:
            from core.tweak_manager import load_tweak_definitions
            
            tweak = self.main_window.tweaks[tweak_name]
            if not apply_value_tweak(tweak, value, tweak_info):
                ErrorDialog.show_operation_failed("apply value", MESSAGES['invalid_value'])
                return
            
            
            current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
            tweak_defs = load_tweak_definitions(current_game_id)
            current_group = self.get_tweak_group(tweak_defs, tweak_name)
            
            if current_group:

                self.apply_group_tweaks(current_group, tweak_name, exclude_main=True)
                

                if self.group_has_bounds_logic(current_group, tweak_defs):
                    self.handle_group_special_logic(current_group, value)
            
            self.update_all_status()
            
        except Exception as e:
            ErrorDialog.show_operation_failed(f"enable {tweak_name}", str(e))
    
    def handle_group_special_logic(self, group_name: str, value: float):
        from core.tweak_manager import load_tweak_definitions
        
        current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        tweak_defs = load_tweak_definitions(current_game_id)
        

        for category, category_tweaks in tweak_defs.items():
            if category == 'game_info':
                continue
            if isinstance(category_tweaks, dict):
                for tweak_name, tweak_data in category_tweaks.items():
                    if (tweak_data.get('group') == group_name and 
                        'bounds_logic' in tweak_data and
                        tweak_name in self.main_window.tweaks):
                        
                        bounds_logic = tweak_data['bounds_logic']
                        if bounds_logic == 'disable_lower_bound':
                            if value < 1.0:
    
                                self.main_window.tweaks[tweak_name].apply_modification()
                            else:

                                self.main_window.tweaks[tweak_name].remove_modification()
    
    def disable_all(self):
        if self.main_window.help_active:
            self.main_window.hide_help_overlay()
        
        active_count = count_active_modifications(self.main_window.tweaks)
        if active_count == 0:
            ErrorDialog.show_no_active_tweaks()
            return
        
        from gui.dialogs import ConfirmationDialog
        if not ConfirmationDialog.confirm_disable_all_tweaks(active_count):
            return
        
        loading_dialog = LoadingDialog(
            self.root,
            "Disabling All Tweaks",
            f"Disabling {active_count} active tweaks...",
            350, 120
        )
        
        try:
            active_tweaks = [name for name, tweak in self.main_window.tweaks.items() 
                           if isinstance(tweak, GameModification) and tweak.status == 'Active']
            
            for i, tweak_name in enumerate(active_tweaks):
                tweak = self.main_window.tweaks.get(tweak_name)
                if isinstance(tweak, GameModification) and tweak.status == 'Active':
                    tweak.remove_modification()
                    loading_dialog.set_message(f"Disabling {tweak_name}...")
            
            self.update_all_status()
            ErrorDialog.show_success(f"Successfully disabled {active_count} tweaks")
            
        except Exception as e:
            ErrorDialog.show_operation_failed("disable all tweaks", str(e))
        finally:
            loading_dialog.close()
    
    def refresh_status(self):
        if self.main_window.help_active:
            self.main_window.hide_help_overlay()
        
        if self.main_window.file_name:
            GameModification.clear_file_cache()
            self.initialize_tweaks()
        else:
            current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
            ErrorDialog.show_file_not_found(current_game_id)
    
    def refresh_tweak_status_only(self):
        if not self.main_window.file_name or not self.main_window.tweaks:
            return
        
        GameModification.clear_file_cache()
        

        for tweak_name, tweak in self.main_window.tweaks.items():
            if isinstance(tweak, GameModification):
                tweak.check_modification_status()
        

        self.update_all_status()
