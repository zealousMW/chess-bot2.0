import json
import os
import time
from typing import Tuple

import numpy as np
import pyautogui
import tkinter as tk
# optional pillow fallback used only if cv2 isn't installed
try:
    from PIL import Image
except Exception:
    Image = None


class RectangleDrawer:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.canvas.bind('<ButtonPress-1>', self.on_button_press)
        self.canvas.bind('<B1-Motion>', self.on_move_press)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_release)
        self.start_x = None
        self.start_y = None
        self.rect = None

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline='black')

    def on_move_press(self, event):
        self.cur_x = self.canvas.canvasx(event.x)
        self.cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x,
                           self.start_y, self.cur_x, self.cur_y)

    def on_button_release(self, event):
        self.master.coords = (int(self.start_x), int(self.start_y), int(self.cur_x), int(self.cur_y))
        self.master.destroy()


def calibrate(save_path: str = None) -> Tuple[int, int, int, int]:
    """Open a translucent full-screen window to draw a rectangle around the board.

    Returns (sx, sy, ex, ey) screen coordinates.
    If save_path is provided, a small json config will be written.
    """
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.35)
    root.coords = None
    RectangleDrawer(root)
    root.mainloop()

    if not root.coords:
        raise RuntimeError("Calibration cancelled or failed")

    sx, sy, ex, ey = root.coords

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'w') as f:
            json.dump({'sx': sx, 'sy': sy, 'ex': ex, 'ey': ey}, f)

    return sx, sy, ex, ey


def load_config(path: str):
    if not os.path.exists(path):
        return None
    import json
    with open(path, 'r') as f:
        return json.load(f)


def capture_board(sx: int, sy: int, ex: int, ey: int, resize: int = 800) -> np.ndarray:
    """Capture the screen region and return a BGR numpy array resized to (resize,resize).
    """
    img = pyautogui.screenshot(region=(sx, sy, ex - sx, ey - sy))
    img = np.array(img)  # RGB
    # Convert to BGR for OpenCV conventions if needed downstream
    img = img[:, :, ::-1]
    # Resize with simple numpy (nearest) or use cv2 if available
    try:
        import cv2 as cv
        img = cv.resize(img, (resize, resize))
    except Exception:
        # fallback: simple reshape (not ideal)
        img = np.array(Image.fromarray(img).resize((resize, resize)))
    return img
