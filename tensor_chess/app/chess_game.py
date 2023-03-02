import sys

import pygame

from settings import Settings
from chess_set import ChessSet
from chess_board import ChessBoard


class ChessGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Tensor Chess")
        
        self.chess_set = ChessSet(self)
        self.chess_board = ChessBoard(self.settings.table_size, self.settings.board_pos)

        self.clock = pygame.time.Clock()
        
        

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(0.25)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        # Draw the chess board.
        self.screen.blit(self.chess_board.surface, self.settings.board_pos)

        # Draw a row of black pieces.
        for index, piece in enumerate(self.chess_set.pieces[:6]):
            piece.x = index * 100
            piece.blitme()

        # # Draw a row of white pieces.
        for index, piece in enumerate(self.chess_set.pieces[6:]):
            piece.x = index * 100
            piece.y = 100
            piece.blitme()

        piece, x, y = self.chess_board.get_square_under_mouse()
        print(piece, x, y)
        


        pygame.display.flip()

if __name__ == "__main__":
    chess_game = ChessGame()
    chess_game.run_game()