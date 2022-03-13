#importing necessary libraries
import cv2
import imutils
from imutils.object_detection import non_max_suppression

#video capture
cap=cv2.VideoCapture("Video1.mp4")

#Initializing the HOG person
hog=cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

while True:
    success,image=cap.read()   #reading frames of video

    imgRGB=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)  #converting to grayscale
    image=imutils.resize(imgRGB,width=min(800,image.shape[1]))  #resizing 

    #detecting all humans
    (humans,_)=hog.detectMultiScale(image,
                                winStride=(5,5),
                                padding=(3,3),
                                scale=1.21)

    #applying non max suppression
    humans_nms=non_max_suppression(humans,probs=None,overlapThresh=0.65)
    counter=0           #initializing the counter                 

    #drawing the rectangle regions
    for(x,y,w,h) in humans_nms:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
        counter+=1  #increasing the counter

    #displaying number of humans in frame
    cv2.putText(image,f'Number of Humans:{int(counter)}',(5,30),cv2.FONT_HERSHEY_COMPLEX,.7,(255,0,0),1)
    
    #displaying output
    cv2.imshow('image',image)
    cv2.waitKey(1)
                                