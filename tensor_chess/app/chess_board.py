from dataclasses import dataclass

import pygame
from pygame.surface import Surface

from chess_set import ChessSet, Piece


class ChessBoard:
    def __init__(self, square_size, board_pos):
        self.square_size = square_size
        self.board_pos = board_pos
        self.board, self.grid = self.__create_board_surface()

    def __create_board_surface(self) -> tuple[Surface, list]:
        """Create a surface for the chess board."""
        board = pygame.Surface((self.square_size * 8, self.square_size * 8))
        board.fill((255, 255, 255))

        chess_set = ChessSet(board)

        grid = []
        for row in range(8):
            grid.append([])
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = (255, 255, 255)
                else:
                    color = (0, 0, 0)
                rect = pygame.draw.rect(
                    board,
                    color,
                    (
                        col * self.square_size,
                        row * self.square_size,
                        self.square_size,
                        self.square_size,
                    ),
                )
                piece = None
                if 0 <= row <= 1:
                    piece = next(chess_set.chess_set["black"])
                    piece.blitme(rect.center)
                elif 6 <= row <= 7:
                    piece = next(chess_set.chess_set["white"])
                    piece.blitme(rect.center)

                square = Square(
                    rect,
                    piece=piece,
                    color=color,
                    row=8 - row,
                    column=chr(col + 97),
                    size=self.square_size,
                )
                grid[row].append(square)
        return board, grid

    def get_square_under_mouse(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(
            self.board_pos
        )
        x, y = [int(v // self.square_size) for v in mouse_pos]
        try:
            if x >= 0 and y >= 0:
                return (self.grid[y][x], x, y)
        except IndexError:
            pass
        return (None, x, y)


@dataclass
class Square:
    rect: pygame.Rect
    piece: Piece = None
    color: str = None
    row: int = None
    column: str = None
    size: int = None

    def __str__(self):
        return f"{self.column}{self.row} {self.piece}"
