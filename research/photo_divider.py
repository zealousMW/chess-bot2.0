import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img_src = '9.png'
img = cv.imread(img_src)
img = cv.resize(img, (800, 800))
# dividing image into 64x64 blocks
square = []
for i in range(8):
    for j in range(8):
        x = i*100
        y = j*100
        square.append(img[x:x+100, y:y+100])

cv.imshow('img', square[0])
if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()
# saving images in sqaure list
for i in range(64):
    x = i
    cv.imwrite('dataset/9'+str(x)+'.png', square[i])
