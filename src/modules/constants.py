from enum import Enum, auto

class BackupStatus(Enum):
    BACKUP_SUCCESS = auto()
    SKIPPED = auto()
    FAILED = auto()
    DISK_FULL = auto()
    NOT_FOUND = auto()