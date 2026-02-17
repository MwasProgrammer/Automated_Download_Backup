import os
import json
from modules.discovery import get_source_path

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

    except Exception as e:
        print(f"An error occurred while loading configuration: {e}")
        return
    
    print("Starting main application logic...")

if __name__ == "__main__":
    main()