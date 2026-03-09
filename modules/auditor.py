import hashlib # Import hashlib for file hashing 
import  logging
from pathlib import Path

logger = logging.getLogger('backup_downloads_logger.auditor')

def scan_downloads_files(source_path: Path, config: dict) -> list[Path]:
    forbidden_files = config['safety_measures'].get('forbidden_extensions', []) # List of forbidden file extensions

    ready_files = [ # List to store paths of files that are ready for backup
        item for item in source_path.iterdir() # Returns Path object
        if item.is_file() and item.suffix.lower() not in forbidden_files
    ]

    logger.info(f"Scanned {len(ready_files)} in {source_path} folder, ready for backup.")

    return ready_files

# Hash a file using SHA256 algorithm to generate a unique identifier for the file content
def calculate_file_hash(file_path: Path, chunk_size: int= 8192) -> str  :
    sha256_hash = hashlib.sha256() # Create a SHA256 hash object
    
    try:
        with open(file_path, 'rb')as f: 
            while chunk := f.read(chunk_size): # Read the file in chunks to handle large files efficiently
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest() # Return the hexadecimal representation of the hash
    except (OSError, IOError) as e:
        logger.error(f"File error hashing {file_path.name}. {e}")
        return ""
    

# Check for duplicate files in the downloads folder 
def duplicate_files_check(ready_files: list[Path]) -> list[Path]:
    calculated_file_hashes = {} # Dictionary to store file hashes and their corresponding file paths
    duplicate_files = [] # List to store paths of duplicate files

    for file_path in ready_files:
        file_hash = calculate_file_hash(file_path) 
        if not file_hash.strip():
            continue 
        if file_hash in calculated_file_hashes:
            logger.warning(f"Duplicate file {file_path.name} matches {calculated_file_hashes[file_hash].name}")
            duplicate_files.append(file_path)
        else:
            calculated_file_hashes[file_hash] = file_path # Store the file path for the calculated hash
    return duplicate_files