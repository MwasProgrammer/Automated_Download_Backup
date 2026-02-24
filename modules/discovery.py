import os

def get_source_path(config): # The user downloads
    target_directory_name = config['source_settings']['target_directory_name'] 
    is_sandbox_mode = config['source_settings'].get('sandbox_mode', False)

    if is_sandbox_mode:
        print("Sandbox mode enabled. Using sandbox directory for source path.")
        target_directory_path = config['source_settings'].get('target_directory_path')
        source_path = os.path.abspath(target_directory_path)

    else:
        source_path = os.path.join(os.path.expanduser('~'), target_directory_name) 

    return source_path