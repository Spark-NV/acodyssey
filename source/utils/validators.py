import os
import errno
from typing import Union, Optional


def is_pathname_valid(pathname: str) -> bool:
    try:
        if not isinstance(pathname, str) or not pathname:
            return False
        root_dirname, pathname = os.path.splitdrive(pathname)
        pathname = pathname[1:len(pathname)]
        root_dirname = root_dirname.rstrip(os.path.sep)
        pathname_fragment = root_dirname
        for pathname_part in pathname.split(os.path.sep):
            pathname_fragment = pathname_fragment + os.path.sep
            pathname_fragment = pathname_fragment + pathname_part
    except TypeError:
        return False
    else:
        try:
            os.lstat(pathname_fragment)
        except OSError as exc:
            if hasattr(exc, 'winerror'):
                return False
            elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                return False
            return False
        else:
            return True


def is_file_path_valid(file_path: str) -> bool:
    if not is_pathname_valid(file_path):
        return False
    
    return os.path.isfile(file_path)


def is_directory_path_valid(dir_path: str) -> bool:
    if not is_pathname_valid(dir_path):
        return False
    
    return os.path.isdir(dir_path)


def validate_float_value(value: Union[str, float], min_val: Optional[float] = None, 
                        max_val: Optional[float] = None) -> tuple[bool, Optional[float], Optional[str]]:
    try:
        if isinstance(value, str):
            parsed_value = float(value.strip())
        else:
            parsed_value = float(value)
        
        if min_val is not None and parsed_value < min_val:
            return False, None, f"Value must be at least {min_val}"
        
        if max_val is not None and parsed_value > max_val:
            return False, None, f"Value must be at most {max_val}"
        
        return True, parsed_value, None
        
    except (ValueError, TypeError):
        return False, None, "Please enter a valid decimal number"


def validate_int_value(value: Union[str, int], min_val: Optional[int] = None, 
                      max_val: Optional[int] = None) -> tuple[bool, Optional[int], Optional[str]]:
    try:
        if isinstance(value, str):
            parsed_value = int(value.strip())
        else:
            parsed_value = int(value)
        
        if min_val is not None and parsed_value < min_val:
            return False, None, f"Value must be at least {min_val}"
        
        if max_val is not None and parsed_value > max_val:
            return False, None, f"Value must be at most {max_val}"
        
        return True, parsed_value, None
        
    except (ValueError, TypeError):
        return False, None, "Please enter a valid whole number"


def validate_boolean_value(value: Union[str, bool]) -> tuple[bool, Optional[bool], Optional[str]]:
    if isinstance(value, bool):
        return True, value, None
    
    if isinstance(value, str):
        value_lower = value.strip().lower()
        if value_lower in ('true', '1', 'yes', 'on'):
            return True, True, None
        elif value_lower in ('false', '0', 'no', 'off'):
            return True, False, None
    
    return False, None, "Please enter a valid boolean value (true/false, yes/no, 1/0)"


def validate_file_extension(file_path: str, allowed_extensions: list[str]) -> bool:
    if not file_path:
        return False
    
    normalized_extensions = [ext.lower().lstrip('.') for ext in allowed_extensions]
    
    file_ext = os.path.splitext(file_path)[1].lower().lstrip('.')
    
    return file_ext in normalized_extensions


def validate_executable_file(file_path: str) -> bool:
    if not is_file_path_valid(file_path):
        return False
    
    from config.settings import FILE_SETTINGS
    return validate_file_extension(file_path, FILE_SETTINGS['executable_extensions'])


def sanitize_filename(filename: str) -> str:
    if not filename:
        return ""
    
    from config.settings import FILE_SETTINGS
    
    sanitized = filename
    for char in FILE_SETTINGS['invalid_filename_chars']:
        sanitized = sanitized.replace(char, '_')
    
    sanitized = sanitized.strip(' .')
    
    if not sanitized:
        sanitized = FILE_SETTINGS['default_filename']
    
    return sanitized


def validate_path_length(path: str, max_length: int = None) -> bool:
    if max_length is None:
        from config.settings import FILE_SETTINGS
        max_length = FILE_SETTINGS['max_path_length']
    if not path:
        return False
    
    return len(path) <= max_length


def is_writable_directory(dir_path: str) -> bool:
    if not is_directory_path_valid(dir_path):
        return False
    
    try:
        test_file = os.path.join(dir_path, '.write_test')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True
    except (OSError, IOError):
        return False
