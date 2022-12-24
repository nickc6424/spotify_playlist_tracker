import pytest
import unittest.mock as mock
from scripts import helper_functions as hf


mock_config_file = """
    [section_1]
    attribute_1=abcde
    attribute_2=fghij

    [section_2]
    attribute_3=1234
    """


@mock.patch("builtins.open", new=mock.mock_open(read_data=mock_config_file), create=True)
@pytest.mark.parametrize(
    "section, attribute, expected",
    [
        ("section_1", "attribute_1", "abcde"),
        ("section_1", "attribute_2", "fghij"),
        ("section_2", "attribute_3", "1234"),
    ],
)
def test_read_config(section, attribute, expected):
    """Using a mocked config file, test attributes are read correctly by the function."""
    result = hf.read_config("/dev/null", section, attribute)
    assert result == expected


@mock.patch("builtins.open", new=mock.mock_open(read_data=mock_config_file), create=True)
@pytest.mark.parametrize(
    "section, attribute",
    [
        ("missing_section", "attribute_1"),
        ("section_1", "missing_attribute"),
    ],
)
def test_read_config_exception(section, attribute):
    """Using a mocked config file, test that an exception is raised when attempting to read missing attributes."""
    with pytest.raises(Exception):
        hf.read_config("/dev/null", section, attribute)
