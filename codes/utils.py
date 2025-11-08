"""Utility helpers for the chess bot project.

This module contains canonical helpers used by the scripts in `codes/`.
Keep functions importable without side effects.
"""

from typing import List
import chess


def board_to_fen(board: List[List[str]]) -> str:
    """Convert a 2D board array (8x8) of piece symbols into the
    FEN piece-placement string (first field of a FEN).

    The board is expected as a list of rows from top (rank 8) to bottom (rank 1).
    Empty squares use the '.' character.

    Example:
        board[0][0] is the piece at a8.
    """
    parts = []
    for row in board:
        empty = 0
        row_parts = []
        for sq in row:
            if sq == '.':
                empty += 1
            else:
                if empty:
                    row_parts.append(str(empty))
                    empty = 0
                row_parts.append(sq)
        if empty:
            row_parts.append(str(empty))
        parts.append(''.join(row_parts))
    return '/'.join(parts)


_piece_map = {
    '.': None,
    'p': 'p', 'r': 'r', 'n': 'n', 'b': 'b', 'q': 'q', 'k': 'k',
    'P': 'P', 'R': 'R', 'N': 'N', 'B': 'B', 'Q': 'Q', 'K': 'K',
}


def board_to_fen_board(board: List[List[str]]) -> str:
    """Create a full chess.Board FEN from a matrix of piece symbols.

    This returns the full FEN string as produced by python-chess.Board.fen().
    Empty squares should be '.'. This function places pieces and then
    returns Board.fen() – other FEN fields (active color, castling, etc.) are
    the library defaults.
    """
    b = chess.Board.empty()
    # board rows are top (rank 8) to bottom (rank 1)
    for row_idx, row in enumerate(board):
        for col_idx, piece in enumerate(row):
            mapped = _piece_map.get(piece, None)
            if mapped:
                sq = chess.square(col_idx, 7 - row_idx)
                b.set_piece_at(sq, chess.Piece.from_symbol(mapped))
    return b.fen()
