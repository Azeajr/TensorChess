import sys

import pygame

from settings import Settings
from chess_board import ChessBoard


class ChessGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Tensor Chess")

        self.clock = pygame.time.Clock()

        self.chess_board = ChessBoard(
            self.settings.square_size, self.settings.board_pos
        )

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(1)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.chess_board.board, self.settings.board_pos)
        print(self.chess_board.get_square_under_mouse())

        pygame.display.flip()


if __name__ == "__main__":
    chess_game = ChessGame()
    chess_game.run_game()
