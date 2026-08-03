<h1>Convolutional Neural Network(CNN):</h1>

<h2>What is a Convolutional Neural Network (CNN)?</h2>

A Convolutional Neural Network (CNN) is a type of deep learning model designed primarily for processing structured grid data, such as images. CNNs are particularly effective in image and video recognition, classification, and other tasks that involve spatial hierarchies.


<h2>Why Did CNNs Come into Existence?</h2>

CNNs were developed to address the challenges associated with processing and understanding images and videos. Traditional neural networks struggled with high-dimensional data due to the sheer number of parameters and computational complexity. CNNs introduce convolutional layers that reduce the number of parameters by sharing weights and exploiting the spatial structure of the data.


<h2>CNN ARCHITECTURE:</h2>

A typical CNN architecture consists of several types of layers:

1. Input Layer: The raw pixel values of the image.
2. Convolutional Layer: Applies a set of learnable filters (kernels) to the input. Each filter slides (convolves) over the input, producing a feature map that represents various aspects of the input (e.g., edges, textures).
3. Activation Function (ReLU): Applies a non-linear function to increase the network's capacity to learn complex patterns. The Rectified Linear Unit (ReLU) is the most common activation function.
4. Pooling Layer: Reduces the spatial dimensions of the feature maps, typically using max pooling or average pooling. This helps in reducing the computational load and controlling overfitting.
5. Fully Connected (Dense) Layer: Neurons in this layer are fully connected to all activations in the previous layer. This layer is typically used towards the end of the network for classification.
6. Output Layer: Produces the final predictions, usually via a softmax activation for classification tasks.


<h2>2D Convolutional Neural Network (2D CNN):</h2>

A 2D Convolutional Neural Network (2D CNN) is a type of neural network specifically designed to process two-dimensional data, typically images. In a 2D CNN, the convolutional layers perform 2D convolutions, which involve applying 2D filters (kernels) to the input data. This process extracts spatial features such as edges, textures, and patterns from the images. The architecture of 2D CNN is nothing different from the normal CNN. It also consists of Input layer, Convolutional layer, Activation layer, Pooling layer, Fully-connected layer and output layer.


<h2>Why to use CNN?</h2>

Using CNNs for SQL injection detection is justified due to their exceptional pattern recognition capabilities. CNNs can effectively capture local patterns and hierarchical features in SQL queries, identifying suspicious sequences indicative of injections. Their efficiency in processing large datasets makes them suitable for real-time applications, and their proven high accuracy, as evidenced by your 99% accuracy rate(1D CNN), demonstrates their effectiveness in distinguishing between normal and malicious queries. This makes CNNs a powerful tool for enhancing web application security against SQL injection attacks.


<h2>Simple Non-Numeric Example:</h2>
Consider a simple task: identifying whether an image contains a cat or a dog.

1. Input Layer: The image of a cat or dog.
2. Convolutional Layer: Filters detect features like edges, shapes, and textures.
3. Pooling Layer: Reduces the size of the feature maps while preserving important features.
4. Fully Connected Layer: Uses the extracted features to make a decision.
5. Output Layer: Outputs probabilities for each class (cat or dog).


<h2>Real World Use Case:</h2>

1. Image Classification: CNNs are extensively used in image classification tasks. For instance, they power the image recognition capabilities in Google Photos, where users can search for specific objects (like "dog" or "beach") in their photo library.

2. Medical Imaging: CNNs assist in analyzing medical images, such as X-rays, MRIs, and CT scans, to detect abnormalities like tumors or fractures.

3. Autonomous Vehicles: CNNs are used in self-driving cars to recognize traffic signs, pedestrians, and other vehicles.


<h3>Applications:</h3>

1. Object Detection: Identifying objects within an image and drawing bounding boxes around them.
2. Face Recognition: Identifying or verifying a person from an image or video frame.
3. Scene Understanding: Understanding and labeling various parts of an image, used in applications like satellite image analysis.
Natural Language Processing: Applied to text data by converting words into embeddings and treating sentences as sequences to capture local dependencies.


<h3>Different Types of CNN Architecture:</h3>
1. LeNet: One of the earliest CNN architectures, primarily used for handwritten digit recognition (MNIST dataset).
2. AlexNet: A deeper network that popularized CNNs by winning the ImageNet competition in 2012.
3. VGGNet: Known for its simplicity, using only 3x3 convolutional layers stacked on top of each other.
4. GoogLeNet (Inception): Introduced the inception module, which applies multiple convolutions with different filter sizes in parallel.
5. ResNet: Introduced residual connections to solve the vanishing gradient problem, allowing for much deeper networks.
6. DenseNet: Uses dense connections between layers to improve gradient flow and encourage feature reuse.







