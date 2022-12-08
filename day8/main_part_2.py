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
