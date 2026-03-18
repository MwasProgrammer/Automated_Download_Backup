from pathlib import Path
import shutil
import logging
from modules.auditor import calculate_file_hash

logger = logging.getLogger('backup_downloads_logger.executor')

def check_disk_space(backup_drive: Path) -> bool:
    total, used, free = shutil.disk_usage(backup_drive)
    free_gb = free // (2**30)
    # Check if free space is less than 1GB
    if free_gb < 1:
        raise OSError(F"Disk storage space critical: Remaining storage space on {backup_drive} is {free_gb}GB!")
    return True 

def get_destination_path(file_path: Path, config: dict, backup_root_path: Path) -> Path:
    file_extension = file_path.suffix.lower()
    categories = config['backup_target'].get('backup_folders', {})

    category_folder = "Others"
    
    for category, extensions in categories.items():
        if file_extension in extensions:
            category_folder = category
            break

    return backup_root_path / category_folder / file_path.name 

# Verify Before Delete Logic
def move_to_backup_drive(source_file: Path, destination_file: Path) -> bool:
    temp_dest = None

    try:
        destination_file.parent.mkdir(parents = True, exist_ok = True) # Ensure the destination directory exists
        temp_dest = destination_file.with_suffix(destination_file.suffix + '.tmp')

        logger.info(f"Stagging: {source_file.name} as {temp_dest.name}")

        shutil.copy2(source_file, temp_dest)
        logger.info(f"Backed up file {source_file.name} to {temp_dest}")

        # Verify the calculated hash, if they match.
        source_hash = calculate_file_hash(source_file)
        temp_hash = calculate_file_hash(temp_dest)

        # Atomic commit or rollback
        if source_hash and source_hash == temp_hash:
            temp_dest.rename(destination_file)

            # Delete files after 100% of Backup verification.
            source_file.unlink()
            logger.info(f"{source_file.name} verified and backed up.")
        
            return True
        else:
            raise ValueError(f"Hash mismatch for {source_file.name} - Integrity failure.")
        
    except Exception as e:
        logger.error(f"Verify Before Delete logic failure for {source_file.name} -> {e}")
        if temp_dest and temp_dest.exists():
            temp_dest.unlink()
            logger.warning(f"Rolled back transaction. File {temp_dest.name} is incomplete or corrupt!")

        return False

    
