from dataclasses import dataclass

import pygame
from pygame import draw

from chess_set import ChessSet, Piece
from chess_moves import Validators


@dataclass
class Coordinate:
    x: int
    y: int


@dataclass
class Square:
    surface: pygame.Surface
    rect: pygame.Rect
    piece: Piece
    color: str
    cord: Coordinate
    size: int

    def draw_square(self):
        pygame.draw.rect(
            self.surface,
            self.color,
            self.rect,
        )

    def __str__(self):
        return f"{chr(self.cord.x + 97)}{self.cord.y} {self.piece}"


class ChessBoard:
    def __init__(self, square_size, board_pos):
        self.square_size = square_size
        self.board_pos = board_pos
        self.board, self.grid = self.__create_board_surface()
        self.validators = Validators(self.grid)

    def __create_board_surface(self) -> tuple[pygame.Surface, list[list[Square]]]:
        """Create a surface for the chess board."""
        board = pygame.Surface((self.square_size * 8, self.square_size * 8))
        board.fill((255, 255, 255))

        chess_set = ChessSet(board)

        grid: list[list[Square]] = []
        for y in range(8):
            grid.append([])
            for x in range(8):
                if (y + x) % 2 == 0:
                    color = (255, 255, 255)
                else:
                    color = (0, 0, 0)
                rect = pygame.Rect(
                    x * self.square_size,
                    y * self.square_size,
                    self.square_size,
                    self.square_size,
                )

                square = Square(
                    board,
                    rect,
                    piece=None,
                    color=color,
                    cord=Coordinate(x, 8 - y),
                    size=self.square_size,
                )
                square.draw_square()

                piece: Piece = None
                if 0 <= y <= 1:
                    piece = next(chess_set.chess_set["black"])
                    piece.blitme(rect.center)
                elif 6 <= y <= 7:
                    piece = next(chess_set.chess_set["white"])
                    piece.blitme(rect.center)
                square.piece = piece

                grid[y].append(square)
        return board, grid

    def get_square_under_mouse(self) -> Square:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(
            self.board_pos
        )
        x, y = [int(v // self.square_size) for v in mouse_pos]
        try:
            if x >= 0 and y >= 0:
                return self.grid[y][x]
        except IndexError:
            pass

    def highlight_selected_square(self):
        square, *_ = self.get_square_under_mouse()
        if square:
            draw.rect(
                self.board,
                (255, 0, 0),
                square.rect,
                4,
            )
        return square
