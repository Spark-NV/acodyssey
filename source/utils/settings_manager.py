import os
import configparser
from typing import Dict, Optional
from pathlib import Path


class SettingsManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.settings_dir = Path(os.environ.get('APPDATA', '')) / 'game_tweaks'
        self.settings_file = self.settings_dir / 'settings.ini'
        
        self.settings_dir.mkdir(parents=True, exist_ok=True)
        
        self.initialize_tweak_files()
        
        self.load_settings()
    
    def load_settings(self):
        if self.settings_file.exists():
            try:
                self.config.read(self.settings_file)
            except Exception as e:
                print(f"Error loading settings: {e}")
                self._create_default_config()
        else:
            self._create_default_config()
    
    def _create_default_config(self):
        if 'General' not in self.config:
            self.config.add_section('General')
        if 'GamePaths' not in self.config:
            self.config.add_section('GamePaths')
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                self.config.write(f)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get_current_game(self) -> Optional[str]:
        return self.config.get('General', 'current_game', fallback=None)
    
    def set_current_game(self, game_id: str):
        if 'General' not in self.config:
            self.config.add_section('General')
        self.config.set('General', 'current_game', game_id)
        self.save_settings()
    
    def get_game_path(self, game_id: str) -> Optional[str]:
        return self.config.get('GamePaths', game_id, fallback=None)
    
    def set_game_path(self, game_id: str, exe_path: str):
        if 'GamePaths' not in self.config:
            self.config.add_section('GamePaths')
        self.config.set('GamePaths', game_id, exe_path)
        self.save_settings()
    
    def get_all_game_paths(self) -> Dict[str, str]:
        if 'GamePaths' not in self.config:
            return {}
        return dict(self.config.items('GamePaths'))
    
    def remove_game_path(self, game_id: str):
        if 'GamePaths' in self.config and self.config.has_option('GamePaths', game_id):
            self.config.remove_option('GamePaths', game_id)
            self.save_settings()
    
    def initialize_tweak_files(self):
        import json
        import shutil
        
        tweaks_dir = self.settings_dir / 'tweaks'
        tweaks_dir.mkdir(parents=True, exist_ok=True)
        
        existing_custom_files = list(tweaks_dir.glob('*_tweaks.json'))
        
        if existing_custom_files:
            print(f"Loaded: ({len(existing_custom_files)} Supported Games)")
            return
        
        try:
            from config.embedded_tweaks import EMBEDDED_TWEAKS, get_all_embedded_game_ids
            
            print("Initializing...")
            
            copied_count = 0
            for game_id in get_all_embedded_game_ids():
                try:
                    tweak_data = EMBEDDED_TWEAKS.get(game_id, {})
                    if tweak_data:
                        custom_file_path = tweaks_dir / f"{game_id}_tweaks.json"
                        with open(custom_file_path, 'w', encoding='utf-8') as f:
                            json.dump(tweak_data, f, indent=2, ensure_ascii=False)
                        
                        copied_count += 1
                        
                except Exception as e:
                    print(f"Error initializing tweak file for {game_id}: {e}")
            
            if copied_count > 0:
                return
                
        except ImportError:
            print("Embedded tweak data not available, skipping initialization")
            return
    
    def get_tweak_files_dir(self) -> Path:
        return self.settings_dir / 'tweaks'


_settings_manager = None

def get_settings_manager() -> SettingsManager:
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    return _settings_manager
