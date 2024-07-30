<h1>PROJECT TITLE</h1>
<br>
<h3>
<u>Staircases Segmentation Using DL</u></h3>
<br>
<h1>GOAL</h1>
<br>

The project uses 50 images of ascending and 50 images of descending stairs.The aim is to classify the stair image as ascending and descending.<br>
The models used are Transfer Learning models which are pretrained on the imagenet weights.
<br>
Staircase Segmentation has usage in robot training in the area of surveillance for military and industrial applications.For behaviour cloning and automation puroses.
<br>



<h1>DATASET</h1>
<br>
The  Dataset is taken from Kaggle
<br>
Dataset Link :- https://www.kaggle.com/datasets/akshaydattatraykhare/ascending-and-descending-staircases
<br>
Description
<br>
There are two folders within the dataset ,one for images of ascending staircases and the other one for descending staircases.Each folder contains 50 images of ascending staircases and 50 images of descending staircases respectively. These images have been taken using mobile phone's camera. This dataset includes interior staircases and exterior staircases of various houses. This dataset can be helpful in detection and classification of ascending and descending staircases.<br>

<h1>DESCRIPTION</h1>

The project aims at classifying the images of the staircases as ascending and descending by using Transfer Learning Models which are pretrained on imagenet weights.<br>
<br>
<h2>METHODOLOGY</h2>
<br>
<ol>
<li>The necessary libraries are imported and installed.</li><li>The dataset has only 100 images in total which is very less to create a robust model.To increasethe robustness and to increase the data samples,images are augmented using Augmentor by flipping,rotating,skewing,zooming,resizing the images and creating 500 samples for each label that is in total 1000 image samples are created by augmenting them from 100 samples of both ascending and descending images.An array of these 1000 samples concatenated with label(Ascending and Descending) is formed into a dataset which will be used for training and testing of the model.</li><li>The dataset is split into training and testing using train_test_split function of sklearn.The train size is kept 0.7 for all the models.</li><li>Label Encoder is used to encode the labels into 0 and 1</li><li>Normalization is done to normzalise the pixel values between 0 and 1</li>
<li>Four Transfer Learning models namely MobileNetV2,VGG16,XCeption,InceptionV3 are used for the training purpose.Sequential models are created of baseline transfer learning models along with convoluted layer,dense layers.Dropout layer is used to avoid overfitting of the model.</li>
<li>Loss Function used is Binary Crossentropy,optimizer is Adam,Metrics is Accuracy</li>
<li>Models are trained on number of epochs value ranging from 25 to 50.</li>
<li>To analyse the accuracy and loss Confusion Matrix,Classification Report,Accuracy Graph (Training Accuracy VS Validation Accuracy),Loss Graph(Training Accuracy VS Validation Accuracy) are generated.
</li>
<li>Some test samples are used to test on the trained models and predictions are made.
</li>
</ol>
<br>
<h1>MODELS USED</h1>
<br>

Transfer Learning Models pretrained on imagenet weights are used for training.Four Models namely MobileNetV2,VGG16,XCeption,InceptionV3 are used.These models are robust and have high learning rate as they are been already trained on similiar data that is imagenet.So they give better accuracy and training.
For each model different number of convolutional,dense and dropout layers are used as per their training accuracy.
Every model is different in its pursuit and are easy trainable.
<br>
<h1>MODELS USED</h1>
<br>

Transfer Learning Models pretrained on imagenet weights are used for training.Four Models namely MobileNetV2,VGG16,XCeption,InceptionV3 are used.These models are robust and have high learning rate as they are been already trained on similiar data that is imagenet.So they give better accuracy and training.
For each model different number of convolutional,dense and dropout layers are used as per their training accuracy.
Every model is different in its pursuit and are easy trainable.
<br>
<h1>BRIEF DESCRIPTION OF MODELS AND THE RESULTS OBTAINED FROM THEM</h1>
<br>
<h1>1. MOBILENETV2 MODEL</h1>
<br>

![mobilenet conv blocks](https://github.com/kanishkakataria/Images/assets/85161519/142333e3-efcf-4386-8bfd-eede3aa842d2)<br>
Depthwise Separable Convolution is introduced which dramatically reduce the complexity cost and model size of the network, which is suitable to Mobile devices, or any devices with low computational power. In MobileNetV2, a better module is introduced with inverted residual structure. Non-linearities in narrow layers are removed this time. With MobileNetV2 as backbone for feature extraction, state-of-the-art performances are also achieved for object detection and semantic segmentation. 

<br>
<ol>
<li>In MobileNetV2, there are two types of blocks. One is residual block with stride of 1. Another one is block with stride of 2 for downsizing.</li>
<li>There are 3 layers for both types of blocks.</li>
<li>This time, the first layer is 1×1 convolution with ReLU6.</li>
<li>The second layer is the depthwise convolution.</li>
<li>The third layer is another 1×1 convolution but without any non-linearity. It is claimed that if ReLU is used again, the deep networks only have the power of a linear classifier on the non-zero volume part of the output domain.</li>
<li>The third layer is another 1×1 convolution but without any non-linearity. It is claimed that if ReLU is used again, the deep networks only have the power of a linear classifier on the non-zero volume part of the output domain.</li>
</ol>
<br>
<h1>2. VGG16 MODEL</h1>
<br>

![model architecture](https://github.com/kanishkakataria/Images/assets/85161519/e8c87859-695f-448e-bb54-1bb78a6c3744)
<br>
A convolutional neural network is also known as a ConvNet, which is a kind of artificial neural network. A convolutional neural network has an input layer, an output layer, and various hidden layers. VGG16 is a type of CNN (Convolutional Neural Network) that is considered to be one of the best computer vision models to date. The creators of this model evaluated the networks and increased the depth using an architecture with very small (3 × 3) convolution filters, which showed a significant improvement on the prior-art configurations. They pushed the depth to 16–19 weight layers making it approx — 138 trainable parameters.

<h2>USAGE</h2>

VGG16 is object detection and classification algorithm which is able to classify 1000 images of 1000 different categories with 92.7% accuracy. It is one of the popular algorithms for image classification and is easy to use with transfer learning.

<h1>ARCHITECTURE</h1>
<ol>
<li>The 16 in VGG16 refers to 16 layers that have weights. In VGG16 there are thirteen convolutional layers, five Max Pooling layers, and three Dense layers which sum up to 21 layers but it has only sixteen weight layers i.e., learnable parameters layer.
</li>
<li>VGG16 takes input tensor size as 224, 244 with 3 RGB channel</li>
<li>Most unique thing about VGG16 is that instead of having a large number of hyper-parameters they focused on having convolution layers of 3x3 filter with stride 1 and always used the same padding and maxpool layer of 2x2 filter of stride 2.</li>
<li>The convolution and max pool layers are consistently arranged throughout the whole architecture</li>
<li>Conv-1 Layer has 64 number of filters, Conv-2 has 128 filters, Conv-3 has 256 filters, Conv 4 and Conv 5 has 512 filters.
Three Fully-Connected (FC) layers follow a stack of convolutional layers: the first two have 4096 channels each, the third performs 1000-way ILSVRC classification and thus contains 1000 channels (one for each class). The final layer is the soft-max layer.</li>
</ol>
<br>
<h1>3. INCEPTIONV3 MODEL</h1>
<br>

![model architecture](https://github.com/kanishkakataria/Images/assets/85161519/e697b22d-0fa8-42b9-a5ba-2fe482bad7fb)<br>
The Inception V3 is a deep learning model based on Convolutional Neural Networks, which is used for image classification. The inception V3 is a superior version of the basic model Inception V1 which was introduced as GoogLeNet in 2014. As the name suggests it was developed by a team at Google.
<br>
The inception v3 model was released in the year 2015, it has a total of 42 layers and a lower error rate than its predecessors. Let's look at what are the different optimizations that make the inception V3 model better.
<br>
<h4>The major modifications done on the Inception V3 model are:-</h4>
<ol>
<li>Factorization into Smaller Convolutions
</li> 
<li>Spatial Factorization into Asymmetric Convolutions</li>
<li>Utility of Auxiliary Classifiers</li>
<li>Efficient Grid Size Reduction</li>
</ol>
<br>
The inception V3 is just the advanced and optimized version of the inception V1 model. The Inception V3 model used several techniques for optimizing the network for better model adaptation.
<br>
<ol>
<li>It has higher efficiency</li>
<li>It has a deeper network compared to the Inception V1 and V2 models, but its speed isn't compromised.</li>
<li>It is computationally less expensive.</li>
<li>It uses auxiliary Classifiers as regularizes.</li>
</ol>
<br>

<h2>XCEPTION MODEL</h2>
<br>

![Modified Deptthwise Separable Convolution in Xception](https://github.com/kanishkakataria/Images/assets/85161519/84790e95-81e7-495e-9ba8-f96d7391330c)
<br>
Xception is a deep convolutional neural network architecture that involves Depthwise Separable Convolutions. It was developed by Google researchers. Google presented an interpretation of Inception modules in convolutional neural networks as being an intermediate step in-between regular convolution and the depthwise separable convolution operation (a depthwise convolution followed by a pointwise convolution). In this light, a depthwise separable convolution can be understood as an Inception module with a maximally large number of towers. This observation leads them to propose a novel deep convolutional neural network architecture inspired by Inception, where Inception modules have been replaced with depthwise separable convolutions.<br>
The modified depthwise separable convolution is the pointwise convolution followed by a depthwise convolution. This modification is motivated by the inception module in Inception-v3 that 1×1 convolution is done first before any n×n spatial convolutions. Thus, it is a bit different from the original one. (n=3 here since 3×3 spatial convolutions are used in Inception-v3.)
<br>
<h2>Two minor differences:</h2>
<br>
1. The order of operations: As mentioned, the original depthwise separable convolutions as usually implemented (e.g. in TensorFlow) perform first channel-wise spatial convolution and then perform 1×1 convolution whereas the modified depthwise separable convolution perform 1×1 convolution first then channel-wise spatial convolution. This is claimed to be unimportant because when it is used in stacked setting, there are only small differences appeared at the beginning and at the end of all the chained inception modules.
<br>
2. The Presence/Absence of Non-Linearity: In the original Inception Module, there is non-linearity after first operation. In Xception, the modified depthwise separable convolution, there is NO intermediate ReLU non-linearity.

<h1>LIBRARIES NEEDED</h1>

The following libraries are essential :-
<br>
<ol>
<li>Keras - open source python library which facilitates deep neural networks like convolutional ,recurrent and their combinations</li>
<li>Tensorflow - open source library which supports Machine Learning powered models and applications.It also works with Keras and is of high utility </li>
<li>Scikit-learn - Simple and efficient tools for data mining and data analysis. It features various classification, regression and clustering algorithms including support vector machines, random forests, gradient boosting, k-means.
</li>

<h1>VISUALIZATION</h1>

<h2>ACCURACY CURVE<h2>

![Mobilenet_acc_curve ](https://github.com/kanishkakataria/Images/assets/85161519/40135c42-46df-40f4-9aba-1cfdc8d0be2d)
<br>
MOBILENET ACCURACY CURVE<br>
![Xception_acc_graph](https://github.com/kanishkakataria/Images/assets/85161519/379debcf-9739-477c-b8bd-40735f86ad46)
<br>
XCEPTION ACCURACY CURVE<br>
![InceptionV3_ACC graph](https://github.com/kanishkakataria/Images/assets/85161519/7d4ea849-13c7-4c70-bc9e-6f17942f3b0e)
<br>
INCEPTIONV3 ACCURACY CURVE<br>
![VGG16_acc_curve](https://github.com/kanishkakataria/Images/assets/85161519/483b35b1-f711-49b1-ba5a-e2ceb6776544)
<br>
VGG16 ACCURACY CURVE
<br>
<h2>LOSS CURVE<h2>

![Mobilenet_loss_Curve](https://github.com/kanishkakataria/Images/assets/85161519/ee7c40f1-e7a2-4b1e-881d-c5767a1087ef)
<br>
MOBILENET LOSS CURVE<br>
![Xception_loss_curve](https://github.com/kanishkakataria/Images/assets/85161519/ec725122-8a07-41f8-a74f-7e051f4263b0)
<br>
XCEPTION LOSS CURVE<br>

![InceptionV3_loss_graph](https://github.com/kanishkakataria/Images/assets/85161519/7352f92a-f79f-4502-8770-91762f97d86a)
<br>
INCEPTIONV3 LOSS CURVE<br>
![VGG16_loss_curve](https://github.com/kanishkakataria/Images/assets/85161519/0ce9b5c3-78e2-4da3-9bf4-be3d98ebf7b6)
<br>
VGG16 LOSS CURVE
<br>
<h1>ACCURACIES</h1>
<ol>
<li>MOBILENETV2 - 99.9%</li>
<li>VGG16 - 99.5%</li>
<li>INCEPTIONV3 - 99%</li>
<li>XCEPTION - 99.8%</li>

</ol>

<h1>CONCLUSION</h1>

The models are trained well with validation accuracies close to 99.9% in MobilenetV2,Inception,Xception and 99.5% in VGG16
To avoid overfitting augmentation,dropout layers was used.The number of layers,train test split and batch size was changed to peform trial and testing for better accuracies.

VGG16 model is said to be the best as it is not overfitting and generalises the data well comparatively.This is clearily shown in the predictions made through test samples on the trained model.

<h1>CONTRIBUTOR</h1>

NAME - KANISHKA KATARIA
<br>
GITHUB - https://github.com/kanishkakataria
<br>
LINKEDIN - https://kanishkakataria.vercel.app/
<br>
PORTFOLIO -https://kanishkakataria.vercel.app/
