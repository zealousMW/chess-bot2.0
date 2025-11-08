import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import codes.chess_bot_need as cbn  # reuse existing helper


def test_empty_board():
    matrix = [['.' for _ in range(8)] for _ in range(8)]
    fen = cbn.board_to_fen(matrix)
    assert fen == '8/8/8/8/8/8/8/8'
