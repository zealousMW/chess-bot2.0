import os
from typing import Tuple

import pyautogui
from stockfish import Stockfish


class Engine:
    def __init__(self, exe_path: str = None, depth: int = 12, hash_mb: int = 1024, threads: int = 2):
        if exe_path is None:
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            exe_path = os.path.join(base, 'stockfish_15.1_win_x64_avx2', 'sk.exe')
        if not os.path.exists(exe_path):
            raise FileNotFoundError(f"Stockfish binary not found: {exe_path}")
        self.sf = Stockfish(exe_path)
        self.sf.set_depth(depth)
        # store current params
        self.params = {
            "Hash": int(hash_mb),
            "Threads": int(threads),
        }
        try:
            self.sf.update_engine_parameters(self.params)
        except Exception:
            # some stockfish wrappers or versions may not support parameter setting
            pass

    def best_move(self, fen: str, time_ms: int = 1000) -> str:
        # expect fen to be a valid FEN string (with side to move etc.)
        self.sf.set_fen_position(fen)
        # prefer time-limited call if available
        try:
            return self.sf.get_best_move_time(time_ms)
        except Exception:
            return self.sf.get_best_move()

    def update_params(self, hash_mb: int = None, threads: int = None):
        """Update engine tuning parameters (Hash in MB, Threads count)."""
        changed = {}
        if hash_mb is not None:
            self.params['Hash'] = int(hash_mb)
            changed['Hash'] = int(hash_mb)
        if threads is not None:
            self.params['Threads'] = int(threads)
            changed['Threads'] = int(threads)
        if changed:
            try:
                self.sf.update_engine_parameters(changed)
            except Exception:
                pass

    def get_params(self):
        return dict(self.params)

    def execute_move(self, uci: str, square_centers: dict):
        # uci like 'e2e4'
        start, end = uci[:2], uci[2:]
        if start not in square_centers or end not in square_centers:
            raise KeyError("Square not found in centers mapping")
        pyautogui.click(square_centers[start])
        pyautogui.click(square_centers[end])
