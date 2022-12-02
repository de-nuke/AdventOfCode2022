"""Helper to init directory and files for a new day"""

import datetime
import sys
from pathlib import Path


SCRIPT = """def main():
    with open("input.txt", "r") as f:
        pass


if __name__ == \"__main__\":
    main()
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

    # make python files
    main_part_1 = day_dir / "main-part-1.py"
    main_part_2 = day_dir / "main-part-2.py"
    with open(main_part_1, "w") as f:
        f.write(SCRIPT)

    with open(main_part_2, "w") as f:
        f.write(SCRIPT)


if __name__ == "__main__":
    main()
