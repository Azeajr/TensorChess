from __future__ import annotations
from itertools import product
from typing import Any, TYPE_CHECKING, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


import pygame

from spritesheet import SpriteSheet
from chess_moves import get_validator

if TYPE_CHECKING:
    from chess_board import Square


class ChessSet:
    """Represents a set of chess pieces. Each piece is an object of the Piece class."""

    def __init__(self, screen: pygame.Surface, grid: list[list[Square]]) -> None:
        """Initializes attributes of a chess set.

        Args:
            screen (Surface): _description_
        """
        self.screen = screen
        self.grid = grid
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
                    get_piece_factory("rook").create_piece(
                        self.screen, self.grid, color
                    ),
                    get_piece_factory("knight").create_piece(
                        self.screen, self.grid, color
                    ),
                    get_piece_factory("bishop").create_piece(
                        self.screen, self.grid, color
                    ),
                    get_piece_factory("queen").create_piece(
                        self.screen, self.grid, color
                    ),
                    get_piece_factory("king").create_piece(
                        self.screen, self.grid, color
                    ),
                    get_piece_factory("bishop").create_piece(
                        self.screen, self.grid, color
                    ),
                    get_piece_factory("knight").create_piece(
                        self.screen, self.grid, color
                    ),
                    get_piece_factory("rook").create_piece(
                        self.screen, self.grid, color
                    ),
                    *[
                        get_piece_factory("pawn").create_piece(
                            self.screen, self.grid, color
                        )
                        for _ in range(8)
                    ],
                ]
            )
            for color in colors
        }
        return pieces


def get_piece_factory(name: str) -> PieceFactory:
    """Returns a factory for creating a chess piece."""
    factories = {
        "pawn": PawnFactory(),
        "rook": RookFactory(),
        "knight": KnightFactory(),
        "bishop": BishopFactory(),
        "queen": QueenFactory(),
        "king": KingFactory(),
    }
    if name not in factories:
        raise ValueError(f"Invalid piece name: {name}")
    return factories[name]


class PieceFactory(ABC):
    """Abstract class for creating chess pieces."""

    @abstractmethod
    def create_piece(
        self, screen: pygame.Surface, grid: list[list[Square]], color: str
    ) -> Piece:
        """Creates a chess piece."""


class PawnFactory(PieceFactory):
    """Creates a pawn chess piece."""

    def create_piece(
        self, screen: pygame.Surface, grid: list[list[Square]], color: str
    ) -> Piece:
        """Creates a pawn chess piece."""
        return Piece(screen, "pawn", color, get_validator("pawn")(grid).validate)


class RookFactory(PieceFactory):
    """Creates a rook chess piece."""

    def create_piece(
        self, screen: pygame.Surface, grid: list[list[Square]], color: str
    ) -> Piece:
        """Creates a rook chess piece."""
        return Piece(screen, "rook", color, get_validator("rook")(grid).validate)


class KnightFactory(PieceFactory):
    """Creates a knight chess piece."""

    def create_piece(
        self, screen: pygame.Surface, grid: list[list[Square]], color: str
    ) -> Piece:
        """Creates a knight chess piece."""
        return Piece(screen, "knight", color, get_validator("knight")().validate)


class BishopFactory(PieceFactory):
    """Creates a bishop chess piece."""

    def create_piece(
        self, screen: pygame.Surface, grid: list[list[Square]], color: str
    ) -> Piece:
        """Creates a bishop chess piece."""
        return Piece(screen, "bishop", color, get_validator("bishop")(grid).validate)


class QueenFactory(PieceFactory):
    """Creates a queen chess piece."""

    def create_piece(
        self, screen: pygame.Surface, grid: list[list[Square]], color: str
    ) -> Piece:
        """Creates a queen chess piece."""
        return Piece(screen, "queen", color, get_validator("queen")(grid).validate)


class KingFactory(PieceFactory):
    """Creates a king chess piece."""

    def create_piece(
        self, screen: pygame.Surface, grid: list[list[Square]], color: str
    ) -> Piece:
        """Creates a king chess piece."""
        return Piece(screen, "king", color, get_validator("king")(grid).validate)


@dataclass
class Piece:
    screen: pygame.Surface
    name: str
    color: str
    validator: Callable[[Square, Square], bool] = None
    image: pygame.Surface = field(init=False)
    rect: pygame.Rect = field(init=False)
    direction: int = None

    def __str__(self) -> str:
        return f"{self.color} {self.name}"

    def __post_init__(self):
        self.__load_images()
        self.image = self._piece_images[(self.color, self.name)]
        self.direction = -1 if self.color == "white" else 1

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
