import cv2 as cv
from cvzone.HandTrackingModule import HandDetector

cap=cv.VideoCapture(0)
hd=HandDetector()

image=cv.imread('gates.jpg')
image=cv.resize(image,(150,150))
x,y=100,100

while 1:
    h,w,c=image.shape
    ret,img=cap.read()
    
    img=cv.flip(img,1)
    hands,img=hd.findHands(img,flipType=False)
    
    if hands:
        lm=hands[0]['lmList']
        #print(lm)
        length,info,img=hd.findDistance(lm[8][0:2],lm[4][0:2],img)
        print(length) 
        
        if length<20:
            pointer=lm[8]
            if x <pointer[0]<x+w and y<pointer[1]<y+h:  
                x,y=pointer[0]-w//2,pointer[1]-h//2
    img[y:y+h,x:x+w]=image
    cv.imshow('frame',img)
    cv.waitKey(1)