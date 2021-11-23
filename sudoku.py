"""
A bunch of helper functions for solve.py
Solve.py solves one of the sudoku puzzles found in the puzzle directory
"""

from __future__ import annotations
from typing import Iterable


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):

        # changed self._grid to a list of lists
        self._grid: list[list[int]] = []

        for puzzle_row in puzzle:
            row = []

            for element in puzzle_row:
                row.append(int(element))

            self._grid.append(row)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""

        # self._grid is now a list so indexing is possible
        self._grid[y][x] = value

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""

        # just like with place indexing is now possible
        self._grid[y][x] = 0

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""

        # just like with place indexing is now possible so returning the value is easy
        return self._grid[y][x]

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""

        # changed options to a set
        options = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        # remove all values from the row using difference
        options = options.difference(set(self.row_values(y)))

        # remove all values from the column using difference
        options = options.difference(set(self.column_values(x)))

        # get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # remove all values from the block using difference
        options = options.difference(set(self.block_values(block_index)))

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        next_x, next_y = -1, -1

        # loop over the rows and grab the index where the value 0 is at
        for row_index, row in enumerate(self._grid):
            try:
                next_x = row.index(0)
                next_y = row_index
                break

            # when the value 0 is not found
            except ValueError:
                pass

        return next_x, next_y

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""
        # it is now possible to index into the grid to grab the rows

        return self._grid[i]

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""

        # getting column values still requires one for loop
        values = []

        for j in range(9):
            values.append(self.value_at(i, j))

        return values

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values = []

        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        for x in range(x_start, x_start + 3):
            for y in range(y_start, y_start + 3):
                values.append(self.value_at(x, y))

        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """

        # checking if zero is in any row in the grid
        return not (any(0 in row for row in self._grid))

    def __str__(self) -> str:
        representation = ""

        # build a printable string from the grid
        for row in self._grid:
            for element in row:
                representation += str(element)
            representation += '\n'

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
