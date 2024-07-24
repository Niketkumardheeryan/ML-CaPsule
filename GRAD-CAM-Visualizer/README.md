## GRAD-CAM Visualizer

### Libraries used
- numpy
- keras
- matplotlib
- tensorflow

### How to run
- Create a virtual environment using venv
- Activate the virtual environme
- Install dependencies
- Run the python notebook

### Overview

#### What is the Xception model
The Xception model, short for "Extreme Inception," is a deep convolutional neural network architecture. Xception builds upon the Inception architecture but replaces the standard Inception modules with depthwise separable convolutions.

#### What is GRAD-CAM
GRAD-CAM, which stands for Gradient-weighted Class Activation Mapping, is a technique used in the field of computer vision to visualize the regions of an image that are important for a convolutional neural network's decision-making process. So GRAD-CAM can be used to explain why the Xception model is classifying that as an "Persian cat" ( Or anything else ) visually through a heatmap.

#### Use Case
Since ML techniques like CNN are essentially "Black Boxes", it is hard for us to understand why it made that choice. Using GRAD-CAM we are able to explain why the CNN model made that particular choice that it did. It helps us to visually understand the "why" of the classification through a heatmap. So basically it helps us to understand visually on what features the CNN model is basing its decision on.

#### Results
In the [code](https://github.com/AMS003010/ML-CaPsule/blob/grad-cam-visualizer/GRAD-CAM-Visualizer/GRAD_CAM_Visualizer.ipynb), the `Xception` model(which is a prebuilt model in keras) is loaded and the below image is taken as input and the `imagenet` weights are loaded.

![dog_cat.png](https://github.com/AMS003010/ML-CaPsule/blob/grad-cam-visualizer/GRAD-CAM-Visualizer/dog_and_cat.png)

The model predicts it to be a 'golden_retriever' below

![image](https://github.com/user-attachments/assets/e044965a-655c-4aaf-b0cf-040bb86ede1b)

The final convulation layer is extracted to calculate the gradient and it is generated as a heatmap below

![image](https://github.com/user-attachments/assets/61af1076-f629-4536-a89b-1122b22ea549)

Finally the input image and generated heatmap is superimposed to generate the final output below which showcases "why" the `Xception` model classifies it as a 'golden_retriever'

![image](https://github.com/user-attachments/assets/ba06662f-b188-46b8-8863-be85066f1e95)

So you can see the features on which the model classifies it is highlighted in the above image.



