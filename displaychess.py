import tkinter as tk
from PIL import Image, ImageTk
import chess.svg
import io
from cairosvg import svg2png

# Create a Tkinter window
window = tk.Tk()
window.title("Chess Board")

# Create a canvas to display the chess board
canvas = tk.Canvas(window, width=800, height=800)
canvas.pack()

# Load the chess board image using the python-chess library
board = chess.Board()
svg_image = chess.svg.board(board, size=800)
png_bytes = svg2png(bytestring=svg_image.encode('utf-8'))
board_image = Image.open(io.BytesIO(svg_image))
photo = ImageTk.PhotoImage(board_image)

# Add the chess board image to the canvas
canvas.create_image(0, 0, image=photo, anchor='nw')

# Run the Tkinter event loop
window.mainloop()
