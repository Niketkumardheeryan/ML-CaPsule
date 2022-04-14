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

                    <--------------------Demo--------------------->
1).First of all clone the project on your system .
2). Now go to the project folder and open the Key-Frame-Extraction.ipynb file (if possible use jupyter notebook).
3). So to use jupyter notebook go to the Key-Frame-Extraction folder use shift + right click and then click on the open windows powershell here .
4).Now in the windows powershell type jupyter notebook.
5).Now jupyter notebook will open on your default browser.
6).Open the Key-Frame-Extraction.ipynb file .

How to execute the code : 
1)In the jupyter notebook you can execute the code using the shift + enter.
2).Execute the first cell containing the libraries.
3).Now execute the 2nd cell containing the code to convert the video into grayscale , canned , original ... now execute that cell .
4) In this next cell we have called the above function so when you execute this code block i.e the block number 3 then you will see the output it may be on your task bar but it will close after some time .So to look at the output when you execute the code look for python output file on your task bar and you can see the difference between the grayscale , canned , original video frames.
5).Also you will get the fps of the video.
6).You can also add your own video. So to add your own video just copy paste the desired video in the Key-Frame-Extraction folder and then copy the name of your video file and paste it in the frames,ogframes,fps = framing("##name of your video file").
7) Now just execute all the code blocks till the 11th block ... So basically in this 11th block all your keyframes out of the total frames of teh video would be saved as a .JPG file in the folder named 'Key_Frames' which would automatically created using the os module of python in your working directory.
8).Now when you see #SECOND PART IMAGE DETECTION FROM THE KEY FRAMES this comment for the particular code block ..... First go to the this link https://pjreddie.com/darknet/yolo/ search for the Row having YOLOv3-416 this name now in this row click on the cfg link which will download the architechture for the YOLO-V3 model and then click on the weights link which will download the weights for the model which is a quite a huge file so it may take some time to download .
9).Now after downloading these files copy and paste both these files into the Key-Frames-Extraction folder where you have all your other files.
10).Now copy the path for the cfg file and paste it in ... - net=cv2.dnn.readNet(r"paste your path in this line of code in these quotes"). Similarly copy the path for the weights file and psate that path into this line of code ... - 
net=cv2.dnn.readNet(r"paste path for weights", "paste path for .cfg file"). So paste both the paths in the same format only that is path of weights , path of cfg file inside the cv2.dnn.readNet function (dnn stands for deep neural networks).
11).Now in the block 14 just do what is go the Key-Frames folder where all key frames are saved as .JPG and copy the path for that folder and then paste that path in this line ... - path="paste the path in this line in the code of the block 14".
12).Now execute all the lines of the code and in the last block you will get the .JPG image labeled with the timestamp having the maximum number of objects , you can verify that by opening the video and going to exact same timestamp as written in the last block output.