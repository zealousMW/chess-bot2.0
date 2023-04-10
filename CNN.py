# CNN
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, MaxPool2D, Flatten, Conv2D
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

f1 = ['r', 'n', 'b', 'q', 'k', 'p', 'mt']
f2 = ['P', 'Q', 'K', 'B', 'N', 'R']
label = []
images_data = []
for i in range(13):
    for j in range(1, 13):
        images_data.append(plt.imread(
            "dataset/"+str(i)+"/1 ("+str(j)+').png'))
        label.append(i)
images = np.array(images_data)
label = np.array(label)
X_train, X_test, y_train, y_test = train_test_split(
    images, label, test_size=0.25, random_state=42)
images = images/255
X_train = X_train/255
X_test = X_test/255
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
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10)
