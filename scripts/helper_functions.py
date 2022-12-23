import configparser


def read_config(filepath: str, section: str, attribute: str) -> str:
    config = configparser.ConfigParser()
    config.read(filepath)
    return config.get(section, attribute)
