import chess


def board_to_fen(board):
    fen = ''
    empty_count = 0

    for row in board:
        for square in row:
            if square == '.':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0
                fen += square
        if empty_count > 0:
            fen += str(empty_count)
            empty_count = 0
        fen += '/'

    # Remove the trailing '/'
    fen = fen[:-1]

    return fen


piece_symbols = {
    'r': 'r', 'n': 'n', 'b': 'b', 'q': 'q', 'k': 'k', 'p': 'p',
    'R': 'R', 'N': 'N', 'B': 'B', 'Q': 'Q', 'K': 'K', 'P': 'P',
    '.': '1'
}


def board_to_fen2(matrix_max):
    board = chess.Board()
    for row_index, row in enumerate(matrix_max):
        for col_index, piece in enumerate(row):
            square = chess.square(col_index, 7 - row_index)
            fen_piece = piece_symbols[piece]
            if fen_piece != '1':
                board.set_piece_at(square, chess.Piece.from_symbol(fen_piece))

# print the resulting FEN string
    print(board.fen())
    return board.fen()
