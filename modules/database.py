import sqlite3
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger('backup_downloads_logger.database')

class BackupDatabase:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('PRAGMA journal_mode = WAL;')

                cursor = conn.cursor()
                cursor.execute ('''
                        CREATE TABLE IF NOT EXISTS processed_files (
                                file_hash TEXT PRIMARY KEY, 
                                file_name TEXT,
                                source_path TEXT,
                                backup_date TEXT
                                )
                                ''')
                conn.commit()
        
        except sqlite3.Error as e:
            logger.error(f"Database Initialization failed! {e}") 
                
                
    def is_already_processed (self, file_hash: str) -> bool:
        if not file_hash: return False

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor. execute ('SELECT 1  FROM processed_files WHERE file_hash = ?', (file_hash,))
                return cursor.fetchone() is not None
            
        except sqlite3.Error as e:
            logger.error(f"Error checking File Hash {file_hash[:8]}: {e}")
            return False
    
    def mark_as_processed (self, file_hash: str, file_name: str, source_path: str = "Unknown"):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT OR IGNORE INTO processed_files (file_hash, file_name, source_path, backup_date)
                               VALUES (?, ?, ?, ?)
                               ''', (file_hash, file_name, str(source_path), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                conn.commit()
        

        except sqlite3.Error as e:
            logger.error(f"Failed to record backup file hash for {file_name}: {e}")
