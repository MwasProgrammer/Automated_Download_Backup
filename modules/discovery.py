from pathlib import Path
import platform
import os
import logging

logger = logging.getLogger('backup_downloads_logger.discovery') 
DRIVE_REMOVABLE = 2
DRIVE_FIXED = 3 

def list_available_drives() -> dict:
    found_drives = {}
    current_os = platform.system()

    if current_os == "Windows":
        import ctypes
        import string

        DRIVE_REMOVABLE = 2
        DRIVE_FIXED = 3

        bitmask = ctypes.windll.kernel32.GetLogicalDrives() # Get a bitmask of all logical drives

        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drive = f"{letter}:\\"
                
                if f"{letter}:" == Path.home().drive:
                    bitmask >>= 1
                    continue

                drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive)
                
                if drive_type not in (DRIVE_REMOVABLE, DRIVE_FIXED):
                    bitmask >>= 1
                    continue

                volume_name = ctypes.create_unicode_buffer(1024)
                drive_results = ctypes.windll.kernel32.GetVolumeInformationW(
                    drive, volume_name, 1024, None, None, None, None, 0
                )

                if drive_results: 
                    disk_label = volume_name.value if volume_name.value else "UNTITLED"
                    found_drives[disk_label.upper()] = Path(drive)
                    
            bitmask >>= 1 # Shift the bitmask to check the next drive

    elif current_os == "Linux":
        user_name = Path.home().name
        search_paths = [Path("/media") / user_name, Path("/mnt")]
        
        for base_bath in search_paths:
            if base_bath.exists():
                for entry in base_bath.iterdir():
                    if entry.is_dir() and os.path.ismount(entry):
                        found_drives[entry.name.upper()] = entry.resolve()
        
                
    return found_drives

def get_drive_by_label(target_label: str = "AUTO") -> Path:
    available_drives = list_available_drives()

    if not available_drives:
        logger.error(f"BACKUP DRIVE NOT FOUND!")
        return None
    
    if target_label != "Auto":
        target_upper =  target_label.upper()
        if target_upper in available_drives:
            logger.info(f"Target Backup Drive {target_label} found at {available_drives[target_upper]}")
            return available_drives[target_upper] 
        return None 
    
    first_label = list(available_drives.keys())[0]
    logger.info(f"Autoselect: The firstBackup drive detected is {first_label}")
    return available_drives[first_label]
    
def get_source_path(config: dict) -> Path: # The user downloads
    source_settings = config.get('source_settings', {})
    is_sandbox_mode = source_settings.get('sandbox_mode', False)
    

    if is_sandbox_mode:
        logger.warning("Sandbox mode active. Using relative pathing.")
        raw_path = source_settings.get('target_directory_path', 'test/sandbox/downloads' )
        source_path = Path(raw_path).resolve()

    else:
        target_name = source_settings.get('target_directory_name', 'Downloads')
        source_path = Path.home() / target_name 

        logger.info(f"Production source path identified: {source_path}")

    return source_path