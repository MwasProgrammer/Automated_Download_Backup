import os
import shutil

def check_disk_space(backup_drive):
    total, used, free = shutil.disk_usage(backup_drive)
    free_gb = free // (2**30)
    # Check if free space is less than 1GB
    if free_gb < 1:
        raise OSError(F"Disk storage space critical: Remaining storage space on {backup_drive} is {free_gb}GB!")
    return True

def get_destination_path(file_path, config):
    file_extension = os.path.splitext(file_path)[1].lower()
    categories = config['backup_target'].get('backup_folders', {})

    category_folder = "Others"
    
    for category, extensions in categories.items():
        if file_extension in extensions:
            category_folder = category
            break
    
    if config['source_settings'].get('sandbox_mode'):
        backup_root = config['backup_target']['backup_directory_path'] # Use the specified backup directory path in sandbox mode
    else:
        backup_root = os.path.join("D:/", config['backup_target']['backup_directory_name']) 

    return os.path.join(backup_root, category_folder,os.path.basename(file_path))

def move_to_backup_drive(source_file, destination_file):
    os.makedirs(os.path.dirname(destination_file), exist_ok=True) # Ensure the destination directory exists

    shutil.move(source_file, destination_file)
    print(f"Backed up file {os.path.basename(source_file)} to {os.path.dirname(destination_file)}")
