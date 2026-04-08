from pathlib import Path
import string 
import ctypes # Import ctypes for Windows API calls to check drive types
import logging

logger = logging.getLogger('backup_downloads_logger.discovery') 
DRIVE_REMOVABLE = 2
DRIVE_FIXED = 3 

def list_available_drives() -> dict:
    bitmask = ctypes.windll.kernel32.GetLogicalDrives() # Get a bitmask of all logical drives

    system_drive = Path.home().drive.upper()
    found_drives = {}

    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drive = f"{letter}:\\"
            
            if f"{letter}:" == system_drive:
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