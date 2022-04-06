Introduction : Hey Folks !! This is Omkar Malpure !!
So this is my project Key frames extraction from a video and also performing object detection using YOLO V3 for each key frame.

Objective :  So the main objective of this project is to extract key frames from a video and perform object detection for each keyframe that is this YOLO V3 will exactly detect the number of objects in that key frames and will also try tell us name of that object.This may used for security purpose , for analyzing large videos , etc.

Libraries used : OpenCV
                 numpy
                 os

Model Used : YOLO V3 
Information about the Model : This YOLO V3 model is trained on COCO dataset which has 80 classification labels in it.

FILES TO DOWNLOAD : 
1).You will have to download the files named yolov3.weights and yolov3.cfg files for importing the weights and the architecture of the model respectively.

2).I am attaching the link to download the yolov3.weights and yolov3.cfg  : https://pjreddie.com/darknet/yolo/ .

3). Now from this link just download the weights and cfg link written on the side of 35 fps .

STEPS : 
1).Extracted the key frames from the video.
2).Then Stored each key frame with its timestamp as the name of the image in a folder.
3).Now imported the YOLO V3 model and its architechture.
4).Then feeded all the key frames to the yolo V3 model and performed object detection and counted the number of objects for that frame .
5).Then found the frame having the maximum number of objects in it.

