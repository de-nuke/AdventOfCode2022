"""
--- Part Two ---

Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house:
they would like to be able to see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an
edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on
the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large
eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390

    Looking up, its view is not blocked; it can see 1 tree (of height 3).
    Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
    Looking right, its view is not blocked; it can see 2 trees.
    Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that
    blocks its view).

A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this
tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390

    Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
    Looking left, its view is not blocked; it can see 2 trees.
    Looking down, its view is also not blocked; it can see 1 tree.
    Looking right, its view is blocked at 2 trees (by a massive tree of height 9).

This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?

https://adventofcode.com/2022/day/8#part2
"""
from typing import List


def get_line_score(tree: int, other_trees: List[int]) -> int:
    """
    Calculate a scenic score of a tree in one direction (i.e. based on one line of trees).

    Scenic score of a tree line is the number of trees between the main tree and the nearest tree that is higher
    or of the same height (including that tree)
    """
    # If tree line is empty (i.e. tree is on the edge) then score is 0
    if not other_trees:
        return 0

    i = 1  # avoiding "referenced before assignment" warning

    for i, other_tree in enumerate(other_trees, start=1):
        if other_tree >= tree:
            break
    return i


def calculate_scenic_score(row_idx: int, col_idx: int, grid: List[List[int]]) -> int:
    """Calculate total scenic score for a tree by multiplying scenic score for each direction.

    Line of trees in a certain direction consists of all trees between the investigated tree and an edge in this
    direction, ordered by the distance from the investigated tree::

        [ ] [ ] [↑] [ ] [ ]

        [ ] [ ] [↑] [ ] [ ]

        [←] [←] [T] [→] [→]

        [ ] [ ] [↓] [ ] [ ]

        [ ] [ ] [↓] [ ] [ ]

    """
    trees_above = [grid[tmp_row_idx][col_idx] for tmp_row_idx in reversed(range(0, row_idx))]
    trees_below = [grid[tmp_row_idx][col_idx] for tmp_row_idx in range(row_idx + 1, len(grid))]
    trees_on_left = [grid[row_idx][tmp_col_idx] for tmp_col_idx in reversed(range(0, col_idx))]
    trees_on_right = [grid[row_idx][tmp_col_idx] for tmp_col_idx in range(col_idx + 1, len(grid[row_idx]))]

    tree = grid[row_idx][col_idx]
    return (
        get_line_score(tree, trees_above)
        * get_line_score(tree, trees_below)
        * get_line_score(tree, trees_on_left)
        * get_line_score(tree, trees_on_right)
    )


def find_highest_scenic_score(grid: List[List[int]]) -> int:
    """Calculate scenic score for each tree and find the highest one"""
    max_score = 0

    for row_idx, row in enumerate(grid):
        for col_idx, col in enumerate(row):
            score = calculate_scenic_score(row_idx, col_idx, grid)
            if score > max_score:
                max_score = score
    return max_score


def main() -> int:
    grid = []
    with open("input.txt", "r") as f:
        for line in f.readlines():
            grid.append(list(map(int, line.strip())))

    result = find_highest_scenic_score(grid)
    print(f"Result: {result}")
    return result


if __name__ == "__main__":
    main()
