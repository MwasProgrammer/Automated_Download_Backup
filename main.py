import json
import logging 
from pathlib import Path
from modules.discovery import get_source_path, get_drive_by_label
from modules.auditor import scan_downloads_files, calculate_file_hash
from modules.executor import check_disk_space, get_destination_path, move_to_backup_drive
from modules.database import BackupDatabase
from modules.backup_downloads_logger import configure_backup_downloads_logger

def load_config() -> dict: # Load cofiguration from config.json
    config_path = Path(__file__).parent / 'config.json'

    try:
        with open(config_path, 'r') as f:
            return json.load(f)
        
    except Exception as e:
        raise RuntimeError(f"Could not load configuration file config.json: {e}")
        
def resolve_backup_root(config: dict) -> Path:
    target_config = config['backup_target']
    if config ['source_settings'].get('sandbox_mode'):
        return Path(target_config['backup_directory_path']).resolve() 
    
    drive_label = target_config.get('volume_label', 'BACKUP_DRIVE')
    found_drive = get_drive_by_label(drive_label)
    
    if not found_drive:
        raise OSError(f"Error: Drive with label {drive_label} not found!")
    
    return found_drive / target_config['backup_directory_name']

def process_single_file(file_path, config, backup_root, db, logger):
    try:
        f_hash = calculate_file_hash(file_path)
        if not f_hash:
            return
        
        if db.is_already_processed(f_hash):
            logger.info(f"Skipping file {file_path.name }. This file is already backed up!")
            return
        
        destination_path = get_destination_path(file_path, config, backup_root)

        if move_to_backup_drive(file_path, destination_path):

            db.mark_as_processed(f_hash, file_path.name, source_path = file_path.parent)

    except Exception as e:
        logger.error(f"Error: Backup cancelled for file {file_path.name}: {e}")


def main():
    logger = configure_backup_downloads_logger()
    logger.info(f"Loading configuration...")
    logger.info("Configurations loaded successfully. Starting backup process.")

    try:
        configuration = load_config() # Load configuration from config.json
        logger.info(f"Configuration loaded successfully: {configuration ['project_name']} version {configuration ['version']}")
    
        db_path = Path(__file__).parent / "back_history.db"
        db = BackupDatabase(db_path)

        source = get_source_path(configuration)
        backup_root = resolve_backup_root(configuration)

        if not source.exists():
            logger.error(f"The source directory {source} not found!")

            return
        
        check_disk_space(backup_root)
        backup_root.mkdir(parents = True, exist_ok =True)

        files_to_process = scan_downloads_files(source, configuration)

        for file in files_to_process:
            process_single_file(file, configuration, backup_root, db, logger)

    except (RuntimeError, OSError) as e:
        logger.critical(f"System halt: {e}")

    except Exception as e:
        logger.error(f"System unexcepted error: {e}")

    finally:
        logger.info(f"Back up complete successfully!")

if __name__ == "__main__":
        main()

        