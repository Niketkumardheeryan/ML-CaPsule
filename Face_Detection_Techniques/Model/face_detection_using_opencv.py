# -*- coding: utf-8 -*-
"""Face_Detection_Using_OpenCV.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MVyI90HVtEE_GWQ7bZLslgav2H42vqRL
"""

# import required modules 
import cv2
from google.colab.patches import cv2_imshow
!curl -o logo.png https://colab.research.google.com/img/colab_favicon_256px.png

# import the xml file defined by the haarcascade library 
from cv2 import CascadeClassifier
classifier=CascadeClassifier("/content/haarcascade_frontalface_alt.xml")

# import the image onto the notebook
img1="/content/image1.jpg"
pixels=cv2.imread(img1)

# function for detecting the faces and building a rectangle over the face
def face_detection(image):
  faces=classifier.detectMultiScale(image)
  for face in faces:
    x,y,w,h=face
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
  cv2_imshow(image)

face_detection(pixels)

# testing the function with another image
print("Now let us test for another image:")
img="/content/image2.jpg"
pixel=cv2.imread(img)
face_detection(pixel)