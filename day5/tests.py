from unittest.mock import mock_open, patch

from .main_part_1 import main as main_1
from .main_part_2 import main as main_2

TEST_INPUT = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
TEST_INPUT = TEST_INPUT[1:-1]

ANSWER_PART_1 = "CMZ"
ANSWER_PART_2 = "MCD"


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
