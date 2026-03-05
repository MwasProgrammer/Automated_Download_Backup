import logging
import sys
from datetime import datetime
# Configure logging for backup downloads
def configure_backup_downloads_logger():
    logger = logging.getLogger('backup_downloads_logger')
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers(): 
        log_filename = f"backup_downloads_{datetime.now().strftime('%Y-%m-%d')}.log" # Log file name with current date 

        file_handler = logging.FileHandler(log_filename) # Create a file handler to write logs to a file
        stream_handler = logging.StreamHandler(sys.stdout)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler) 
        logger.addHandler(stream_handler)

    return logger
