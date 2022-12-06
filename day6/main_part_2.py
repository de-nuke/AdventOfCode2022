"""
--- Part Two ---

Your device's communication system is correctly detecting packets, but still isn't working. It looks like it also needs
to look for messages.

A start-of-message marker is just like a start-of-packet marker, except it consists of 14 distinct characters rather
than 4.

Here are the first positions of start-of-message markers for all of the above examples:

    mjqjpqmgbljsphdztnvjfqwrcgsmlb: first marker after character 19
    bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 23
    nppdvjthqldpwncqszvftbrmjlhg: first marker after character 23
    nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 29
    zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 26

How many characters need to be processed before the first start-of-message marker is detected?

https://adventofcode.com/2022/day/6#part2
"""

from collections import deque

MARKER_LENGTH = 14


def main():
    # Deque works as a fixed-size window moving through the stream, char by char
    marker = deque([], maxlen=MARKER_LENGTH)
    pos = 0

    with open("input.txt", "r") as f:
        while 1:
            char = f.read(1)
            pos += 1
            if not char:
                break
            marker.append(char)

            # SET keeps only unique items so if its length is equal to the length of a marker, then all items in it
            # must be unique.
            if len(set(marker)) == MARKER_LENGTH:
                break

    print(f"Marker: {''.join(marker)}")
    print(f"Position: {pos}")
    return pos


if __name__ == "__main__":
    main()
