from unittest.mock import patch, mock_open
from scripts import load


def read_config_side_effect_func(filepath: str, section: str, attribute: str):
    if attribute == "host":
        return "host_response"
    elif attribute == "user":
        return "user_response"
    elif attribute == "password":
        return "password_response"
    elif attribute == "dbname":
        return "dbname_response"
    elif attribute == "port":
        return "port_response"


@patch("scripts.load.read_config")
def test_read_db_connection(mock_read_config):
    mock_read_config.side_effect = read_config_side_effect_func
    expected_result = {
        "host": read_config_side_effect_func("secrets.cfg", "database", "host"),
        "user": read_config_side_effect_func("secrets.cfg", "database", "user"),
        "password": read_config_side_effect_func("secrets.cfg", "database", "password"),
        "dbname": read_config_side_effect_func("secrets.cfg", "database", "dbname"),
        "port": read_config_side_effect_func("secrets.cfg", "database", "port"),
    }
    assert load.read_db_connection() == expected_result


@patch("builtins.open", new_callable=mock_open, read_data="SELECT * FROM table_name")
def test_get_sql_from_script(mock_file):
    assert load.get_sql_from_script("path/to/open") == "SELECT * FROM table_name"
