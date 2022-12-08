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
