import os
from typing import Tuple

import pyautogui
from stockfish import Stockfish


class Engine:
    def __init__(self, exe_path: str = None, depth: int = 12):
        if exe_path is None:
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            exe_path = os.path.join(base, 'stockfish_15.1_win_x64_avx2', 'sk.exe')
        if not os.path.exists(exe_path):
            raise FileNotFoundError(f"Stockfish binary not found: {exe_path}")
        self.sf = Stockfish(exe_path)
        self.sf.set_depth(depth)
        try:
            self.sf.update_engine_parameters({"Hash": 1024, "Threads": 2})
        except Exception:
            pass

    def best_move(self, fen: str, time_ms: int = 1000) -> str:
        # expect fen to be a valid FEN string (with side to move etc.)
        self.sf.set_fen_position(fen)
        # prefer time-limited call if available
        try:
            return self.sf.get_best_move_time(time_ms)
        except Exception:
            return self.sf.get_best_move()

    def execute_move(self, uci: str, square_centers: dict):
        # uci like 'e2e4'
        start, end = uci[:2], uci[2:]
        if start not in square_centers or end not in square_centers:
            raise KeyError("Square not found in centers mapping")
        pyautogui.click(square_centers[start])
        pyautogui.click(square_centers[end])
