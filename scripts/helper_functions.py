import configparser


def read_config(filepath: str, section: str, attribute: str) -> str:
    """Reads a specific attribute from a config file."""
    config = configparser.ConfigParser()
    config.read(filepath)
    return config.get(section, attribute)
