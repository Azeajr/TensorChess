from itertools import product
from typing import Any, Callable
from dataclasses import dataclass, field

import pygame

from spritesheet import SpriteSheet


class ChessSet:
    """Represents a set of chess pieces. Each piece is an object of the Piece class."""

    def __init__(self, screen: pygame.Surface) -> None:
        """Initializes attributes of a chess set.

        Args:
            screen (Surface): _description_
        """
        self.screen = screen
        self.__chess_set = self.__create_set()

    @property
    def chess_set(self) -> dict[str, list[Any]]:
        """Returns the chess set."""
        return self.__chess_set

    def __create_set(self) -> dict[str, list[Any]]:
        """Creates a list of chess pieces."""
        colors = ["white", "black"]

        pieces = {
            color: (iter if color == "black" else reversed)(
                [
                    Piece(self.screen, "rook", color),
                    Piece(self.screen, "knight", color),
                    Piece(self.screen, "bishop", color),
                    Piece(self.screen, "queen", color),
                    Piece(self.screen, "king", color),
                    Piece(self.screen, "bishop", color),
                    Piece(self.screen, "knight", color),
                    Piece(self.screen, "rook", color),
                    *[Piece(self.screen, "pawn", color) for _ in range(8)],
                ]
            )
            for color in colors
        }
        return pieces


@dataclass
class Piece:
    screen: pygame.Surface
    name: str
    color: str
    image: pygame.Surface = field(init=False)
    rect: pygame.Rect = field(init=False)
    direction: int = field(init=False)
    validator: Callable[[tuple[int, int], tuple[int, int]], bool] = field(init=False)

    def __str__(self) -> str:
        return f"{self.color} {self.name}"

    def __post_init__(self):
        self.__load_images()
        self.image = self._piece_images[(self.color, self.name)]
        self.direction = 1 if self.color == "black" else -1
        self.__load_validators()

    def blitme(self, center: tuple[int, int]) -> None:
        """Draws the piece at its current location."""
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.screen.blit(self.image, self.rect)

    def __load_images(self) -> None:
        """_summary_"""
        filename = "graphics/chess_pieces.bmp"
        pieces_ss = SpriteSheet(filename)

        colors = ["black", "white"]
        names = ["king", "queen", "rook", "bishop", "knight", "pawn"]

        self._piece_images = dict(
            zip(
                product(colors, names), pieces_ss.load_grid_images(2, 6, 64, 72, 68, 48)
            )
        )

    def __load_validators(self) -> None:
        validators = {
            "pawn": lambda start, end: start.column == end.column
            and start.row + 1 * self.direction == end.row,
            "rook": lambda start, end: start.column == end.column
            or start.row == end.row,
            "knight": lambda start, end: abs(start.column - end.column) == 2
            and abs(start.row - end.row) == 1
            or abs(start.column - end.column) == 1
            and abs(start.row - end.row) == 2,
            "bishop": lambda start, end: abs(start.column - end.column)
            == abs(start.row - end.row),
            "queen": lambda start, end: abs(start.column - end.column)
            == abs(start.row - end.row)
            or start.column == end.column
            or start.row == end.row,
            "king": lambda start, end: abs(start.column - end.column) <= 1
            and abs(start.row - end.row) <= 1,
        }
        self.validator = validators[self.name]
