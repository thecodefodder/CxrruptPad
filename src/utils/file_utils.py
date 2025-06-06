import os
import json
import shutil

def ensure_dir_exists(directory):
    """Ensure that a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    return directory

def get_data_dir():
    """Get the data directory for storing application data."""
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
    return ensure_dir_exists(base_dir)

def get_sounds_dir():
    """Get the sounds directory for storing sound files."""
    sounds_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "sounds")
    return ensure_dir_exists(sounds_dir)

def get_tab_dir(tab_name=None):
    """
    Get the directory for tabs or a specific tab's sounds.
    
    If tab_name is provided, returns the path to that specific tab's directory.
    If tab_name is None, returns the main tabs directory.
    """
    # Get the main sounds directory
    sounds_dir = get_sounds_dir()
    
    # If no tab name is provided, return the main sounds directory
    if tab_name is None:
        return sounds_dir
    
    # Otherwise, return the specific tab directory
    tab_dir = os.path.join(sounds_dir, tab_name)
    return ensure_dir_exists(tab_dir)

def save_json(file_path, data):
    """Save data to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def load_json(file_path, default=None):
    """Load data from a JSON file, returning default if file not found."""
    if not os.path.exists(file_path):
        return default if default is not None else {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return default if default is not None else {}

def get_tab_favorites_path(tab_name):
    """Get the path to a tab's favorites file."""
    data_dir = get_data_dir()
    return os.path.join(data_dir, f"{tab_name}_favorites.json")

def get_app_settings_path():
    """Get the path to the application settings file."""
    data_dir = get_data_dir()
    return os.path.join(data_dir, "settings.json")

def create_safe_filename(name):
    """Create a safe filename from the given name."""
    return "".join([c for c in name if c.isalpha() or c.isdigit() or c in ' -_']).strip()

def delete_file_safely(file_path):
    """Safely delete a file if it exists."""
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except:
            return False
    return False

def move_file_safely(src_path, dst_path, copy=False):
    """
    Safely move or copy a file, creating any necessary directories.
    
    Args:
        src_path: Source file path
        dst_path: Destination file path
        copy: If True, copy the file instead of moving it
    """
    if not os.path.exists(src_path):
        return False
    
    dst_dir = os.path.dirname(dst_path)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir, exist_ok=True)
    
    try:
        if copy:
            shutil.copy2(src_path, dst_path)
        else:
            shutil.move(src_path, dst_path)
        return True
    except Exception:
        return False 