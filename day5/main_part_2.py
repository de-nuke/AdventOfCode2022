"""
As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away.
The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder,
and the ability to pick up and move multiple crates at once.

Again considering the example above, the crates begin in the same configuration:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3

However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the same
order, resulting in this new configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3

Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3

Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3

In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be
ready to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of each
stack?

https://adventofcode.com/2022/day/5#part2
"""
import re
from typing import List, Optional

# How many characters crate representations takes
CRATE_REPR_LENGTH = 3

CRATE_REGEX = re.compile(r"\[(?P<crate_name>[a-zA-Z])\]")
MOVE_REGEX = re.compile(r"move (?P<crates_number>\d+) from (?P<source_stack>\d+) to (?P<dest_stack>\d+)")


class Stack:
    def __init__(self):
        self.crates = []

    def put(self, crate: str):
        self.crates.append(crate)

    def put_many(self, crates: List[str]):
        self.crates.extend(crates)

    def remove(self):
        return self.crates.pop() if self.crates else None

    def remove_many(self, n=1):
        crates_removed, crates_left = self.crates[-n:], self.crates[:-n]
        self.crates = crates_left
        return crates_removed

    def get_top(self):
        return self.crates[-1]

    def repr(self, vertical=True):
        repr_str = ""
        sep = "\n" if vertical else ""
        for crate in reversed(self.crates):
            repr_str += f"[{crate}]" + sep
        if not vertical:
            repr_str += "\n"
        return repr_str

    def __str__(self):
        return self.repr(vertical=False)


def line_splitter(line: str):
    """Split line (by space char) into string parts with a given length (CRATE_REPR_LENGTH)."""
    pos_start = 0
    line = line.replace("\n", "")
    pos_end = pos_start + CRATE_REPR_LENGTH
    while pos_end <= len(line):
        yield line[pos_start:pos_end]
        pos_start = pos_end + 1  # Adding extra "one" to skip a space between crate representations


def parse_crates_layer(line: str) -> List[Optional[str]]:
    """Convert a string line into a list with crate names or Nones"""
    layer = []
    for part in line_splitter(line):
        match = CRATE_REGEX.match(part)
        if match:
            layer.append(match.group("crate_name"))
        else:
            layer.append(None)
    return layer


def make_stacks(crates_layers, num_of_stacks):
    """Transform list of crate layers into crate stacks"""
    stacks = [Stack() for _ in range(num_of_stacks)]
    for layer in reversed(crates_layers):  # insert from bottom to the top
        for stack_idx, crate in enumerate(layer):
            stack = stacks[stack_idx]
            if crate:
                stack.put(crate)
    return stacks


def parse_move(line: str):
    """Parse "move" line to get number of crates to move, an index of source stack and an index of destination stack."""
    match = MOVE_REGEX.match(line)
    if match:
        # Subtracting one from stack index because input has indexes starting at 1, but in the script we count from 0
        return (
            int(match.group("crates_number")),
            int(match.group("source_stack")) - 1,
            int(match.group("dest_stack")) - 1,
        )
    return None


def make_move(stacks, move):
    """Move crates between stacks"""
    crates_number, source_stack_idx, dest_stack_idx = move
    source_stack = stacks[source_stack_idx]
    dest_stack = stacks[dest_stack_idx]

    crates_to_move = source_stack.remove_many(n=crates_number)
    assert all(crates_to_move)
    dest_stack.put_many(crates_to_move)


def main():
    crates_layers = []
    num_of_stacks = 0
    parse_mode = ["stack", "moves"][0]
    stacks = []

    with open("input.txt", "r") as f:
        for line in f.readlines():
            if line != "\n":
                if parse_mode == "stack":
                    layer = parse_crates_layer(line)
                    if len(layer) > num_of_stacks:
                        num_of_stacks = len(layer)
                    if any(layer):  # Skip "empty" layers
                        crates_layers.append(layer)
                else:
                    move = parse_move(line)
                    if move:
                        make_move(stacks, move)
            else:
                stacks = make_stacks(crates_layers, num_of_stacks)
                parse_mode = "moves"  # Change parse mode
        result = "".join(stack.get_top() for stack in stacks)
        print("Result:", result)
        return result


if __name__ == "__main__":
    main()
