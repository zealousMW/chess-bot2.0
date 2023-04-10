from tensorflow.keras.models import load_model
import numpy as np
import cv2 as cv
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPool2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Dense
import pyautogui
from stockfish import Stockfish
import chess_bot_need as cbn
import chess
import time
sf = Stockfish('stockfish_15.1_win_x64_avx2/sk.exe')
sf.set_depth(20)
sf.set_skill_level(20)
sf.update_engine_parameters({"Hash": 4096, "Threads": 4})


model = Sequential()
model.add(Conv2D(64, (3, 3), activation='relu', input_shape=(100, 100, 3)))
model.add(MaxPool2D(2, 2))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPool2D(2, 2))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPool2D(2, 2))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(13, activation='softmax'))
model = load_model('model4.0.h5')
# 298.0 169.0 1089.0 962.0
sx = 298
sy = 169
ex = 1089
ey = 962
square_size = (ex - sx) // 8
square_centers = {}
for row in range(8):
    for col in range(8):
        x = sx + col * square_size + square_size // 2
        y = sy + row * square_size + square_size // 2
        square_centers[chr(col + ord('a')) + str(8 - row)] = (x, y)


def move():
    img = pyautogui.screenshot(region=(sx, sy, ex-sx, ey-sy))
    img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    # img_src = 'hello.png'
    # img = cv.imread(img_src)
    img = cv.resize(img, (800, 800))
    cp = ['.', 'r', 'n', 'b', 'k', 'q', 'p', 'R', 'N', 'B', 'K', 'Q', 'P']
    square = []
    for i in range(8):
        for j in range(8):
            x = i*100
            y = j*100
            square.append(img[x:x+100, y:y+100])
    square = np.array(square)
    square = square/255
    square.shape

    x = model.predict([square])
    data = []
    matrix = []
    for i in range(64):
        data.append(np.argmax(x[i]))
    for i in data:
        matrix.append(cp[i])
    matrix_max = []
    for i in range(0, 64, 8):
        row = matrix[i:i+8]
        matrix_max.append(row)
    print(matrix_max)
    fen = cbn.board_to_fen(matrix_max)
    print(fen)
    print(sf.is_fen_valid(fen+' w KQkq - 0 1'))
    sf.set_fen_position(fen+' w')
    print(sf.get_best_move())
    input_str = sf.get_best_move_time(1000)
    start_pos, end_pos = input_str[:2], input_str[2:]
    print(input_str)
    pyautogui.click(square_centers[start_pos])
    pyautogui.click(square_centers[end_pos])


while True:
    input()
    move()
