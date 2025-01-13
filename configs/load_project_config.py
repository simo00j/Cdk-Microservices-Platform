import json

def load_config(config_file='configs/project_config.json'):
    """
    Load the project configuration from a JSON file.

    Args:
    - config_file (str): The path to the configuration file. Defaults to 'project_config.json'.

    Returns:
    - dict: The configuration data as a dictionary.
    """
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
            return config.get('projects', [])
    except OSError as e:
        print(f"Error opening or reading the configuration file: {config_file}. Error: {e}")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the configuration file: {config_file}")
        return []
