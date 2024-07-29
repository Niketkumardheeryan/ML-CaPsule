# Dog Breeds Classification

to predict correct dog breed labels corresponding to their dog images


Approach for this Project :

**Image segmentation**

is a crucial task in computer vision that involves identifying and classifying different regions or objects within an image. In this project, I will explore three different approaches for image segmentation using deep learning models: **VGG19**, **MobileNet** and **ResNet50V2**.

`ResNet50V2`

I have implemented a ResNet50V2 model for image classification using Keras. The ResNet50V2 model, pre-trained on the **ImageNet dataset**, serves as a powerful feature extractor. By freezing the pre-trained layers and adding additional layers for classification, we were able to achieve good performance on our image classification task.

`MobileNet`

By utilizing **transfer learning** with the MobileNet model, we can leverage pre-trained weights and significantly reduce the training time required for our image classification task. This approach is particularly useful when working with limited training data, as we can benefit from the rich representations learned by the base model on a large-scale dataset like ImageNet.

`vgg19`

VGG19 is a deep convolutional neural network architecture known for its exceptional performance in image recognition tasks. With 19 layers, it utilizes small convolutional filters and max-pooling layers to extract hierarchical features from images. VGG19 has been widely used as a benchmark model in computer vision research and has achieved remarkable accuracy in various image classification challenges.

**Visualization**
![predicted labels](https://github.com/aditya0929/Dog-Breeds-Classification/assets/127277877/37d63e3e-2083-42fa-97df-ee6912beda57)

Since the models' high levels of accuracy(90% and above) means that most of their pictures will be almost havinG similar predicted labels with little room for mistake, the anticipated labels for the vegetables are visualised as follows.

**Throughout the project,**

I will preprocess the dataset by resizing the images and splitting it into training,validation and testing sets. For training, I will employ a loss function suitable for image segmentation, such as cross-entropy loss, and optimize the models using technique like Adam optimization

**After training the models,**

I will evaluate their performance using appropriate metrics. Additionally, I will visualize the segmentation results to gain insights into how well the models can accurately identify and classify different regions within the vegetable images.

**Performance checker**

![Accuracy Evaluation](https://github.com/aditya0929/Dog-Breeds-Classification/assets/127277877/f6d43ce8-dfcd-4b6c-afbd-a90f28bacaff)

## after evaluation, `RESNET50V2` model looks to be the best fit model in this case of Dog Breed Classification .

## even though the other models also have a high accuracy and have complete capacity for executing the task and predicting the labels.

**Future Scope**

This project will contribute to advancing the understanding and application of deep learning in the field of computer vision and could potentially find applications in sorting of dog images based on different classes.