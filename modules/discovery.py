from pathlib import Path
import string 
import ctypes # Import ctypes for Windows API calls to check drive types
import logging

logger = logging.getLogger('backup_downloads_logger.discovery') 
DRIVE_REMOVABLE = 3
DRIVE_FIXED = 2 

def get_drive_by_label(target_label: str = "AUTO") -> Path:
    bitmask = ctypes.windll.kernel32.GetLogicalDrives() # Get a bitmask of all logical drives

    system_drive = Path.home().drive.upper()
    fallback_drive = None

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
                if target_label != "AUTO" and volume_name.value.upper() == target_label.upper():
                    logger.debug(f"Drive discovery: Found '{target_label}' at {drive}")
                    return Path (drive)
            
                if fallback_drive is None:
                    fallback_drive = Path(drive)
                        
        bitmask >>= 1 # Shift the bitmask to check the next drive
        
    if fallback_drive:
        logger.info(f"Drive Discovery: Using AutoDrive at {fallback_drive}")
        return fallback_drive
    
    return None 


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