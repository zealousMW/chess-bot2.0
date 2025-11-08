"""coordinateGetter.py

Minimal script that lets the user draw a rectangle over the screen
and prints the bounding coordinates to stdout. The user can copy those
coordinates into `finalcode.py` (manual paste as requested).

Usage: run the script and draw a rectangle with the mouse. When you
release the mouse the script prints: sx sy ex ey
"""

import tkinter as tk


class RectangleSelector:
    """A tiny transparent fullscreen selector that prints coords and exits."""

    def __init__(self):
        self.root = tk.Tk()
        # make window fullscreen and semi-transparent so user can see the board
        self.root.attributes("-fullscreen", True)
        try:
            self.root.attributes("-alpha", 0.25)
        except Exception:
            # some platforms may not support alpha; that's fine
            pass

        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self._start = None
        self._rect = None

    def on_press(self, event):
        self._start = (self.canvas.canvasx(event.x_root), self.canvas.canvasy(event.y_root))
        self._rect = self.canvas.create_rectangle(self._start[0], self._start[1], self._start[0], self._start[1], outline="red")

    def on_drag(self, event):
        if not self._rect:
            return
        x, y = (self.canvas.canvasx(event.x_root), self.canvas.canvasy(event.y_root))
        self.canvas.coords(self._rect, self._start[0], self._start[1], x, y)

    def on_release(self, event):
        # compute integer pixel coordinates in screen space (left, top, right, bottom)
        x1, y1 = self._start
        x2, y2 = (self.canvas.canvasx(event.x_root), self.canvas.canvasy(event.y_root))
        sx, sy = int(min(x1, x2)), int(min(y1, y2))
        ex, ey = int(max(x1, x2)), int(max(y1, y2))
        # print coordinates so the user can copy them
        print(sx, sy, ex, ey)
        # close the GUI
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def main():
    sel = RectangleSelector()
    sel.run()


if __name__ == "__main__":
    main()
