import os
import json
from typing import Dict, Any
from .game_config import get_current_game_config, get_game_configs, get_game_config


def count_tweaks_from_json(game_id: str = None) -> int:
    try:
        if game_id is None:
            current_game = get_current_game_config()
            if current_game:
                game_id = current_game.get('game_id')
            else:
                return 0
        
        from .game_config import get_tweak_file_path
        config_path = get_tweak_file_path(game_id)
        
        if not config_path or not os.path.exists(config_path):
            return 0
            
        with open(config_path, 'r') as f:
            tweak_defs = json.load(f)
        
        unique_groups = set()
        total_count = 0
        
        for category, category_tweaks in tweak_defs.items():
            if category == 'game_info':
                continue
            if isinstance(category_tweaks, dict):
                for tweak_id, tweak_data in category_tweaks.items():
                    if isinstance(tweak_data, dict):
                        if 'group' in tweak_data:
                            unique_groups.add(tweak_data['group'])
                        else:
                            total_count += 1
        
        total_count += len(unique_groups)
        
        return total_count
    except Exception:
        return 0


CURRENT_VERSION = 'V1.0'

DEFAULT_STEAM_PATHS = [
    r'C:\Program Files (x86)\Steam',
    r'C:\Program Files\Steam'
]

STEAM_REGISTRY_KEYS = [
    r'SOFTWARE\Wow6432Node\Valve\Steam',
    r'SOFTWARE\Valve\Steam'
]

GAME_REGISTRY_MUICACHE_KEY = r'Local Settings\Software\Microsoft\Windows\Shell\MuiCache'

def get_current_game_settings(game_id: str = None):
    if game_id:
        current_game = get_game_config(game_id)
    else:
        current_game = get_current_game_config()
    
    if current_game:
        return {
            'name': current_game.get('name', 'Unknown Game'),
            'short_name': current_game.get('short_name', 'Unknown'),
            'steam_app_id': current_game.get('steam_app_id', ''),
            'executable_name': current_game.get('executable_name', ''),
            'nexus_mods_url': current_game.get('nexus_mods_url', ''),
            'backup_file_name': f"{current_game.get('executable_name', 'game')}.backup",
            'main_title': current_game.get('main_title', 'Game Tweak Pack'),
            'tweak_pack_version': current_game.get('tweak_pack_version', 'V1.0'),
            'subtitle': current_game.get('subtitle', 'Compatible with {game_name} {compatible_version}'),
            'compatible_version': current_game.get('compatible_version', 'V1.0.0')
        }
    
    return {
        'name': 'No Games Available',
        'short_name': 'None',
        'steam_app_id': '',
        'executable_name': '',
        'nexus_mods_url': '',
        'backup_file_name': '',
        'main_title': 'Game Tweak Pack',
        'tweak_pack_version': 'V1.0',
        'subtitle': 'No games configured',
        'compatible_version': 'V1.0.0'
    }

GUI_STYLES = {
    'Large.TButton': {
        'padding': (15, 8),
        'font': ('Arial', 11)
    },
    'Help.TButton': {
        'padding': (8, 8),
        'font': ('Arial', 11)
    }
}

MAIN_WINDOW_SIZE = "1200x700"
MAIN_WINDOW_MIN_SIZE = (1000, 600)
LOADING_WINDOW_SIZE = "400x150"
DIALOG_SIZE = "400x200"


DIALOG_DIMENSIONS = {
    'value_input': "400x200",
    'simple_loading': "300x100",
    'info_dialog': "800x600",
    'loading': "400x150"
}


FONT_CONFIG = {
    'title': ("Arial", 16, "bold"),
    'subtitle': ("Arial", 10),
    'section': ("Arial", 12, "bold"),
    'tweak_name': ("Arial", 13, "bold"),
    'status': ("Arial", 12),
    'button': ("Arial", 11),
    'text': ("Consolas", 9),
    'info': ("Arial", 14, "bold")
}


FILE_SETTINGS = {
    'executable_extensions': ['exe', 'com', 'bat', 'cmd'],
    'file_type_filters': [("Executable files", "*.exe"), ("All files", "*.*")],
    'max_path_length': 260,
    'invalid_filename_chars': '<>:"/\\|?*',
    'default_filename': "unnamed"
}


UI_TEXT = {
    'enable_button': "Enable",
    'disable_button': "Disable",
    'change_value_button': "Change Value",
    'help_button': "?",
    'ok_button': "OK",
    'cancel_button': "Cancel",
    'close_button': "Close",
    'status_label': "Status:",
    'unknown_status': "Unknown",
    'window_title': "Game Tweaker",
    'main_title': "Game Tweak Pack {version}",
    'subtitle': "Compatible with {game_name} {compatible_version}",
    'loading_text': "Initializing {game_name} Tweaks",
    'info_title': "Game Tweaker",
    'loading_description': "Initializing...please be patient...",
    'help_title': "Help: {tweak_name}",
    'close_help': "× Close",
    'game_selector_label': "Select Game:",
    'no_games_available': "No games available"
}


MESSAGES = {
    'file_not_found': "{game_exe} not found automatically.",
    'file_not_found_error': "{game_exe} not found. Please select the file manually.",
    'select_file_prompt': "Would you like to browse for the file manually?",
    'select_file_title': "Select {game_exe}",
    'wrong_file_error': "Please select {game_exe} file",
    'no_backup_error': "No backup found. Create a backup first.",
    'no_active_tweaks': "No active tweaks to disable.",
    'operation_failed': "Failed to {operation}: {error}",
    'success': "{operation} completed successfully.",
    'backup_with_active_warning': "There are active tweaks. Disable them before creating a backup.",
    'confirm_disable_all': "Are you sure you want to disable all {count} active tweaks?",
    'confirm_restore_backup': "Are you sure you want to restore the backup? This will overwrite the current game file.",
    'already_active': "{tweak_name} is already active",
    'not_active': "{tweak_name} is not active",
    'not_found': "Tweak {tweak_name} not found",
    'no_value_changes': "{tweak_name} does not support value changes",
    'enter_value': "Please enter a value for {tweak_name}:",
    'change_value': "Please enter a new value for {tweak_name}:",
    'valid_range': "Valid range: {min_val} to {max_val}",
    'min_value': "Minimum value: {min_val}",
    'max_value': "Maximum value: {max_val}",
    'float_description': "Number can be a whole number or decimal (e.g., 2.5)",
    'int_description': "Enter a whole number with no decimal places (e.g., 2)",
    'enter_value_error': "Please enter a value",
    'invalid_decimal': "Please enter a valid decimal number",
    'invalid_integer': "Please enter a valid whole number",
    'value_too_low': "Value must be at least {min_val}",
    'value_too_high': "Value must be at most {max_val}",
    'invalid_value': "Invalid value",
    'game_changed': "Game changed to {game_name}."
}
