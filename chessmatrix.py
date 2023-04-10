import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

img_src = 'hello.png'

img = cv.imread(img_src)
img = cv.resize(img, (800, 800))
cv.imwrite('hello.png', img)
square = []
for i in range(8):
    for j in range(8):
        x = i*100
        y = j*100
        square.append(img[x:x+100, y:y+100])

# cv.imshow('img', square[0])
# if cv.waitKey(0) & 0xff == 27:
#    cv.destroyAllWindows()

squarecn = np.array(square)
squarecn = squarecn/255
model = load_model('model6.0.h5')
x = result = model.predict(squarecn)
for i in range(64):
    print(x[i].argmax())
"""square = np.array(square)
square = square.reshape(64, -1)
square = preprocessing.scale(square)
mode = pickle.load(open('model3.0_corrected.sav', 'rb'))
x = mode.predict(square)"""
