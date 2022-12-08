from unittest.mock import mock_open, patch

from .main_part_1 import main as main_1
from .main_part_2 import main as main_2

TEST_INPUT = """
30373
25512
65332
33549
35390
""".strip()

ANSWER_PART_1 = 21
ANSWER_PART_2 = 8


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
