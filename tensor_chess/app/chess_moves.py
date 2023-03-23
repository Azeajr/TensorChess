from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod


if TYPE_CHECKING:
    from chess_board import Square
    from chess_set import Piece


def get_validator(name: str) -> Validator:
    """Returns a validator for a chess piece."""
    validators = {
        "pawn": PawnValidator,
        "rook": RookValidator,
        "knight": KnightValidator,
        "bishop": BishopValidator,
        "queen": QueenValidator,
        "king": KingValidator,
    }
    return validators[name]


class Validator(ABC):
    """Represents a chess piece validator."""

    @abstractmethod
    def validate(self, start: Square, end: Square) -> bool:
        """Validates a move."""


class PawnValidator(Validator):
    """Represents a pawn validator."""

    def __init__(self, grid: list[list[Square]]):
        """Initializes the pawn validator."""
        self.grid = grid

    def validate(self, start: Square, end: Square) -> bool:
        """Validates a pawn move."""

        def __single_move() -> bool:
            """Validates a single move."""
            return (
                start.cord.x == end.cord.x
                and start.cord.y + 1 * start.piece.direction == end.cord.y
                and not end.piece
            )

        def __double_move() -> bool:
            """Validates a double move."""
            if start.piece.direction == 1:
                if start.cord.y != 1:
                    return False
            elif start.piece.direction == -1:
                if start.cord.y != 6:
                    return False
            return (
                start.cord.x == end.cord.x
                and start.cord.y + 2 * start.piece.direction == end.cord.y
                and not end.piece
            )

        def __capture() -> bool:
            """Validates a capture move."""
            return (
                abs(start.cord.x - end.cord.x) == 1
                and start.cord.y + 1 * start.piece.direction == end.cord.y
                and end.piece
            )

        def __en_passant() -> bool:
            """Validates an en passant move."""
            if start.piece.direction == 1:
                if start.cord.y != 4:
                    return False
            elif start.piece.direction == -1:
                if start.cord.y != 3:
                    return False
            return (
                abs(start.cord.x - end.cord.x) == 1
                and start.cord.y + 1 * start.piece.direction == end.cord.y
                and not end.piece
                and self.grid[end.cord.x][start.cord.y].piece
            )

        return __single_move() or __double_move() or __capture() or __en_passant()


class KnightValidator(Validator):
    """Represents a knight validator."""

    def validate(self, start: Square, end: Square) -> bool:
        """Validates a knight move."""
        return (
            abs(start.cord.x - end.cord.x) == 1
            and abs(start.cord.y - end.cord.y) == 2
            or abs(start.cord.x - end.cord.x) == 2
            and abs(start.cord.y - end.cord.y) == 1
        )


class BishopValidator(Validator):
    """Represents a bishop validator."""

    def __init__(self, grid: list[list[Square]]):
        """Initializes the bishop validator."""
        self.grid = grid

    def validate(self, start: Square, end: Square) -> bool:
        """Validates a bishop move."""

        def slope(start: Square, end: Square) -> float:
            """Returns the slope of the line between two squares."""
            return (end.cord.y - start.cord.y) / (end.cord.x - start.cord.x)

        if abs(start.cord.x - end.cord.x) == abs(start.cord.y - end.cord.y):
            if slope(start, end) == 1.0:
                for x, y in zip(
                    range(
                        min(start.cord.x, end.cord.x) + 1, max(start.cord.x, end.cord.x)
                    ),
                    range(
                        min(start.cord.y, end.cord.y) + 1, max(start.cord.y, end.cord.y)
                    ),
                ):
                    if self.grid[x][y].piece:
                        return False
                return True
            elif slope(start, end) == -1.0:
                for x, y in zip(
                    range(
                        min(start.cord.x, end.cord.x) + 1, max(start.cord.x, end.cord.x)
                    ),
                    range(
                        max(start.cord.y, end.cord.y) - 1,
                        min(start.cord.y, end.cord.y),
                        -1,
                    ),
                ):
                    if self.grid[x][y].piece:
                        return False
                return True
            return False


class RookValidator(Validator):
    """Represents a rook validator."""

    def __init__(self, grid: list[list[Square]]):
        """Initializes the rook validator."""
        self.grid = grid

    def validate(self, start: Square, end: Square) -> bool:
        """Validates a rook move."""
        if start.cord.x == end.cord.x:
            for y in range(
                min(start.cord.y, end.cord.y) + 1, max(start.cord.y, end.cord.y)
            ):
                if self.grid[start.cord.x][y].piece:
                    return False
            return True
        elif start.cord.y == end.cord.y:
            for x in range(
                min(start.cord.x, end.cord.x) + 1, max(start.cord.x, end.cord.x)
            ):
                if self.grid[x][start.cord.y].piece:
                    return False
            return True


class QueenValidator(Validator):
    """Represents a queen validator."""

    def __init__(self, grid: list[list[Square]]):
        """Initializes the queen validator."""
        self.grid = grid
        self.bishop = BishopValidator(grid)
        self.rook = RookValidator(grid)

    def validate(self, start: Square, end: Square) -> bool:
        """Validates a queen move."""
        return self.bishop.validate(start, end) or self.rook.validate(start, end)


class KingValidator(Validator):
    """Represents a king validator."""

    def __init__(self, grid: list[list[Square]]):
        """Initializes the king validator."""
        self.grid = grid

    def validate(self, start: Square, end: Square) -> bool:
        """Validates a king move."""
        if abs(start.cord.x - end.cord.x) <= 1 and abs(start.cord.y - end.cord.y) <= 1:
            return True
        return False
