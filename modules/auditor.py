import os
import hashlib # Import hashlib for file hashing 

def scan_downloads_files(source_path, config):
    forbidden_files = config['safety_measures']['forbidden_extensions'] # List of forbidden file extensions

    all_downloaded_items = os.listdir(source_path) # List all items in the source path

    ready_files = [] # List to store paths of files that are ready for backup
    for item in all_downloaded_items: 
        full_path = os.path.join(source_path, item) 
        if os.path.isfile(full_path): # Check if the item is a file
            file_extension = os.path.splitext(item)[1].lower() 
            if file_extension not in forbidden_files: 
                ready_files.append(full_path) # Add the full path of the file to the list of ready files

    return ready_files

# Hash a file using SHA256 algorithm to generate a unique identifier for the file content
def calculate_file_hash(file_path, chunk_size=8192):
    sha256_hash = hashlib.sha256() # Create a SHA256 hash object
    
    try:
        with open(file_path, 'rb')as f: 
            while chunk := f.read(chunk_size): # Read the file in chunks to handle large files efficiently
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest() # Return the hexadecimal representation of the hash
    except Exception as e:
        print(f"Error calculating hash for {file_path}: {e}")
        return None
    

# Check for duplicate files in the downloads folder 
def duplicate_files_check(ready_files):
    calculated_file_hashes = {} # Dictionary to store file hashes and their corresponding file paths
    duplicate_files = [] # List to store paths of duplicate files

    for file_path in ready_files:
        file_hash = calculate_file_hash(file_path) 
        if file_hash is None:
            continue # Skip files that couldn't be hashed
        if file_hash in calculated_file_hashes:
            duplicate_files.append(file_path)
        else:
            calculated_file_hashes[file_hash] = file_path # Store the file path for the calculated hash
    return duplicate_files