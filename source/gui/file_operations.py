import os
from typing import Optional

from core.file_manager import find_game_file, check_for_backup
from core.tweak_manager import GameModification, create_backup, restore_backup, count_active_modifications
from gui.dialogs import FileSelectionDialog, ErrorDialog, ConfirmationDialog
from config.settings import get_current_game_settings


class FileOperations:
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.root = main_window.root
    
    def find_game_file(self, auto_prompt=True):
        current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        self.main_window.file_name = find_game_file(current_game_id)
        
        from config.settings import MESSAGES, get_current_game_settings
        
        if self.main_window.file_name:
            self.main_window.ui_setup.file_label.config(text=self.main_window.file_name, foreground="green")
            self.main_window.backup_exists = check_for_backup(self.main_window.file_name, current_game_id)
            self.check_and_initialize_tweaks()
        else:
            game_settings = get_current_game_settings(current_game_id)
            executable_name = game_settings.get('executable_name', 'game.exe')
            if auto_prompt:
                file_not_found_msg = MESSAGES['file_not_found'].format(game_exe=executable_name)
                self.main_window.ui_setup.file_label.config(text=file_not_found_msg, foreground="orange")
                self.prompt_for_file()
            else:
                clickable_msg = f"Couldn't automatically find {executable_name}, please click me to find it manually."
                self.main_window.ui_setup.file_label.config(text=clickable_msg, foreground="red")
                self.main_window.ui_setup.clear_tweak_sections()
                self.main_window.ui_setup.create_tweak_sections()
                self.main_window.ui_setup.update_active_tweaks_display()
    
    def prompt_for_file(self):
        current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        filename = FileSelectionDialog.prompt_for_file(self.main_window, current_game_id)
        if filename:
            self.main_window.file_name = filename
            from config.settings import MESSAGES
            self.main_window.ui_setup.file_label.config(text=self.main_window.file_name, foreground="green")
            
            current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
            self.main_window.backup_exists = check_for_backup(self.main_window.file_name, current_game_id)
            
            if current_game_id:
                from utils.settings_manager import get_settings_manager
                settings = get_settings_manager()
                settings.set_game_path(current_game_id, filename)
            
            self.check_and_initialize_tweaks()
        else:
            game_settings = get_current_game_settings(current_game_id)
            executable_name = game_settings.get('executable_name', 'game.exe')
            self.main_window.ui_setup.file_label.config(text=f"Couldn't automatically find {executable_name}, please click me to find it manually.", foreground="red")
            self.main_window.ui_setup.clear_tweak_sections()
            self.main_window.ui_setup.create_tweak_sections()
            self.main_window.ui_setup.update_active_tweaks_display()
    
    def check_and_initialize_tweaks(self):
        if self.main_window.file_name and not self.main_window.tweaks:
            self.main_window.tweak_management.initialize_tweaks()
    
    def run_game(self):
        if self.main_window.help_active:
            self.main_window.hide_help_overlay()
        
        if self.main_window.file_name and os.path.exists(self.main_window.file_name):
            os.startfile(self.main_window.file_name)
        else:
            current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
            ErrorDialog.show_file_not_found(current_game_id)
    
    def create_backup(self):
        if self.main_window.help_active:
            self.main_window.hide_help_overlay()
        
        if not self.main_window.file_name:
            current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
            ErrorDialog.show_file_not_found(current_game_id)
            return
        
        current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        if count_active_modifications(self.main_window.tweaks, current_game_id) > 0:
            if ConfirmationDialog.confirm_backup_with_active_tweaks():
                return
        
        current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
        if create_backup(self.main_window.file_name, current_game_id):
            self.main_window.backup_exists = True
            ErrorDialog.show_success("Backup created")
        else:
            ErrorDialog.show_operation_failed("create backup", "Unknown error")
    
    def restore_backup(self):
        if self.main_window.help_active:
            self.main_window.hide_help_overlay()
        
        if not self.main_window.backup_exists:
            ErrorDialog.show_no_backup()
            return
        
        if ConfirmationDialog.confirm_restore_backup():
            current_game_id = self.main_window.current_game_id or self.main_window.game_selector.get_current_game_id()
            if restore_backup(self.main_window.file_name, current_game_id):
                self.main_window.tweak_management.refresh_tweak_status_only()
                ErrorDialog.show_success("Backup restored")
            else:
                ErrorDialog.show_operation_failed("restore backup", "Unknown error")
