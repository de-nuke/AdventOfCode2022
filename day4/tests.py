from unittest.mock import mock_open, patch

from .main_part_1 import main as main_1
from .main_part_2 import main as main_2

TEST_INPUT = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""".strip()

ANSWER_PART_1 = 2
ANSWER_PART_2 = 4


@patch("builtins.open", new_callable=mock_open, read_data=TEST_INPUT)
def test_part_1(mock_file):
    result = main_1()

    mock_file.assert_called_with("input.txt", "r")
    assert result == ANSWER_PART_1


@patch("builtins.open", new_callable=mock_open, read_data=TEST_INPUT)
def test_part_2(mock_file):
    result = main_2()

    mock_file.assert_called_with("input.txt", "r")
    assert result == ANSWER_PART_2
