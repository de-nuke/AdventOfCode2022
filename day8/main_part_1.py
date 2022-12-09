"""
--- Day 8: Treetop Tree House ---

The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a
previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location
for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the
number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For
example:

30373
25512
65332
33549
35390

Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees
in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to
block the view. In this example, that only leaves the interior nine trees to consider:

    The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of
    height 5 are in the way.)
    The top-middle 5 is visible from the top and right.
    The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of
    height 0 between it and an edge.
    The left-middle 5 is visible, but only from the right.
    The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most
    height 2 between it and an edge.
    The right-middle 3 is visible from the right.
    In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this
arrangement.

Consider your map; how many trees are visible from outside the grid?

https://adventofcode.com/2022/day/8
"""
from typing import List


def is_visible_from_top(row_idx: int, col_idx: int, grid: List[List[int]]) -> bool:
    """
    Check if the investigated tree is higher than any tree above it. If it is, then it is visible from the top edge.
    """
    trees_above = [grid[tmp_row_idx][col_idx] for tmp_row_idx in range(0, row_idx)]
    return (max(trees_above) < grid[row_idx][col_idx]) if trees_above else True


def is_visible_from_bottom(row_idx: int, col_idx: int, grid: List[List[int]]) -> bool:
    """
    Check if the investigated tree is higher than any tree below it. If so, it's visible from the bottom edge.
    """
    trees_below = [grid[tmp_row_idx][col_idx] for tmp_row_idx in range(row_idx + 1, len(grid))]
    return (max(trees_below) < grid[row_idx][col_idx]) if trees_below else True


def is_visible_from_left(row_idx: int, col_idx: int, grid: List[List[int]]) -> bool:
    """
    Check if the investigated tree is higher than any tree to the left of it. If so, it's visible from the left edge.
    """
    trees_on_left = [grid[row_idx][tmp_col_idx] for tmp_col_idx in range(0, col_idx)]
    return (max(trees_on_left) < grid[row_idx][col_idx]) if trees_on_left else True


def is_visible_from_right(row_idx: int, col_idx: int, grid: List[List[int]]) -> bool:
    """
    Check if the investigated tree is higher than any tree to the right of it. If so, it's visible from the right edge.
    """
    trees_on_right = [grid[row_idx][tmp_col_idx] for tmp_col_idx in range(col_idx + 1, len(grid[row_idx]))]
    return (max(trees_on_right) < grid[row_idx][col_idx]) if trees_on_right else True


def count_visible_trees(grid: List[List[int]]) -> int:
    """Count how many trees are visible from outside the grid (from at least one direction).

    A tree is "visible" if there aren't any trees between it and the edge that are higher or of the same height. Trees
    on the edges are always visible.
    """
    n_visible_trees = 0

    for row_idx, row in enumerate(grid):
        for col_idx, col in enumerate(row):
            is_visible = (
                is_visible_from_top(row_idx, col_idx, grid)
                or is_visible_from_bottom(row_idx, col_idx, grid)
                or is_visible_from_left(row_idx, col_idx, grid)
                or is_visible_from_right(row_idx, col_idx, grid)
            )
            n_visible_trees += is_visible  # True is 1, False is 0

    return n_visible_trees


def main() -> int:
    grid = []
    with open("input.txt", "r") as f:
        for line in f.readlines():
            grid.append(list(map(int, line.strip())))

    result = count_visible_trees(grid)
    print(f"Result: {result}")
    return result


if __name__ == "__main__":
    main()
