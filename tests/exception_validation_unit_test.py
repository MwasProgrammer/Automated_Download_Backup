import json
import os
from pathlib import Path
from main import main, load_config
from modules.error_exceptions import ConfigurationError, EnvironmentError
import logging

logger = logging.getLogger('backup_downloads_logger')

def run_exception_validation_test():
    logger.info(f"DRY RUN for exception_validation unit test.")
    original_config = ""
    config_path = Path("config.json")


    if config_path.exists():
        original_config = config_path.read_text()
        with open (config_path, "w") as f:
            f.write("{this_is_corrupt_json}")
    
    try:
        logger.info(f"Testing laod configuration with a 'corrupt' version JSON.")
        load_config()

    except Exception as e:
        logger.info(f"Successfully caught expected error as {e}")
        
