import tkinter as tk
from tkinter import messagebox


def on_close():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        win.destroy()


def screenshot():
    dr.destroy()
    import pyautogui
    import time
    time.sleep(2)

    img = pyautogui.screenshot(region=(sx, sy, ex-sx, ey-sy))
    img.save('testss.png')


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
        global sx, sy, ex, ey
        sx = self.start_x
        sy = self.start_y
        ex, ey = self.cur_x, self.cur_y
        self.master.destroy()
        import pyautogui
        import time
        time.sleep(2)
        img = pyautogui.screenshot(region=(sx, sy, ex-sx, ey-sy))
        img.save('testss.png')
        print(sx, sy, ex, ey)


dr = tk.Tk()
dr.attributes('-fullscreen', True)
dr.attributes('-alpha', 0.5)
draw = RectangleDrawer(dr)
# dr.protocol("WM_DELETE_WINDOW", screenshot)
dr.mainloop()

win = tk.Tk()
win.title("chessbot")
win.geometry("500x500")
win.resizable(False, False)
win['bg'] = 'black'

text = tk.Label(win, width=50, height=25,
                text="Welcome to chess bot", bg='black', fg='white')
text.pack()
# button = tk.Button(win, text="Start", width=10, height=2,
#                  bg='black', fg='white', command=lambda: select_screen)
win.protocol("WM_DELETE_WINDOW", on_close)
win.mainloop()
