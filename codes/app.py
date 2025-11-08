import json
import os
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

from .capture import calibrate, load_config
from .chessbot_core import ChessBot


CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'calib.json')


class App:
    def __init__(self, root):
        self.root = root
        root.title('Chess Bot UI')

        self.bot = ChessBot(config_path=CONFIG_PATH)

        frm = tk.Frame(root)
        frm.pack(padx=10, pady=10)

        self.calib_btn = tk.Button(frm, text='Calibrate (select board)', command=self.calibrate)
        self.calib_btn.grid(row=0, column=0, padx=5, pady=5)

        self.detect_btn = tk.Button(frm, text='Detect board', command=self.detect)
        self.detect_btn.grid(row=0, column=1, padx=5, pady=5)

        self.suggest_btn = tk.Button(frm, text='Suggest move', command=self.suggest)
        self.suggest_btn.grid(row=0, column=2, padx=5, pady=5)

        self.exec_btn = tk.Button(frm, text='Execute move', command=self.execute_move)
        self.exec_btn.grid(row=0, column=3, padx=5, pady=5)

        # Engine settings frame
        settings_frm = tk.Frame(root)
        settings_frm.pack(padx=10, pady=(0, 10), fill=tk.X)

        tk.Label(settings_frm, text='Engine Hash (MB):').grid(row=0, column=0, sticky='e')
        self.hash_var = tk.StringVar(value=str(self.bot.engine.get_params().get('Hash', 1024)))
        self.hash_entry = tk.Entry(settings_frm, textvariable=self.hash_var, width=8)
        self.hash_entry.grid(row=0, column=1, padx=4)

        tk.Label(settings_frm, text='Threads:').grid(row=0, column=2, sticky='e')
        self.threads_var = tk.StringVar(value=str(self.bot.engine.get_params().get('Threads', 2)))
        self.threads_entry = tk.Entry(settings_frm, textvariable=self.threads_var, width=4)
        self.threads_entry.grid(row=0, column=3, padx=4)

        self.apply_engine_btn = tk.Button(settings_frm, text='Apply Engine Settings', command=self.apply_engine_settings)
        self.apply_engine_btn.grid(row=0, column=4, padx=8)

        # Side (white/black) selection
        tk.Label(settings_frm, text='Play as:').grid(row=1, column=0, sticky='e')
        self.side_var = tk.StringVar(value='w')
        self.white_rb = tk.Radiobutton(settings_frm, text='White', variable=self.side_var, value='w')
        self.white_rb.grid(row=1, column=1, sticky='w')
        self.black_rb = tk.Radiobutton(settings_frm, text='Black', variable=self.side_var, value='b')
        self.black_rb.grid(row=1, column=2, sticky='w')

        self.text = scrolledtext.ScrolledText(root, width=60, height=20)
        self.text.pack(padx=10, pady=10)

        self.current_matrix = None
        self.current_fen = None
        self.current_move = None

    def log(self, *parts):
        self.text.insert(tk.END, ' '.join(map(str, parts)) + '\n')
        self.text.see(tk.END)

    def calibrate(self):
        # run calibration in separate thread since it blocks with fullscreen tk
        def job():
            try:
                sx, sy, ex, ey = calibrate(save_path=CONFIG_PATH)
                self.bot.config = load_config(CONFIG_PATH)
                self.log('Calibration saved:', sx, sy, ex, ey)
            except Exception as e:
                messagebox.showerror('Calibration failed', str(e))

        threading.Thread(target=job, daemon=True).start()

    def apply_engine_settings(self):
        try:
            h = int(self.hash_var.get())
            t = int(self.threads_var.get())
        except Exception:
            messagebox.showerror('Invalid input', 'Hash and Threads must be integers')
            return
        try:
            self.bot.engine.update_params(hash_mb=h, threads=t)
            self.log(f'Engine parameters applied: Hash={h}MB, Threads={t}')
        except Exception as e:
            messagebox.showerror('Failed to apply', str(e))

    def detect(self):
        try:
            matrix = self.bot.capture_and_predict()
            self.current_matrix = matrix
            self.current_fen = self.bot.matrix_to_fen(matrix)
            self.log('Detected board:')
            for row in matrix:
                self.log(''.join(row))
            self.log('FEN:', self.current_fen)
        except Exception as e:
            messagebox.showerror('Detect failed', str(e))

    def suggest(self):
        if not self.current_fen:
            messagebox.showinfo('No board', 'Run Detect board first')
            return
        try:
            # use selected side from UI ("w" or "b")
            side = self.side_var.get() or 'w'
            move = self.bot.suggest_move(self.current_fen, side=side)
            self.current_move = move
            self.log('Suggested move:', move)
        except Exception as e:
            messagebox.showerror('Suggest failed', str(e))

    def execute_move(self):
        if not self.current_move:
            messagebox.showinfo('No move', 'Get a suggested move first')
            return
        try:
            centers = self.bot.square_centers()
            self.bot.engine.execute_move(self.current_move, centers)
            self.log('Executed move:', self.current_move)
        except Exception as e:
            messagebox.showerror('Execute failed', str(e))


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
