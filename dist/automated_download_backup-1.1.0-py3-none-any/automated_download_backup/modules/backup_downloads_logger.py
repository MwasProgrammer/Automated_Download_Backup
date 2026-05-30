import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
# Configure logging for backup downloads
def configure_backup_downloads_logger():
    logger = logging.getLogger('backup_downloads_logger')
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers(): 
        logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    console_handler.setFormatter(console_format)

    log_directory = Path(__file__).parent.parent / "Logs"
    log_directory.mkdir(exist_ok = True)
    log_file = log_directory / "backup_details.log"

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes= 1024 * 1024,
        backupCount= 5

    )

    file_handler.setLevel(logging.DEBUG)

    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler) 
    logger.addHandler(file_handler)

    return logger
