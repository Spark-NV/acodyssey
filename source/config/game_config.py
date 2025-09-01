import os
import json
from typing import Dict, Any, Optional

def get_game_configs() -> Dict[str, Dict[str, Any]]:
    game_configs = {}
    
    from utils.settings_manager import get_settings_manager
    settings_manager = get_settings_manager()
    tweaks_dir = settings_manager.get_tweak_files_dir()
    
    if tweaks_dir.exists():
        for tweak_file in tweaks_dir.glob('*_tweaks.json'):
            try:
                with open(tweak_file, 'r') as f:
                    tweak_data = json.load(f)
                
                if 'game_info' in tweak_data:
                    game_info = tweak_data['game_info']
                    game_id = game_info.get('game_id', tweak_file.stem.replace('_tweaks', ''))
                    
                    game_configs[game_id] = {
                        'name': game_info.get('name', 'Unknown Game'),
                        'short_name': game_info.get('short_name', game_info.get('name', 'Unknown')),
                        'steam_app_id': game_info.get('steam_app_id', ''),
                        'executable_name': game_info.get('executable_name', ''),
                        'nexus_mods_url': game_info.get('nexus_mods_url', ''),
                        'main_title': game_info.get('main_title', 'Game Tweak Pack'),
                        'tweak_pack_version': game_info.get('tweak_pack_version', 'V1.0'),
                        'subtitle': game_info.get('subtitle', 'Compatible with {game_name} {compatible_version}'),
                        'compatible_version': game_info.get('compatible_version', 'V1.0.0'),
                        'tweak_file': str(tweak_file),
                        'default': game_info.get('default', False),
                        'source': 'custom'
                    }
            except Exception as e:
                print(f"Error loading game config from {tweak_file}: {e}")
    
    return game_configs

def get_current_game_config() -> Optional[Dict[str, Any]]:
    game_configs = get_game_configs()
    if not game_configs:
        return None
    
    for game_id, config in game_configs.items():
        if config.get('default', False):
            return config
    
    return list(game_configs.values())[0]

def get_game_config(game_id: str) -> Optional[Dict[str, Any]]:
    game_configs = get_game_configs()
    return game_configs.get(game_id)

def get_tweak_file_path(game_id: str) -> Optional[str]:
    game_config = get_game_config(game_id)
    if game_config:
        return game_config['tweak_file']
    return None
