import cv2
from tensorflow import keras
from keras.applications.resnet50 import ResNet50, decode_predictions

resnet = ResNet50()
img = cv2.imread('static/images/uploads/bird2.jpg', -1)
img = cv2.resize(img, (224, 224))
yhat = resnet.predict(img.reshape(-1, 224, 224, 3))
label = decode_predictions(yhat)
#label = label[0][0]
print(label[0][0][1])