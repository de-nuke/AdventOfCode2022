"""
It seems like there is still quite a bit of duplicate work planned. Instead, the Elves would like to know the number of pairs that overlap at all.

In the above example, the first two pairs (2-4,6-8 and 2-3,4-5) don't overlap, while the remaining four pairs (5-7,7-9, 2-8,3-7, 6-6,4-6, and 2-6,4-8) do overlap:

    5-7,7-9 overlaps in a single section, 7.
    2-8,3-7 overlaps all of the sections 3 through 7.
    6-6,4-6 overlaps in a single section, 6.
    2-6,4-8 overlaps in sections 4, 5, and 6.

So, in this example, the number of overlapping assignment pairs is 4.

In how many assignment pairs do the ranges overlap?


"""

from typing import Tuple, List


def parse_ranges(line: str) -> Tuple[List[int], List[int]]:
    left, right = line.split(",")
    range_left = list(map(int, left.split("-")))
    range_right = list(map(int, right.split("-")))
    range_left = list(range(range_left[0], range_left[1] + 1))
    range_right = list(range(range_right[0], range_right[1] + 1))
    return range_left, range_right


def ranges_intersect(range_1: List[int], range_2: List[int]) -> bool:
    set_1, set_2 = set(range_1), set(range_2)
    return bool(set_1.intersection(set_2) or set_2.intersection(set_1))


def main():
    result = 0
    with open("input.txt", "r") as f:
        for line in f.readlines():
            range_left, range_right = parse_ranges(line)
            if ranges_intersect(range_left, range_right):
                result += 1

    print("Result:", result)
    return result


if __name__ == "__main__":
    main()
