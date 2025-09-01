import os
import errno
import winreg
from typing import Optional, List
from utils.validators import is_pathname_valid


def find_executable_recursively(directory: str, executable_name: str, max_depth: int = 7) -> Optional[str]:
    if not os.path.exists(directory) or not os.path.isdir(directory):
        return None
    
    def search_recursive(current_dir: str, depth: int) -> Optional[str]:
        if depth > max_depth:
            return None
        
        try:
            exe_path = os.path.join(current_dir, executable_name)
            if os.path.exists(exe_path) and os.path.isfile(exe_path):
                return exe_path
            
            for item in os.listdir(current_dir):
                item_path = os.path.join(current_dir, item)
                if os.path.isdir(item_path):
                    result = search_recursive(item_path, depth + 1)
                    if result:
                        return result
        except (OSError, PermissionError):
            pass
        
        return None
    
    return search_recursive(directory, 0)


def discover_registry_pattern(executable_name: str) -> Optional[str]:
    try:
        key_path = r'Local Settings\Software\Microsoft\Windows\Shell\MuiCache'
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path)
        
        i = 0
        while True:
            try:
                key_name, key_value, key_type = winreg.EnumValue(key, i)
                
                if executable_name.lower() in key_name.lower() and '.exe' in key_name.lower():
                    if key_name.endswith('.FriendlyAppName'):
                        path_part = key_name[:-16]
                        
                        if '\\' in path_part:
                            parts = path_part.split('\\')
                            if len(parts) >= 2:
                                game_dir = parts[-2]
                                exe_name = parts[-1]
                                
                                pattern = f"\\\\{game_dir}\\\\{exe_name}.FriendlyAppName"
                                winreg.CloseKey(key)
                                return pattern
                
                i += 1
            except WindowsError:
                break
        
        winreg.CloseKey(key)
        
    except WindowsError:
        pass
    
    return None


def get_steam_install_path() -> Optional[str]:
    from config.settings import STEAM_REGISTRY_KEYS
    
    for registry_key in STEAM_REGISTRY_KEYS:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_key)
            steam_path, _ = winreg.QueryValueEx(key, 'InstallPath')
            winreg.CloseKey(key)
            return steam_path
        except WindowsError:
            continue
    
    from config.settings import DEFAULT_STEAM_PATHS
    for path in DEFAULT_STEAM_PATHS:
        if os.path.exists(path):
            return path
    
    return None


def get_steam_library_folders(steam_path: str) -> List[str]:
    library_folders = []
    
    if not steam_path:
        return library_folders
    
    main_library = os.path.join(steam_path, 'steamapps')
    if os.path.exists(main_library):
        library_folders.append(main_library)
    
    libraryfolders_path = os.path.join(steam_path, 'steamapps', 'libraryfolders.vdf')
    if os.path.exists(libraryfolders_path):
        try:
            with open(libraryfolders_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                for i, line in enumerate(lines):
                    line = line.strip()
                    if '"path"' in line and '\\' in line:
                        path_start = line.find('"path"') + 6
                        quote_start = line.find('"', path_start)
                        if quote_start != -1:
                            quote_end = line.find('"', quote_start + 1)
                            if quote_end != -1:
                                library_path = line[quote_start + 1:quote_end]
                                library_path = library_path.replace('\\\\', '\\')
                                steamapps_path = os.path.join(library_path, 'steamapps')
                                if os.path.exists(steamapps_path):
                                    library_folders.append(steamapps_path)
        except Exception:
            pass
    
    return library_folders


def find_game_in_steam_libraries(library_folders: List[str], game_id: str = None) -> Optional[str]:
    from config.settings import get_current_game_settings
    game_settings = get_current_game_settings(game_id)
    steam_app_id = game_settings['steam_app_id']
    executable_name = game_settings['executable_name']
    
    for library in library_folders:
        manifest_path = os.path.join(library, f'appmanifest_{steam_app_id}.acf')
        if os.path.exists(manifest_path):
            
            install_dir = None
            try:
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if '"installdir"' in line:
                            quote_start = line.find('"', line.find('"installdir"') + 12)
                            if quote_start != -1:
                                quote_end = line.find('"', quote_start + 1)
                                if quote_end != -1:
                                    install_dir = line[quote_start + 1:quote_end]
                                    break
            except Exception:
                pass
            
            if install_dir:
                game_dir = os.path.join(library, 'common', install_dir)
                if os.path.exists(game_dir):
                    exe_path = find_executable_recursively(game_dir, executable_name)
                    if exe_path:
                        return exe_path
            
            common_dir = os.path.join(library, 'common')
            if os.path.exists(common_dir):
                exe_path = find_executable_recursively(common_dir, executable_name)
                if exe_path:
                    return exe_path
    
    return None


def find_game_from_registry(game_id: str = None) -> Optional[str]:
    from config.settings import GAME_REGISTRY_MUICACHE_KEY, get_current_game_settings
    game_settings = get_current_game_settings(game_id)
    executable_name = game_settings['executable_name']
    
    search_pattern = discover_registry_pattern(executable_name)
    if not search_pattern:
        return None
    
    try:
        keys = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, GAME_REGISTRY_MUICACHE_KEY)
        i = 0
        while True:
            key_name, key_value, key_type = winreg.EnumValue(keys, i)
            if key_name.find(search_pattern, 0) > 0:
                game_path = key_name[0:len(key_name) - 16]
                return game_path
            i += 1
    except WindowsError as e:
        pass
    
    return None


def find_game_file(game_id: str = None) -> Optional[str]:
    from utils.settings_manager import get_settings_manager
    from config.settings import get_current_game_settings
    
    settings = get_settings_manager()
    saved_path = settings.get_game_path(game_id) if game_id else None
    
    if saved_path and os.path.exists(saved_path):
        return saved_path
    
    game_path = find_game_from_registry(game_id)
    if game_path:
        if game_id:
            settings.set_game_path(game_id, game_path)
        return game_path
    
    steam_path = get_steam_install_path()
    if steam_path:
        library_folders = get_steam_library_folders(steam_path)
        if library_folders:
            game_path = find_game_in_steam_libraries(library_folders, game_id)
            if game_path:
                if game_id:
                    settings.set_game_path(game_id, game_path)
                return game_path
    
    return None


def check_for_backup(file_name: str, game_id: str = None) -> bool:
    from config.settings import get_current_game_settings
    
    game_settings = get_current_game_settings(game_id)
    backup_file_name = game_settings['backup_file_name']
    
    backup_dir = os.path.dirname(os.path.abspath(file_name))
    backup_file = backup_dir + os.path.sep + backup_file_name
    return is_pathname_valid(backup_file) and os.path.exists(backup_file)


def get_backup_path(file_name: str, game_id: str = None) -> str:
    from config.settings import get_current_game_settings
    
    game_settings = get_current_game_settings(game_id)
    backup_file_name = game_settings['backup_file_name']
    
    backup_dir = os.path.dirname(os.path.abspath(file_name))
    return backup_dir + os.path.sep + backup_file_name
