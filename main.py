import os
import json
from modules.discovery import get_source_path
from modules.auditor import scan_downloads_files, duplicate_files_check

def load_config(): # Load cofiguration from config.json
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Error: 'config.json' not found in {config_path}")

    with open(config_path, 'r') as f:
        return json.load(f)
    
def main():
    print("Loading configuration...")

    try:
        configuration = load_config()
        print(f"Configuration loaded successfully: {configuration ['project_name']} version {configuration ['version']}")
    
        print("Discovering source path...")
        source_path =get_source_path(configuration)

        if os.path.exists(source_path):
            print(f"Source path discovered: {source_path}")
        else:
            print(f"Error: Source path not found: {source_path}")

        print("Scanning downloads folder for files ready for backup...")
        ready_files_for_backup = scan_downloads_files(source_path, configuration)
        print(f"Found {len(ready_files_for_backup)} files ready for backup.")

        # View files ready for backup (top 3 files and bottom 3 files)
        if ready_files_for_backup:
            print("Top 3 files ready for backup:")
            for i, file in enumerate(ready_files_for_backup[:3]):
                print(f"  {i+1}. {os.path.basename(file)}")

            if len(ready_files_for_backup) > 3:
                print("Bottom 3 files ready for backup:")
                for i, file in enumerate(ready_files_for_backup[-3:], start=len(ready_files_for_backup)-2):
                    print(f"  {i}. {os.path.basename(file)}")

        print("Checking for duplicate files in the downloads folder...")
        duplicate_files = duplicate_files_check(source_path)
        if duplicate_files:
            print(f"Found {len(duplicate_files)} duplicate files:")
            for file in duplicate_files:
                print(f"  - {os.path.basename(file)}")
        else:
            print("No duplicate files found.")

    except Exception as e:
        print(f"An error occurred while loading configuration: {e}")
        return
    
    #print("Starting main application logic...")

if __name__ == "__main__":
    main()