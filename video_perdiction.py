import numpy as np
import cv2 as cv
import numpy as np
from tensorflow.keras.models import load_model
import pyautogui
from stockfish import Stockfish
import chess
import chess_bot_need as cbn
sf = Stockfish('stockfish_15.1_win_x64_avx2/sk.exe')
sf.set_depth(20)
sf.set_skill_level(20)
sf.update_engine_parameters({"Hash": 4096, "Threads": 4})
# 229.0 118.0 1124.0 1016.0
# 298.0 169.0 1089.0 962.0

sx = 288
sy = 169
ex = 1081
ey = 962
cp = ['.', 'r', 'n', 'b', 'k', 'q', 'p', 'R', 'N', 'B', 'K', 'Q', 'P']


def board_to_fen(board):
    fen = ''
    empty_count = 0

    for row in board:
        for square in row:
            if square == '.':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0
                fen += square
        if empty_count > 0:
            fen += str(empty_count)
            empty_count = 0
        fen += '/'

    # Remove the trailing '/'
    fen = fen[:-1]

    return fen


while True:
    img = pyautogui.screenshot(region=(sx, sy, ex-sx, ey-sy))
    # img = cv.imread('sample4.png')
    img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    cv.imwrite('hello.png', img)
    img = cv.imread('hello.png')
    img = cv.resize(img, (800, 800))
    square = []
    for i in range(8):
        for j in range(8):
            x = i*100
            y = j*100
            square.append(img[x:x+100, y:y+100])
    squarecn = np.array(square)
    squarecn = squarecn/255
    model = load_model('model6.0.h5')
    x = result = model.predict(squarecn)
    data = []
    for i in range(64):
        data.append(x[i].argmax())
    matrix = []
    for i in data:
        matrix.append(cp[i])
    matrix_max = []
    print(matrix_max)
    for i in range(0, 64, 8):
        row = matrix[i:i+8]
        matrix_max.append(row)
    print(matrix_max)
    fen = cbn.board_to_fen(matrix_max)
    print(fen)
    sf.set_fen_position(fen)
    print(sf.get_best_move())
    cv.imshow('img', img)
    # cv.imwrite('hello.png', img)
    if cv.waitKey(1) & 0xff == 27:
        break
cv.destroyAllWindows()
