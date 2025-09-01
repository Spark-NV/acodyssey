import os
import time
import json
from typing import Dict, Any, Optional, Callable
from bitstring import BitStream, BitArray, ConstBitStream
from shutil import copyfile

from config.settings import count_tweaks_from_json
from core.file_manager import check_for_backup, get_backup_path


class GameModification:
    
    _file_cache = {}
    _cache_timestamp = 0

    def __init__(self, modification_name: str, file_name: str, original_byte_array: str, 
                 modified_byte_array: str, variable_offset: int, variable_type: str):
        self.modification_name = modification_name
        self.file_name = file_name
        self.original_byte_array = original_byte_array
        self.variable_offset = variable_offset
        self.variable_type = variable_type
        self.status = ''
        self.statustext = ''
        self.byte_offset = 0
        self.initialised = False
        
        if variable_offset > 0:
            temp = BitArray(modified_byte_array)
            self.modified_byte_array_firstpart = temp[0:variable_offset * 4]
        self.modified_byte_array = modified_byte_array
        
        self.check_modification_status()

    def check_modification_status(self):
        file_stream = self.get_cached_file_stream(self.file_name)
        found = file_stream.find(self.original_byte_array, bytealigned=True)
        
        if len(found) > 1:
            self.status = 'ERROR!'
        elif len(found) == 1:
            self.status = 'Inactive'
            self.statustext = 'Inactive'
            self.byte_offset = found
        else:
            if self.variable_offset > 0:
                found = file_stream.find(self.modified_byte_array_firstpart, bytealigned=True)
                if len(found) == 1:
                    length = len(self.modified_byte_array) * 4
                    self.modified_byte_array = '0x' + file_stream.read(length).hex
                    self.status = 'Active'
                    if self.variable_type == 'float':
                        self.statustext = 'Active (%.2f)' % BitArray(self.modified_byte_array)[self.variable_offset * 4:self.variable_offset * 4 + 32].floatle
                    if self.variable_type == 'byte':
                        self.statustext = 'Active (%u)' % BitArray(self.modified_byte_array)[self.variable_offset * 4:self.variable_offset * 4 + 8].uint
                    self.byte_offset = found
                else:
                    self.status = 'Error'
                    self.statustext = 'ERROR!'
            else:
                found = file_stream.find(self.modified_byte_array, bytealigned=True)
                if len(found) == 1:
                    self.status = 'Active'
                    self.statustext = 'Active'
                    self.byte_offset = found
                else:
                    self.status = 'Error'
                    self.statustext = 'ERROR!'

    def apply_modification(self):
        if self.status == 'Inactive':
            self.clear_file_cache()
            file_stream = BitStream(filename=self.file_name)
            file_stream.pos = self.byte_offset[0]
            file_stream.overwrite(self.modified_byte_array)
            self.save_modification(file_stream)
            self.check_modification_status()

    def remove_modification(self):
        if self.status == 'Active':
            self.clear_file_cache()
            file_stream = BitStream(filename=self.file_name)
            file_stream.pos = self.byte_offset[0]
            file_stream.overwrite(self.original_byte_array)
            self.save_modification(file_stream)
            self.check_modification_status()

    def save_modification(self, file_stream):
        if self.status == 'Active' or self.status == 'Inactive':
            try:
                with open(self.file_name, 'wb') as f:
                    file_stream.tofile(f)
                self.clear_file_cache()
            except IOError:
                pass
    
    @classmethod
    def get_cached_file_stream(cls, file_name: str) -> ConstBitStream:
        try:
            current_timestamp = os.path.getmtime(file_name)
            if file_name in cls._file_cache and cls._cache_timestamp >= current_timestamp:
                return cls._file_cache[file_name]
        except OSError:
            pass
        
        try:
            file_stream = ConstBitStream(filename=file_name)
            cls._file_cache[file_name] = file_stream
            cls._cache_timestamp = current_timestamp
            return file_stream
        except Exception:
            return ConstBitStream(filename=file_name)
    
    @classmethod
    def clear_file_cache(cls):

        import gc
        cls._file_cache.clear()
        cls._cache_timestamp = 0
        gc.collect()


def load_tweak_definitions(game_id: str = None) -> Dict[str, Any]:
    if game_id is None:
        from config.game_config import get_current_game_config
        current_game = get_current_game_config()
        if current_game:
            game_id = current_game.get('game_id')
        else:
            return {}
    
    from config.game_config import get_tweak_file_path
    config_path = get_tweak_file_path(game_id)
    
    if not config_path or not os.path.exists(config_path):
        return {}
    
    with open(config_path, 'r') as f:
        return json.load(f)


def initialize_game_modifications(file_name: str, progress_callback: Optional[Callable] = None, game_id: str = None) -> Dict[str, GameModification]:
    tweak_defs = load_tweak_definitions(game_id)
    
    unique_groups = set()
    individual_tweaks = 0
    
    for category, category_tweaks in tweak_defs.items():
        if category == 'game_info':
            continue
        for tweak_id, tweak_data in category_tweaks.items():
            if isinstance(tweak_data, dict):
                if 'group' in tweak_data:
                    unique_groups.add(tweak_data['group'])
                else:
                    individual_tweaks += 1
    
    total_unique_tweaks = len(unique_groups) + individual_tweaks
    initialized_count = 0
    counted_groups = set()
    
    def update_progress():
        nonlocal initialized_count
        initialized_count += 1
        if progress_callback:
            progress_callback(initialized_count, total_unique_tweaks)
    
    modifications = {}
    
    for category, category_tweaks in tweak_defs.items():
        if category == 'game_info':
            continue
        for tweak_id, tweak_data in category_tweaks.items():
            modification = GameModification(
                modification_name=tweak_data['name'],
                file_name=file_name,
                original_byte_array=tweak_data['originalByteArray'],
                modified_byte_array=tweak_data['modifiedByteArray'],
                variable_offset=tweak_data['variableOffset'],
                variable_type=tweak_data['variableType']
            )
            modifications[tweak_id] = modification
            
            if 'group' in tweak_data:
                group_name = tweak_data['group']
                if group_name not in counted_groups:
                    counted_groups.add(group_name)
                    update_progress()
            else:
                update_progress()
    
    return modifications


def count_active_modifications(modification_list: Dict[str, GameModification], game_id: str = None) -> int:
    active_groups = set()
    individual_active_count = 0
    
    for item_name, item_instance in modification_list.items():
        if isinstance(item_instance, GameModification) and item_instance.status == 'Active':
            try:
                tweak_defs = load_tweak_definitions(game_id)
                for category, category_tweaks in tweak_defs.items():
                    if category == 'game_info':
                        continue
                    if item_name in category_tweaks:
                        tweak_data = category_tweaks[item_name]
                        if 'group' in tweak_data:
                            active_groups.add(tweak_data['group'])
                        else:
                            individual_active_count += 1
                        break
            except Exception:
                individual_active_count += 1
    
    return len(active_groups) + individual_active_count

def create_backup(file_name: str, game_id: str = None) -> bool:
    try:
        backup_path = get_backup_path(file_name, game_id)
        copyfile(file_name, backup_path)
        return True
    except Exception:
        return False


def restore_backup(file_name: str, game_id: str = None) -> bool:
    try:

        GameModification.clear_file_cache()
        backup_path = get_backup_path(file_name, game_id)
        if not check_for_backup(file_name, game_id):
            return False
        copyfile(backup_path, file_name)
        return True
    except Exception:
        return False


def apply_value_tweak(tweak: GameModification, value: float, tweak_info: Dict[str, Any]) -> bool:
    try:
        value_type = tweak_info.get("type")
        min_val = tweak_info.get("min")
        max_val = tweak_info.get("max")
        
        if min_val is not None and value < min_val:
            return False
        if max_val is not None and value > max_val:
            return False
        
        was_active = tweak.status == 'Active'
        if was_active:
            tweak.remove_modification()
        
        if value_type == "float":
            temp = BitArray(floatle=value, length=32)
        else:
            temp = BitArray(uint=value, length=8)
        
        temp2 = BitArray(tweak.modified_byte_array)
        temp2.overwrite(temp, tweak.variable_offset * 4)
        tweak.modified_byte_array = '0x' + temp2.hex
        tweak.apply_modification()
        
        return True
    except Exception:
        return False
