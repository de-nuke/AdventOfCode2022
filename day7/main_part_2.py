"""
--- Part Two ---

Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the update, you need unused space of at least
30000000. You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165;
this means that the size of the unused space must currently be 21618835, which isn't quite the 30000000 required by the
update. Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can
run.

To achieve this, you have the following options:

    Delete directory e, which would increase unused space by 584.
    Delete directory a, which would increase unused space by 94853.
    Delete directory d, which would increase unused space by 24933642.
    Delete directory /, which would increase unused space by 48381165.

Directories e and a are both too small; deleting them would not free up enough space. However, directories d and / are
both big enough! Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is
the total size of that directory?

https://adventofcode.com/2022/day/7#part2
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

TOTAL_DISK_SPACE = 70000000
UNUSED_SPACE_REQUIRED = 30000000


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

    def get_used_space(self) -> int:
        """Get disk space used by all files."""
        if not self.root:
            raise RuntimeError("Missing root directory")
        return self.root.size

    def get_unused_space(self) -> int:
        """Get remaining free disk space."""
        return TOTAL_DISK_SPACE - self.get_used_space()

    def get_minimum_space_to_free_up(self) -> int:
        """Get minimum unused space required to run the system update."""
        return UNUSED_SPACE_REQUIRED - self.get_unused_space()


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
    minimum_space_to_free_up = system.get_minimum_space_to_free_up()
    return filter(lambda d: d.size >= minimum_space_to_free_up, directories)


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

        directories_big_enough = find_directories(system)
        smallest_directory_to_remove = min(directories_big_enough, key=lambda d: d.size)
        result = smallest_directory_to_remove.size

        print(f"Result: {result}")
        return result


if __name__ == "__main__":
    main()
