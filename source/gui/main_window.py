import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional

from config.settings import CURRENT_VERSION, GUI_STYLES, MAIN_WINDOW_SIZE, MAIN_WINDOW_MIN_SIZE, UI_TEXT, get_current_game_settings
from gui.ui_setup import UISetup
from gui.tweak_management import TweakManagement
from gui.file_operations import FileOperations
from gui.help_system import HelpSystem
from gui.components import GameSelector


class GameTweakPackGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Game Tweak Pack")
        self.root.geometry(MAIN_WINDOW_SIZE)
        self.root.minsize(*MAIN_WINDOW_MIN_SIZE)
        self.root.resizable(True, True)
        
        self.file_name = ""
        self.tweaks = {}
        self.backup_exists = False
        self.current_game_id = None
        
        self.overlay_frame = None
        
        self.ui_setup = UISetup(self)
        self.tweak_management = TweakManagement(self)
        self.file_operations = FileOperations(self)
        self.help_system = HelpSystem(self)
        self.game_selector = GameSelector(self.root, self.on_game_changed)
        
        self.ui_setup.setup_styles()
        
        from utils.settings_manager import get_settings_manager
        settings = get_settings_manager()
        saved_game = settings.get_current_game()
        
        if saved_game and saved_game in [gid for gid in self.game_selector.game_ids]:
            self.game_selector.set_current_game(saved_game)
            self.current_game_id = saved_game
        else:
            self.current_game_id = self.game_selector.get_current_game_id()
            if self.current_game_id:
                settings.set_current_game(self.current_game_id)
        
        self.ui_setup.setup_ui()
        
        self.initialize_application()
        
        game_settings = get_current_game_settings(self.current_game_id)
        title_text = f"{game_settings.get('main_title', 'Game Tweak Pack')} {game_settings.get('tweak_pack_version', 'V1.0')} ({game_settings.get('compatible_version', 'V1.0.0')})"
        self.root.title(title_text)
    
    def initialize_application(self):
        self.file_operations.find_game_file()
        
        if self.file_name:
            self.file_operations.check_and_initialize_tweaks()
        else:
            game_settings = get_current_game_settings(self.current_game_id)
            executable_name = game_settings.get('executable_name', 'game.exe')
            self.ui_setup.status_label.config(text=f"Please select {executable_name} file")
    
    def run_game(self):
        self.file_operations.run_game()
    
    def create_backup(self):
        self.file_operations.create_backup()
    
    def restore_backup(self):
        self.file_operations.restore_backup()
    
    def disable_all(self):
        self.tweak_management.disable_all()
    
    def refresh_status(self):
        self.tweak_management.refresh_status()
    
    def enable_tweak(self, tweak_name: str):
        self.tweak_management.enable_tweak(tweak_name)
    
    def disable_tweak(self, tweak_name: str):
        self.tweak_management.disable_tweak(tweak_name)
    
    def show_help(self, tweak_name: str):
        self.help_system.show_help(tweak_name)
    
    def hide_help_overlay(self):
        self.help_system.hide_help_overlay()
    
    def toggle_info_overlay(self):
        self.help_system.toggle_info_overlay()
    
    def show_tweak_editor(self):
        from gui.tweak_editor import TweakEditor
        editor = TweakEditor(self)
        editor.show_editor()
    
    def refresh_application(self):
        self.game_selector.refresh_games()
        
        self.initialize_application()
        
        self.ui_setup.update_game_info(self.current_game_id)
        self.ui_setup.update_active_tweaks_display()
        
        self.update_window_title()
    
    @property
    def help_active(self):
        return self.help_system.help_active
    
    def update_window_title(self):
        game_settings = get_current_game_settings(self.current_game_id)
        title_text = f"{game_settings.get('main_title', 'Game Tweak Pack')} {game_settings.get('tweak_pack_version', 'V1.0')} ({game_settings.get('compatible_version', 'V1.0.0')})"
        self.root.title(title_text)
    
    def on_game_changed(self, game_id: str):
        if game_id != self.current_game_id:
            if self.help_active:
                self.hide_help_overlay()
            
            self.current_game_id = game_id
            
            from utils.settings_manager import get_settings_manager
            settings = get_settings_manager()
            settings.set_current_game(game_id)
            
            self.file_name = ""
            self.tweaks = {}
            self.backup_exists = False
            
            self.file_operations.find_game_file(auto_prompt=False)
            
            self.ui_setup.update_game_info(game_id)
            
            self.ui_setup.update_active_tweaks_display()
            
            self.update_window_title()
            
            from config.game_config import get_game_config
            from config.settings import MESSAGES
            import tkinter.messagebox as messagebox
            
            game_config = get_game_config(game_id)
            if game_config:
                messagebox.showinfo("Game Changed", 
                                  MESSAGES['game_changed'].format(game_name=game_config['name']))
    
    @property
    def GameModification(self):
        from core.tweak_manager import GameModification
        return GameModification
    
    @property
    def confirmation_dialog(self):
        from gui.dialogs import ConfirmationDialog
        return ConfirmationDialog
