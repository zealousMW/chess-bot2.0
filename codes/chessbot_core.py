import os
from typing import Tuple, Dict

import numpy as np

from .capture import capture_board, load_config
from .model_wrapper import ModelWrapper
from .engine import Engine
from . import chess_bot_need as cbn


def make_square_centers(sx: int, sy: int, ex: int, ey: int) -> Dict[str, Tuple[int, int]]:
    # compute centers mapping a8..h1
    square_size = (ex - sx) // 8
    centers = {}
    for row in range(8):
        for col in range(8):
            x = sx + col * square_size + square_size // 2
            y = sy + row * square_size + square_size // 2
            # file a..h and rank 8..1
            sq = chr(col + ord('a')) + str(8 - row)
            centers[sq] = (x, y)
    return centers


class ChessBot:
    def __init__(self, model_path: str = None, stockfish_path: str = None, config_path: str = None):
        self.model = ModelWrapper(model_path)
        self.engine = Engine(stockfish_path)
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'calib.json')
        self.config_path = config_path
        self.config = load_config(config_path) or {}

    def capture_and_predict(self):
        if not self.config:
            raise RuntimeError('No calibration config available; run calibration first')
        sx, sy, ex, ey = self.config['sx'], self.config['sy'], self.config['ex'], self.config['ey']
        img = capture_board(sx, sy, ex, ey, resize=800)
        matrix = self.model.predict_board(img)
        return matrix

    def matrix_to_fen(self, matrix):
        # reuse existing helper
        return cbn.board_to_fen(matrix)

    def suggest_move(self, fen: str, side: str = 'w', time_ms: int = 1000):
        """Ask the engine for a best move. `side` should be 'w' or 'b'.

        fen: board piece placement string (without side/castling info).
        This method appends the side and passes to the engine.
        """
        if side not in ('w', 'b'):
            raise ValueError("side must be 'w' or 'b'")
        fen_full = fen + ' ' + side
        return self.engine.best_move(fen_full, time_ms=time_ms)

    def square_centers(self):
        if not self.config:
            raise RuntimeError('No calibration config available')
        return make_square_centers(self.config['sx'], self.config['sy'], self.config['ex'], self.config['ey'])
