import cv2
import numpy as np
from matplotlib import pyplot as plt

image = cv2.imread('forest.jpg',0)
ret,thres1 = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
ret,thres2 = cv2.threshold(image,127,255,cv2.THRESH_BINARY_INV)
ret,thres3 = cv2.threshold(image,127,255,cv2.THRESH_TRUNC)
ret,thres4 = cv2.threshold(image,127,255,cv2.THRESH_TOZERO)
ret,thres5 = cv2.threshold(image,127,255,cv2.THRESH_TOZERO_INV)

titles = ['Original Image','BINARY Image','BINARY_INV Image','TRUNC Image','TOZERO Image','TOZERO_INV Image']
images = [image, thres1, thres2, thres3, thres4, thres5]

for i in range(6):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()