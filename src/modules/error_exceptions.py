class BackupError(Exception):
    # Docstring implementation - """..."""
    # #If you were to run help(BackupError), Python would display this exact sentence to the developer.
    """Base class for all backup-related errors."""
    pass

class ConfigurationError(BackupError):
    """USER ERROR: config.json is corrupted."""
    pass

class EnvironmentError(BackupError):
    """ENVIRONMENTAL ERROR (Drive): Backup Drive unplugged, or disk full."""
    pass

class IntegrityError(BackupError):
    """SYSTEM ERROR: SHA-256 mismatch."""
    pass
