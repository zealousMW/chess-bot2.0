import pyautogui

# Define the start and end positions of the chess board on the screen
sx = 297
sy = 169
ex = 1090
ey = 961

# Map chess board squares to screen coordinates
square_size = (ex - sx) // 8
square_centers = {}
for row in range(8):
    for col in range(8):
        x = sx + col * square_size + square_size // 2
        y = sy + row * square_size + square_size // 2
        square_centers[chr(col + ord('a')) + str(8 - row)] = (x, y)

# Example input for testing
input_str = 'e2e3'

# Get start and end positions from input string
start_pos, end_pos = input_str[:2], input_str[2:]

# Click on the start and end positions
pyautogui.click(square_centers[start_pos])
pyautogui.click(square_centers[end_pos])
