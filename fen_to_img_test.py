import chess

from board import BoardImage
from config import Config

fen = "rnbqk1nr/pppp1ppp/8/4p3/1bP5/2N5/PP1PPPPP/R1BQKBNR w KQkq - 2 3"
# fen = "R1BQKBNR/PP1PPPPP/2N5/1bP5/4p3/8/pppp1ppp/rnbqk1nr w KQkq - 2 3"

config = Config(piece_theme="fantasy", flip_board=True)

renderer = BoardImage(fen, config=config)

image = renderer.render(highlighted_squares=(chess.F8, chess.B4))
# image = renderer.render(highlighted_squares=(chess.F1, chess.B5))
image.show()
