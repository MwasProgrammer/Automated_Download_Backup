import sqlite3
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger('backup_downloads_logger.database')

class BackupDatabase:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute