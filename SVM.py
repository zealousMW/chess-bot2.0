import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, preprocessing
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import metrics

images_data = []
for i in range(64):
    images_data.append(plt.imread('dataset/square'+str(i+63)+'.png'))
images = np.array(images_data)
labels = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r',
          'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p',
          '.', '.', '.', '.', '.', '.', '.', '.',
          '.', '.', '.', '.', '.', '.', '.', '.',
          '.', '.', '.', '.', '.', '.', '.', '.',
          '.', '.', '.', '.', '.', '.', '.', '.',
          'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P',
          'R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
data_size = len(images_data)
images = images.reshape(data_size, -1)
images = preprocessing.scale(images)
X_train, X_test, y_train, y_test = train_test_split(
    images, labels, test_size=0.7, random_state=42)
svm_classifer = SVC(gamma=0.001)
svm_classifer.fit(images, labels)
predictions = svm_classifer.predict(X_test)
print("accuracy", metrics.accuracy_score(y_test, predictions) * 100)

# saving model
filename = 'model.sav'
pickle.dump(svm_classifer, open(filename, 'wb'))

# loading model again
