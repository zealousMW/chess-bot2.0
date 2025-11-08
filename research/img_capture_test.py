import cv2 as cv
import pyautogui
import numpy as np
# 229.0 118.0 1124.0 1016.0
# 297.0 169.0 1090.0 961.0
# 288.0 169.0 1079.0 961.0
sx = 288
sy = 169
ex = 1079
ey = 961
while True:
    img = pyautogui.screenshot(region=(sx, sy, ex-sx, ey-sy))
    img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
    img = cv.resize(img, (800, 800))

    cv.imshow('img', img)
    cv.imwrite('hello.png', img)
    if cv.waitKey(1) & 0xff == 27:
        break
cv.destroyAllWindows()
