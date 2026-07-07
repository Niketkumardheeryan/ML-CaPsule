## MNIST Digit Classification with PyTorch

This repository contains a PyTorch implementation for
training a Convolutional Neural Network (CNN) to classify handwritten
digits from the MNIST dataset. The code includes data preprocessing,
model definition, training loop, and evaluation metrics.

## Introduction

The MNIST dataset is a widely used benchmark dataset in
the field of computer vision and machine learning. It consists of 60,000
 training images and 10,000 test images of handwritten digits (0-9). The
 goal of this project is to train a CNN model to accurately classify
these digits.

## Dataset

The MNIST dataset is loaded using the `keras.datasets.mnist.load_data()`
 function from the Keras library. The dataset is split into training and
 test sets, and the data is preprocessed by reshaping the images to a 4D
 tensor (batch_size, channels, height, width) and normalizing the pixel
values to the range **.**

## Dependencies

The following Python libraries are required to run the code:

* PyTorch
* NumPy
* Pandas
* Seaborn
* Matplotlib
* scikit-learn

You can install these dependencies using pip:

<pre class="not-prose w-full overflow-hidden rounded font-mono text-sm font-extralight" node="[object Object]"><div class="codeWrapper text-textMainDark selection:!text-superDark selection:bg-superDuper/10 relative" node="[object Object]"><div class="absolute"></div><div class="sc-gEvEer bMfiHw"><span><code>pip install torch torchvision numpy pandas seaborn matplotlib scikit-learn
</code></span></div></div></pre>

## Usage

1. Clone the repository:

<pre class="not-prose w-full overflow-hidden rounded font-mono text-sm font-extralight" node="[object Object]"><div class="codeWrapper text-textMainDark selection:!text-superDark selection:bg-superDuper/10 relative" node="[object Object]"><div class="absolute"></div><div class="sc-gEvEer bMfiHw"><span><code>git https://github.com/Niketkumardheeryan/ML-CaPsule.git
cd MNIST English Classification
cd CNN
cd .py files
</code></span></div></div></pre>

2. Run the script:

<pre class="not-prose w-full overflow-hidden rounded font-mono text-sm font-extralight" node="[object Object]"><div class="codeWrapper text-textMainDark selection:!text-superDark selection:bg-superDuper/10 relative" node="[object Object]"><div class="absolute"></div><div class="sc-gEvEer bMfiHw"><span><code>CNN_PyTorch.py
</code></span></div></div></pre>

This will train the CNN model on the MNIST dataset and evaluate its performance on the test set.

## Code Structure

The code is organized as follows:

* `imports`: Import necessary libraries and modules.
* `device configuration`: Check if a CUDA-enabled GPU is available and set the device accordingly.
* `load and preprocess data`: Load the MNIST dataset, preprocess the data, and convert it to PyTorch tensors.
* `data visualization`: Visualize sample images from the training set and analyze pixel intensity distributions.
* `dimensionality reduction`:
  Apply Principal Component Analysis (PCA) and t-Distributed Stochastic
  Neighbor Embedding (t-SNE) for visualizing the data in lower dimensions.
* `model definition`: Define the CNN model architecture using PyTorch's `nn.Module`.
* `create data loaders`: Create PyTorch `TensorDataset` and `DataLoader` objects for efficient data loading during training and evaluation.
* `instantiate model`: Create an instance of the CNN model and move it to the specified device.
* `define loss and optimizer`: Define the loss function (cross-entropy loss) and optimizer (Adam) for training.
* `training loop`: Train the CNN model for a specified number of epochs, updating the model parameters based on the computed gradients.
* `evaluation`: Evaluate the trained model on the test set, computing accuracy, classification report, and confusion matrix.
* `visualization`: Visualize the confusion matrix as a heatmap.

## Model Architecture

The CNN model consists of the following layers:

1. `conv1`: A 2D convolutional layer with 32 output channels, a kernel size of 3x3, and padding of 1.
2. `conv2`: A 2D convolutional layer with 64 output channels, a kernel size of 3x3, and padding of 1.
3. `pool`: A 2D max pooling layer with a kernel size of 2x2 and stride of 2.
4. `fc1`: A fully connected layer with 128 output units.
5. `fc2`: A fully connected layer with 10 output units (one for each digit class).

The model uses ReLU activations and max pooling layers to introduce non-linearity and reduce spatial dimensions.

## Training

The model is trained using the Adam optimizer and
cross-entropy loss function. The training loop iterates over the
specified number of epochs, and in each epoch, the model iterates over
the training data in batches. For each batch, the following steps are
performed:

1. Move the input data and labels to the specified device (CPU or GPU).
2. Zero out the gradients from the previous iteration.
3. Compute the model's output for the current batch.
4. Calculate the loss between the output and the true labels using the cross-entropy loss function.
5. Backpropagate the loss to compute the gradients.
6. Update the model's parameters using the Adam optimizer.

The running loss is printed every 200 iterations for monitoring purposes.

## Evaluation

After training, the model is evaluated on the test set. The evaluation process includes:

1. Disabling gradient computation for evaluation.
2. Iterating over the test data in batches.
3. Computing the model's output for each batch.
4. Getting the predicted labels by taking the maximum value along the output dimension.
5. Updating the total number of samples and the number of correct predictions.
6. Appending the true labels and predicted labels to separate lists for further evaluation.

The overall accuracy on the test set is calculated as the
 percentage of correct predictions. Additionally, a classification
report is generated, providing metrics such as precision, recall, and
F1-score for each class, as well as macro-averaged and weighted
averages.
The confusion matrix is also computed and visualized as a
 heatmap, providing a visual representation of the model's performance
and highlighting the classes that are most often confused with each
other.

## Results

The trained model achieves an accuracy of 99.33% on the
MNIST test set. The classification report and confusion matrix are
displayed in the console output.


## Author/Contributors

[Saswat Susmoy](https://github.com/Saswatsusmoy)
