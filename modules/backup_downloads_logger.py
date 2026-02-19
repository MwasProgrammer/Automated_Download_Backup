import logging

# Configure logging for backup downloads
def configure_backup_downloads_logger():
    logging.basicConfig(
        filename = 'backup_downloads.log',
        level = logging.INFO,
        format = '%(asctime)s - %(levelname)s - %(message)s',
    )

    return logging.getLogger('backup_downloads_logger')