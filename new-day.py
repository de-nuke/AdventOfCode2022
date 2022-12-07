"""Helper to init directory and files for a new day"""

import datetime
import sys
from pathlib import Path


SCRIPT = """def main():
    result = ...
    with open("input.txt", "r") as f:
        pass

    print(f\"Result: {result}\")
    return result


if __name__ == \"__main__\":
    main()
"""


TEST_TEMPLATE = """
from unittest.mock import patch, mock_open

from .main_part_1 import main as main_1
from .main_part_2 import main as main_2

TEST_INPUT = \"\"\"
\"\"\".strip()

ANSWER_PART_1 = ...
ANSWER_PART_2 = ...


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
"""


def get_dir(day_num, copy_num=0):
    dir_name = f"./day{day_num}({copy_num})" if copy_num else f"./day{day_num}"
    day_dir = Path(dir_name)
    if day_dir.exists():
        return get_dir(day_num, copy_num=copy_num+1)
    else:
        return day_dir


def main():
    if len(sys.argv) > 1:
        day_num = sys.argv[1]
    else:
        day_num = datetime.date.today().day

    day_dir = get_dir(day_num)
    day_dir.mkdir()

    # make input.txt
    (day_dir / "input.txt").touch()
    (day_dir / "__init__.py").touch()

    # make python files
    main_part_1 = day_dir / "main_part_1.py"
    main_part_2 = day_dir / "main_part_2.py"
    tests = day_dir / "tests.py"
    with open(main_part_1, "w") as f:
        f.write(SCRIPT)

    with open(main_part_2, "w") as f:
        f.write(SCRIPT)

    with open(tests, "w") as f:
        f.write(TEST_TEMPLATE)


if __name__ == "__main__":
    main()
