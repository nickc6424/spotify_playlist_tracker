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
    # You can mock the builtin open function that will return a StringIO with config file contents if /config/program.cfg is being opened
    result = hf.read_config("/dev/null", section, attribute)
    assert result == expected
