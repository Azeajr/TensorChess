from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, TYPE_CHECKING


if TYPE_CHECKING:
    from chess_board import Square


@dataclass
class Validators:
    """Represents a chess piece validator."""
    grid: list[list[Square]]
    validator: dict[str, Callable[[Square, Square], bool]] = field(
        default_factory=dict
    )

    # name: Optional[str] = None
    # validator: Optional[Callable[[Square, Square], bool]] = None

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
        return __single_move() or __double_move() or __capture()

    def _rook_validator(self, start: Square, end: Square, _) -> bool:
        """Validates a rook move."""
        if start.cord.x == end.cord.x:
            for row in range(
                min(start.cord.y, end.cord.y) + 1, max(start.cord.y, end.cord.y)
            ):
                if self.grid[row][start.cord.x].piece:
                    return False
            return True
        elif start.cord.y == end.cord.y:
            for column in range(
                min(start.cord.x, end.cord.x) + 1, max(start.cord.x, end.cord.x)
            ):
                if self.grid[start.cord.y][column].piece:
                    return False
            return True

        return start.cord.x == end.cord.x or start.cord.y == end.cord.y

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
        return abs(start.cord.x - end.cord.x) == abs(start.cord.y - end.cord.y)

    def _queen_validator(self, start: Square, end: Square, _) -> bool:
        """Validates a queen move."""
        return self._rook_validator(start, end, None) or self._bishop_validator(
            start, end, None
        )

    def _king_validator(self, start: Square, end: Square, _) -> bool:
        """Validates a king move."""
        return (
            abs(start.cord.x - end.cord.x) <= 1
            and abs(start.cord.y - end.cord.y) <= 1
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
