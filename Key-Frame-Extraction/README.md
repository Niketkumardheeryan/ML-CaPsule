Hey Folks !! This is Omkar Malpure !!
So this is my project Key frames extraction from a video and also performing object detection using YOLO V3 for each key frame.

--- So the main objective of this project is to extract key frames from a video and perform object detection for each keyframe that is this YOLO V3 will exactly detect the number of objects in that key frames and will also try tell us name of that object.This may used for security purpose , for analyzing large videos , etc.

Libraries used - OpenCV
                 numpy
                 os

Model Used - YOLO V3 
            - This YOLO V3 model is trained on COCO dataset which has 80 classification labels in it.

Note - You will have to download the files named yolov3.weights and yolov3.cfg files for importing the weights and the architecture of the model respectively.
I am attaching the link to download the yolov3.weights and yolov3.cfg .... https://pjreddie.com/darknet/yolo/ .
Now from this link just download the weights and cfg related to 35 fps .

