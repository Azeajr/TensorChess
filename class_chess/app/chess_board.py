from dataclasses import dataclass

import pygame

from chess_set import ChessSet, Piece


@dataclass
class Coordinate:
    x: int
    y: int

    def __str__(self):
        return f"{chr(self.x + 97)}{8 - self.y}"


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
        return f"{self.cord} {self.piece}"


class ChessBoard:
    def __init__(self, square_size, board_pos):
        self.square_size = square_size
        self.board_pos = board_pos
        self.board, self.grid = self.__create_board_surface()

    def __create_board_surface(self) -> tuple[pygame.Surface, list[list[Square]]]:
        """Create a surface for the chess board."""
        board = pygame.Surface((self.square_size * 8, self.square_size * 8))
        board.fill((255, 255, 255))
        grid: list[list[Square]] = [[None for x in range(8)] for y in range(8)]
        chess_set = ChessSet(board, grid)

        for y in range(8):
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
                    cord=Coordinate(x, y),
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

                grid[x][y] = square
        return board, grid

    def get_square_under_mouse(self) -> Square:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(
            self.board_pos
        )
        x, y = [int(v // self.square_size) for v in mouse_pos]
        try:
            if x >= 0 and y >= 0:
                return self.grid[x][y]
        except IndexError:
            pass
