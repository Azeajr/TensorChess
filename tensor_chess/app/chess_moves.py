from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, TYPE_CHECKING


if TYPE_CHECKING:
    from chess_board import Square


@dataclass
class Validators:
    """Represents a chess piece validator."""

    grid: list[list[Square]]
    validator: dict[str, Callable[[Square, Square], bool]] = field(default_factory=dict)

    def _pawn_validator(self, start: Square, end: Square, direction: int) -> bool:
        """Validates a pawn move."""

        def __single_move() -> bool:
            """Validates a single move."""
            return (
                start.cord.x == end.cord.x
                and start.cord.y + 1 * direction == end.cord.y
                and not end.piece
            )

        def __double_move() -> bool:
            """Validates a double move."""
            if direction == 1:
                if start.cord.y != 1:
                    return False
            elif direction == -1:
                if start.cord.y != 6:
                    return False
            return (
                start.cord.x == end.cord.x
                and start.cord.y + 2 * direction == end.cord.y
                and not end.piece
            )

        def __capture() -> bool:
            """Validates a capture move."""
            return (
                abs(start.cord.x - end.cord.x) == 1
                and start.cord.y + 1 * direction == end.cord.y
                and end.piece
            )
        
        def __en_passant() -> bool:
            """Validates an en passant move."""
            if direction == 1:
                if start.cord.y != 4:
                    return False
            elif direction == -1:
                if start.cord.y != 3:
                    return False
            return (
                abs(start.cord.x - end.cord.x) == 1
                and start.cord.y + 1 * direction == end.cord.y
                and not end.piece
                and self.grid[end.cord.x][start.cord.y].piece
            )

        return __single_move() or __double_move() or __capture() or __en_passant()

    def _rook_validator(self, start: Square, end: Square, _) -> bool:
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

    def _knight_validator(self, start: Square, end: Square, _) -> bool:
        """Validates a knight move."""
        return (
            abs(start.cord.x - end.cord.x) == 2
            and abs(start.cord.y - end.cord.y) == 1
            or abs(start.cord.x - end.cord.x) == 1
            and abs(start.cord.y - end.cord.y) == 2
        )

    def _bishop_validator(self, start: Square, end: Square, _) -> bool:
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
                        max(start.cord.y, end.cord.y) - 1, min(start.cord.y, end.cord.y), -1
                    ),
                ):
                    if self.grid[x][y].piece:
                        return False
                return True
            return False

    def _queen_validator(self, start: Square, end: Square, _) -> bool:
        """Validates a queen move."""
        return self._rook_validator(start, end, None) or self._bishop_validator(
            start, end, None
        )

    def _king_validator(self, start: Square, end: Square, _) -> bool:
        """Validates a king move."""
        return (
            abs(start.cord.x - end.cord.x) <= 1 and abs(start.cord.y - end.cord.y) <= 1
        )

    def __post_init__(self):
        """Loads the validator function."""
        self.validator["pawn"] = self._pawn_validator
        self.validator["rook"] = self._rook_validator
        self.validator["knight"] = self._knight_validator
        self.validator["bishop"] = self._bishop_validator
        self.validator["queen"] = self._queen_validator
        self.validator["king"] = self._king_validator

        # if not self.name:
        #     raise ValueError("Validator name is required.")

        # if self.name == "pawn":
        #     self.validator = self._pawn_validator
        # elif self.name == "rook":
        #     self.validator = self._rook_validator
        # elif self.name == "knight":
        #     self.validator = self._knight_validator
        # elif self.name == "bishop":
        #     self.validator = self._bishop_validator
        # elif self.name == "queen":
        #     self.validator = self._queen_validator
        # elif self.name == "king":
        #     self.validator = self._king_validator
        # else:
        #     raise ValueError(f"Invalid validator name: {self.name}")
