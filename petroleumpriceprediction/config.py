import yaml

def load_config(filepath: str) -> dict:
    """Loads configurations from a YAML file.
    
    Parameters
    ----------
    filepath : str
        Path to the YAML file containing the configuration settings.
    
    Returns
    -------
    dict
        Dictionary containing the loaded configuration data.
    """
    with open(filepath, "r") as file:
        config = yaml.safe_load(file)
    return config
