# Driver Drowsiness Detection
This is a driver drowsiness detection project, that detects if the drivers eyes are closed for 15 continuous frames, then the system alerts the driver. The project uses OpenCV and Haarcascade classifier to detect the eyes. A CNN model is trained on the given dataset to detect whether the eye is open or closed.

## Libraries Used : 
### CNN Model
- tensorflow
- keras.preprocessing.image

### Driver Drowsiness Detection
- OpenCV
- keras.models
- tensorflow
- numpy
- keras.preprocessing

## Steps being followed :
### CNN Model
- Import Libraries
- Data Preprocessing
- Initializing CNN
- Convolutional Layer
- Max Pooling Layer
- Adding a second convolution and max pooling layer
- Flattening
- Full Connections
- Output Layer
- Training the CNN
- Saving the model

### Driver Drowsiness Detection
- Import Libraries
- Load CNN Model
- Face and Eye Detection using Haar Cascade
- Eye open or closed prediction using the CNN Model
- Alert if drowsy


## Demo
<img width="458" alt="image" src="https://user-images.githubusercontent.com/73430464/160766013-f7214357-ecf7-4463-b43f-077c45936da2.png">

