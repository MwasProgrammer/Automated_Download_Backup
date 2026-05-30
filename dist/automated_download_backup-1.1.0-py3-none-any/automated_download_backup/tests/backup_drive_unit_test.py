import json
from pathlib import Path
from main import main, load_config
from modules.backup_downloads_logger import configure_backup_downloads_logger

backup_drive_test_logger = configure_backup_downloads_logger()

def run_backup_drive_test():
    backup_drive_test_logger.info(f"Testing for missing backup drive simulation.")
    config_path = Path("config.json")
    original_config = config_path.read_text()
    test_config = json.loads(original_config)
    test_config['backup_target']['volume_label'] = "Missing_Backup_Drive"

    with open (config_path, "w") as f:
        json.dump(test_config, f)

    backup_drive_test_logger.info(f"Run main() with the 'missing drive'.")
    try:
        main()

    except Exception as e:
        backup_drive_test_logger.info(f"Error testing for missing drive: {e}")

    finally:
        with open(config_path, "w") as f:
            f.write(original_config)

        backup_drive_test_logger.info(f"Backup Target Drive restored successfully.")

if __name__ == "__main__":
    run_backup_drive_test()