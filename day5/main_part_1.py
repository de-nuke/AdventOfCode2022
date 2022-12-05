"""
The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks
of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or
fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are
rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which
crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input).
For example:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is
on top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a
single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack
to a different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to
stack 1, resulting in this configuration:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3

In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first crate
to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3

Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up
below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3

Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3

The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in
stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?

https://adventofcode.com/2022/day/5
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

    def remove(self):
        return self.crates.pop() if self.crates else None

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
    for _ in range(crates_number):
        crate = source_stack.remove()
        assert crate is not None
        dest_stack.put(crate)


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
