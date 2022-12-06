from unittest.mock import mock_open, patch

from .main_part_1 import main as main_1
from .main_part_2 import main as main_2

TEST_INPUTS_1 = [
    "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "nppdvjthqldpwncqszvftbrmjlhg",
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
]

TEST_INPUTS_2 = [
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
    "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "nppdvjthqldpwncqszvftbrmjlhg",
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
]

ANSWERS_PART_1 = [5, 6, 10, 11]
ANSWERS_PART_2 = [19, 23, 23, 29, 26]


def test_part_1():
    for i, test_input in enumerate(TEST_INPUTS_1):
        with patch("builtins.open", new_callable=mock_open, read_data=test_input) as mock_file:
            result = main_1()
            mock_file.assert_called_with("input.txt", "r")
            assert result == ANSWERS_PART_1[i]


def test_part_2():
    for i, test_input in enumerate(TEST_INPUTS_2):
        with patch("builtins.open", new_callable=mock_open, read_data=test_input) as mock_file:
            result = main_2()
            mock_file.assert_called_with("input.txt", "r")
            assert result == ANSWERS_PART_2[i]
