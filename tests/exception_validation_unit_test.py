import json
from pathlib import Path
from main import main, load_config
from modules.error_exceptions import ConfigurationError, EnvironmentError
import logging
from modules.backup_downloads_logger import configure_backup_downloads_logger

exception_validation_test_logger = configure_backup_downloads_logger()

def run_exception_validation_test():
    exception_validation_test_logger.info(f"DRY RUN for exception_validation unit test.")
    original_config = ""
    config_path = Path("config.json")


    if config_path.exists():
        original_config = config_path.read_text()
        with open (config_path, "w") as f: 
            f.write("{this_is_corrupt_json}")
    
    try:
        exception_validation_test_logger.info(f"Testing laod configuration with a 'corrupt' version JSON.")
        load_config()

    except Exception as e:
        exception_validation_test_logger.info(f"Successfully caught expected error as {e}")
    
    finally:
        with open (config_path, "w") as f:
            f.write(original_config)

        exception_validation_test_logger.info(f"config.json has been restored successfully.")

        

if __name__ == "__main__":
    run_exception_validation_test()
