from dataclasses import dataclass

import pygame

from chess_set import Piece



class ChessBoard:
    def __init__(self, table_size, board_pos):
        self.table_size = table_size
        self.board_pos = board_pos
        self.surface, self.grid = create_board_surface(self.table_size)

    def get_square_under_mouse(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(
            self.board_pos
        )
        x, y = [int(v // self.table_size) for v in mouse_pos]
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
    column: int = None
    size: int = None


def create_board_surface(tile_size):
    """Create a surface for the chess board."""
    surface = pygame.Surface((tile_size * 8, tile_size * 8))
    surface.fill((255, 255, 255))

    grid = []
    for row in range(8):
        grid.append([])
        for col in range(8):
            if (row + col) % 2 == 0:
                color = (0, 0, 0)
            else:
                color = (255, 255, 255)
            rect = pygame.draw.rect(
                surface,
                color,
                (col * tile_size, row * tile_size, tile_size, tile_size),
            )
            square = Square(rect, color=color, row=row, column=col, size=tile_size)
            grid[row].append(square)

    return surface, grid