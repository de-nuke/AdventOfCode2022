"""
The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for
each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for
Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get if
you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z

This strategy guide predicts and recommends the following:

    In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for you
    with a score of 8 (2 because you chose Paper + 6 because you won).
    In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a loss for
    you with a score of 1 (1 + 0).
    The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.

In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?

https://adventofcode.com/2022/day/2
"""

from typing import Tuple

# rock = A/X, paper = B/Y, scissors = C/Z
ENEMY_SHAPES = ["A", "B", "C"]
MY_SHAPES = ["X", "Y", "Z"]

LOSS_POINTS = 0
DRAW_POINTS = 3
VICTORY_POINTS = 6

POINTS_MAP = {"X": 1, "Y": 2, "Z": 3}

WINNER_OVER = {
    "A": "Y",
    "B": "Z",
    "C": "X",
    "X": "B",
    "Y": "C",
    "Z": "A",
}


def parse_shapes(line: str) -> Tuple[str, str]:
    enemy_shape, my_shape = line.strip().split(" ")
    assert enemy_shape in ENEMY_SHAPES
    assert my_shape in MY_SHAPES
    return enemy_shape, my_shape


def battle_result(enemy_shape: str, my_shape: str) -> int:
    if ENEMY_SHAPES.index(enemy_shape) == MY_SHAPES.index(my_shape):
        return DRAW_POINTS
    if my_shape == WINNER_OVER[enemy_shape]:
        return VICTORY_POINTS
    else:
        return LOSS_POINTS


def calculate_round_points(enemy_shape: str, my_shape: str) -> int:
    battle_points = battle_result(enemy_shape, my_shape)
    my_shape_points = POINTS_MAP[my_shape]
    return battle_points + my_shape_points


def main():
    total = 0
    with open("input.txt", "r") as f:
        for line in f.readlines():
            enemy_shape, my_shape = parse_shapes(line)
            round_points = calculate_round_points(enemy_shape, my_shape)
            total += round_points
            print(line.strip(), "->", round_points)
    print("Total points:", total)
    return total


if __name__ == "__main__":
    main()
