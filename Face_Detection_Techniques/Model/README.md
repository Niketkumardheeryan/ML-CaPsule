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

Image:

![image1](https://user-images.githubusercontent.com/65596711/122972111-690a0780-d3ad-11eb-80a8-a9bab3be68e8.jpg)

Applying the techniques we get:

![output_img_1](https://user-images.githubusercontent.com/65596711/122972283-98b90f80-d3ad-11eb-8638-76c29479a68e.png)
