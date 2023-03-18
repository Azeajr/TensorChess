import sys

from pygame import constants
from pygame import event
from pygame import base
from pygame import display
from pygame import time
from pygame import mouse

from settings import Settings
from chess_board import ChessBoard, Square


class ChessGame:
    def __init__(self):
        base.init()
        self.settings = Settings()
        self.screen = display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        display.set_caption("Tensor Chess")

        self.clock = time.Clock()

        self.chess_board = ChessBoard(
            self.settings.square_size, self.settings.board_pos
        )
        self.selection: Square = None

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for this_event in event.get():
            if this_event.type == constants.QUIT:
                sys.exit()
            elif this_event.type == constants.KEYDOWN:
                if this_event.key == constants.K_q:
                    sys.exit()
            elif this_event.type == constants.MOUSEBUTTONDOWN:
                square = self.chess_board.get_square_under_mouse()
                if square and square.piece:
                    self.selection = square

            elif this_event.type == constants.MOUSEBUTTONUP:
                square = self.chess_board.get_square_under_mouse()
                if (
                    square
                    and self.selection
                    and (square != self.selection)
                    and self.chess_board.validators.validator[
                        self.selection.piece.name
                    ](self.selection, square, self.selection.piece.direction)
                ):
                    square.piece = self.selection.piece
                    self.selection.piece = None
                    square.draw_square()
                    square.piece.blitme(square.rect.center)
                    self.selection.draw_square()

                self.selection = None

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.chess_board.board, self.settings.board_pos)

        if self.selection:
            self.screen.blit(self.selection.piece.image, mouse.get_pos())

        display.flip()


if __name__ == "__main__":
    chess_game = ChessGame()
    chess_game.run_game()
