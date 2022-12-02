"""
The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the round needs
to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round
ends as indicated. The example above now goes like this:

    In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y), so you also
    choose Rock. This gives you a score of 1 + 3 = 4.
    In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with
    a score of 1 + 0 = 1.
    In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.

Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.

Following the Elf's instructions for the second column, what would your total score be if everything goes exactly
according to your strategy guide?

https://adventofcode.com/2022/day/2#part2
"""

from typing import Tuple

ROCK = "A"
PAPER = "B"
SCISSORS = "C"
LOSS = "X"
DRAW = "Y"
VICTORY = "Z"

SHAPES = [ROCK, PAPER, SCISSORS]
EXPECTED_RESULT = [LOSS, DRAW, VICTORY]

OUTCOME_POINTS = {LOSS: 0, DRAW: 3, VICTORY: 6}
POINTS_MAP = {ROCK: 1, PAPER: 2, SCISSORS: 3}


# Winner over Rock is Paper, winner over paper are Scissors and winner over Scissors is Rock
WINNER_OVER = {
    ROCK: PAPER,
    PAPER: SCISSORS,
    SCISSORS: ROCK,
}
LOSER_TO = {value: key for key, value in WINNER_OVER.items()}


def parse_shapes(line: str) -> Tuple[str, str]:
    enemy_shape, expected_outcome = line.strip().split(" ")
    assert enemy_shape in SHAPES
    assert expected_outcome in EXPECTED_RESULT
    return enemy_shape, expected_outcome


def get_my_shape_expected(enemy_shape: str, expected_outcome: str) -> str:
    if expected_outcome == LOSS:
        return LOSER_TO[enemy_shape]
    elif expected_outcome == VICTORY:
        return WINNER_OVER[enemy_shape]
    else:
        return enemy_shape


def calculate_round_points(enemy_shape: str, expected_outcome: str) -> int:
    my_shape = get_my_shape_expected(enemy_shape, expected_outcome)
    battle_points = OUTCOME_POINTS[expected_outcome]
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
