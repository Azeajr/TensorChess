from itertools import product

from spritesheet import SpriteSheet


class ChessSet:
    """Represents a set of chess pieces. Each piece is an object of the Piece class."""

    def __init__(self, chess_game) -> None:
        """Initializes attributes to represent the overall set of chess pieces.

        Args:
            chess_game (_type_): _description_
        """

        self.chess_game = chess_game
        self.pieces = []
        self._load_pieces()

    def _load_pieces(self) -> None:
        """_summary_"""
        filename = "graphics/chess_pieces.bmp"
        pieces_ss = SpriteSheet(filename)

        piece_images = pieces_ss.load_grid_images(2, 6, 64, 72, 68, 48)

        colors = ["black", "white"]
        names = ["king", "queen", "rook", "bishop", "knight", "pawn"]

        def add_piece(nested_tuple):
            (color, name), image = nested_tuple
            piece = Piece(self.chess_game)
            piece.name = name
            piece.color = color
            piece.image = image
            return piece

        self.pieces = list(map(add_piece, zip(product(colors, names), piece_images)))


class Piece:
    """Represents a chess piece."""

    def __init__(self, chess_game):
        """Initializes attributes of a chess piece.

        Args:
            chess_game (_type_): _description_
        """
        self.image = None
        self.name = ""
        self.color = ""

        self.screen = chess_game.screen

        self.x, self.y = 0.0, 0.0

    def blitme(self):
        """Draws the piece at its current location."""
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        self.screen.blit(self.image, self.rect)
