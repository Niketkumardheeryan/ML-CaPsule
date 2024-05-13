# Hindi Letter Classification

## Introduction

This is a hindi letter classification web application created usinfg python and utilizes Convolutional Neural Networks, it utilizes
LENET-5 architecture. This architecture was created in 1998. We can also use other architectures like ALEXNET, GoogleNET, RESNET, VGGNET etc.

![Alt text](https://indiatyping.com/images/Hindi_Alphabets.webp "Hindi letters")

## Web Application

The web app is created using streamlit framework. It contains a heading, small introduction and then a image uploader. After the user uploads image, the image goes to backend and respected class is predicted by the CNN model and then the uploaded image along with prediction is showed. We can play with prediciton time and accuracy by changing batch_size, number of epochs and using a different CNN architecture.

## Libraries used

1. Numpy
2. Keras
3. Tensorflow
4. Streamlit

# How to run locally

install the necessary libraries using pip
open the project folder
Run following command : 

```python

streamlit run file_name.py

```

# Snapshots

![Alt text](https://ibb.co/0C1HFVn "Snapshot 1")
![Alt text](https://ibb.co/p1jw0RD "Snapshot 2")
