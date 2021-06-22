**Face Detection Techniques**

**Goal:** This project identifies the faces in an image and plots a rectangular box around the face.

**What I have done :**

- I have implemented this project using two techniques:
        1.Using Deep Learning
        2.Using OpenCV
     
- Firstly I have imported the required libraries, and loaded the image onto the notebook.

- Read the image loaded using imread of cv2 module.

- I have written functions of respective techniques which helps us to implement it again on different images.

- 1. Using Deep Learning:
		- For implementing facial detection in deep learning, I have implemented it using MTCNN technique -(Multi Task Cascade convolutional Neural Networks) 
		- Firstly we need to resize the image.
		
		- Then detect the faces using mtcnn classifier.
		
		- Plot the rectangular plot around the faces.

- 2. Using OpenCV:
	- For implementing using OpenCV , firstly we need to download the harcascade library's frontal face xml file.
	- Then detect the faces using Multi scale classifier
	- Plot the rectangular plot around the faces.


**Libraries Needed:**  cv2, tensorflow, mtcnn,
