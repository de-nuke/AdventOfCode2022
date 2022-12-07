"""
--- Day 7: No Space Left On Device ---

You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear
much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input).
For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files).
The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and
listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

    cd means change directory. This changes which directory is the current directory, but the specific result depends
    on the argument:
        cd x moves in one level: it looks in the current directory for the directory named x and makes it the current
        directory.
        cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory
        the current directory.
        cd / switches the current directory to the outermost directory, /.
    ls means list. It prints out all of the files and directories immediately contained by the current directory:
        123 abc means that the current directory contains a file named abc with size 123.
        dir xyz means that the current directory contains a directory named xyz.

Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)

Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a). These
directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion.
To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the
sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic
size.)

The total sizes of the directories above can be found as follows:

    The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
    The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and
    h.lst (size 62596), plus file i indirectly (a contains e which contains i).
    Directory d has total size 24933642.
    As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.

To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes.
In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this
example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those
directories?

https://adventofcode.com/2022/day/7
"""

import re
from collections import namedtuple
from typing import Dict, Generator, Iterable, List, Optional, TextIO, Tuple

COMMAND_REGEX = re.compile(r"^\$ (?P<command_name>cd|ls)( (?P<command_parameter>[\w/\.]+))?$")
LISTED_FILE_REGEX = re.compile(r"^(?P<file_size>\d+) (?P<file_name>[\w+\.]+)$")
LISTED_DIR_REGEX = re.compile(r"^dir (?P<directory_name>[\w+\.]+)$")


Command = namedtuple("Command", ["name", "parameter"])
ListedFile = namedtuple("ListedFile", ["name", "size"])
ListedDirectory = namedtuple("ListedDirectory", ["name"])

ParsedLineType = Tuple[Optional[Command], Optional[ListedFile], Optional[ListedDirectory]]

MAX_DIR_SIZE = 100000


class Directory:
    """Simple filesystem directory with a tree structure."""

    def __init__(self, name: str, parent: Optional["Directory"] = None) -> None:
        self.name = name
        self.parent = parent
        self.directories: Dict[str, "Directory"] = {}  # <name>: <Directory>
        self.files: Dict[str, int] = {}  # <name>: <size>

    def add_file(self, name: str, size: int) -> None:
        """Create a file in this directory."""
        self.files[name] = size

    def add_directory(self, name: str) -> "Directory":
        """Create a child directory in this directory."""
        if name in [".", ".."]:
            raise ValueError("Cannot add '.' and '..' directories.")
        self.directories[name] = Directory(name, parent=self)
        return self.directories[name]

    def find_directory(self, name: str) -> Optional["Directory"]:
        """Return regular, child directory (with given name) or one of the 'special' directories."""
        if name == ".":
            return self
        if name == "..":
            return self.parent
        return self.directories.get(name)

    def __str__(self) -> str:
        return self.name + f"(path: {self.path})"

    @property
    def path(self) -> str:
        """Get absolute path of the directory."""
        if self.parent:
            return ("root" if self.parent.path == "/" else self.parent.path) + "/" + self.name
        else:
            return self.name

    @property
    def size(self) -> int:
        """
        Count the size of a directory. Total size is a sum of all files and directories sizes located in this directory.
        """
        return sum(self.files.values()) + sum(directory.size for directory in self.child_directories)

    @property
    def child_directories(self) -> List["Directory"]:
        """Return list of all "normal" directories located in this one. Special directories are skipped."""
        return list(self.directories.values())

    def tree_representation(self, indent_level: int = 0) -> str:
        """
        Get a graphical representation of the directory tree.
        """
        lines = []
        indent = "\t" * indent_level
        lines.append(indent + " - " + self.name + " (dir):")
        for directory in self.child_directories:
            directory.tree_representation(indent_level + 1)
        for name, size in self.files.items():
            lines.append(indent + "\t" + " - " + name + f" (file, size={size})")
        return "\n".join(lines)


class System:
    """Simple directory manager able to change current directory or traverse all of them."""

    def __init__(self) -> None:
        self.current_directory: Optional[Directory] = None
        self.root: Optional[Directory] = None

    def change_directory(self, name: str) -> None:
        """
        Change current working directory to the one with a given name.

        Special names are:
        '.' – Doesn't change directory, stays in the current one.
        '..' – Change directory to the parent of the current directory.

        If directory with a given name hasn't been seen yet, then add it to the directory tree.
        """
        if self.current_directory is None:
            # This is only the initial state, because later system is always in a directory.
            self.root = Directory(name, parent=None)
            self.current_directory = self.root
            return

        destination_directory = self.current_directory.find_directory(name)
        if destination_directory is None:
            self.current_directory = self.current_directory.add_directory(name)
        else:
            self.current_directory = destination_directory

    def traverse_directories(self, starting_directory: Optional[Directory] = None) -> Generator[Directory, None, None]:
        """Visit and yield every directory in the system starting from root or from given directory."""
        starting_directory = starting_directory or self.root
        if starting_directory is None:
            raise RuntimeError("Missing root directory")
        yield starting_directory
        for directory in starting_directory.child_directories:
            yield from self.traverse_directories(directory)


def input_parser(file_handler: TextIO) -> Generator[ParsedLineType, None, None]:
    """Parse each line of the "terminal output" (this puzzle input) into specific type."""
    for line in file_handler:
        command, listed_file, listed_directory = None, None, None
        match = COMMAND_REGEX.match(line)
        if match:
            command = Command(name=match.group("command_name"), parameter=match.group("command_parameter"))
        match = LISTED_FILE_REGEX.match(line)
        if match:
            listed_file = ListedFile(name=match.group("file_name"), size=int(match.group("file_size")))
        match = LISTED_DIR_REGEX.match(line)
        if match:
            listed_directory = ListedDirectory(name=match.group("directory_name"))
        yield command, listed_file, listed_directory


def handle_command(command: Command, system: System) -> None:
    """Handle case when terminal output line was command call."""
    if command.name == "cd":
        system.change_directory(command.parameter)
    elif command.name == "ls":
        pass  # Skip
    else:
        raise ValueError(f"Invalid command '{command.name}'")


def handle_listed_file(listed_file: ListedFile, system: System) -> None:
    """Handle case when terminal output line was a listed file"""
    if not system.current_directory:
        raise RuntimeError("System must be in a working directory")
    current_directory = system.current_directory
    current_directory.add_file(listed_file.name, listed_file.size)


def handle_listed_directory(listed_directory: ListedDirectory, system: System) -> None:
    """Handle case when terminal output line was a listed directory"""
    if not system.current_directory:
        raise RuntimeError("System must be in a working directory")
    current_directory = system.current_directory
    current_directory.add_directory(listed_directory.name)


def find_directories(system: System) -> Iterable[Directory]:
    """Traverse through all directories and filter them by the rule of the puzzle"""
    directories = system.traverse_directories()
    return filter(lambda d: d.size <= MAX_DIR_SIZE, directories)


def main() -> int:
    with open("input.txt", "r") as f:
        system = System()
        for command, listed_file, listed_directory in input_parser(f):
            if command:
                handle_command(command, system)
            elif listed_file:
                handle_listed_file(listed_file, system)
            elif listed_directory:
                handle_listed_directory(listed_directory, system)
            else:
                raise ValueError(f"Invalid line at {f.tell()}")

        filtered_directories = find_directories(system)
        result = sum(d.size for d in filtered_directories)
        print(f"Result: {result}")
        return result


if __name__ == "__main__":
    main()
