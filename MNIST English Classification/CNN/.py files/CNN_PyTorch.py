# Imports
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import torch.nn.functional as F
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# We import the necessary libraries and modules for working with PyTorch, which is a popular deep learning framework.
# torch.nn provides classes and functions for building neural networks.
# torch.optim provides optimization algorithms for training neural networks.
# torchvision provides datasets and data transformations commonly used in computer vision tasks.
# torch.nn.functional provides activation functions and other utilities.
# torch.utils.data provides utilities for loading and batching data.

from keras.datasets import mnist  # Import MNIST dataset from Keras
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# We import additional libraries for data manipulation, visualization, and evaluation.
# Keras is a high-level neural networks API, and we use it to load the MNIST dataset.
# NumPy is a library for numerical computing in Python.
# Pandas is a data manipulation and analysis library.
# Seaborn and Matplotlib are data visualization libraries.

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# We import various functions and classes from scikit-learn for evaluation metrics, dimensionality reduction, and data visualization.

# Device Configuration
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)  # Print the device being used (CPU or GPU)

# We check if a CUDA-enabled GPU is available on the system. If so, we set the device to 'cuda' for GPU computations.
# Otherwise, we set the device to 'cpu' for CPU computations. This allows us to leverage GPU acceleration if available.

# Load the MNIST dataset
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# We load the MNIST dataset using the mnist.load_data() function from Keras.
# The dataset is split into training and test sets, and we unpack the data and labels into separate variables.

# Convert the dataset to NumPy array and normalize the data
X_train = X_train.reshape((-1, 1, 28, 28)).astype(np.float32) / 255.  # Reshape and normalize training images
X_test = X_test.reshape((-1, 1, 28, 28)).astype(np.float32) / 255.  # Reshape and normalize test images
y_train = y_train.astype(np.int64)  # Convert training labels to int64
y_test = y_test.astype(np.int64)  # Convert test labels to int64

# We preprocess the data by reshaping the images to a 4D tensor (batch_size, channels, height, width) and normalizing the pixel values to the range [0, 1].
# This is a common preprocessing step for image data, as neural networks typically expect input data in this format.
# We also convert the labels to int64 data type for compatibility with PyTorch.

# Convert the datasets to PyTorch tensors
x_train = torch.from_numpy(X_train)
y_train = torch.from_numpy(y_train)
x_test = torch.from_numpy(X_test)
y_test = torch.from_numpy(y_test)

x_train.shape, y_train.shape  # Print the shapes of the training data tensors

# We convert the NumPy arrays to PyTorch tensors using torch.from_numpy().
# PyTorch tensors are the primary data structures used for computations in PyTorch.
# We print the shapes of the training data tensors for verification.

# Visualize sample images from the training set
fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(12, 6))
axes = axes.flatten()

for i, ax in enumerate(axes):
    if i < 10:
        img = X_train[i].squeeze()  # Get the i-th training image
        ax.imshow(img, cmap='gray')  # Display the image
        ax.set_title(f'Label: {y_train[i]}')  # Set the title as the label
    else:
        ax.axis('off')  # Turn off axis for empty subplots

plt.tight_layout()
plt.show()

# We visualize a grid of 10 sample images from the training set, along with their corresponding labels.
# This step helps us understand the data we're working with and verify that the preprocessing steps were applied correctly.

# Calculate and visualize mean images per class
mean_images = []
for digit in range(10):
    mean_image = np.mean(X_train[y_train == digit], axis=0)  # Calculate mean image for each digit
    mean_images.append(mean_image)

# Plot mean images
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
axes = axes.flatten()

for i, (ax, mean_image) in enumerate(zip(axes, mean_images)):
    ax.imshow(mean_image.reshape(28, 28), cmap='gray')  # Display the mean image
    ax.set_title(f'Digit: {i}')  # Set the title as the digit
    ax.axis('off')

plt.tight_layout()
plt.show()

# We calculate and visualize the mean image for each digit class (0-9) in the training set.
# This step can provide insights into the characteristics of each digit class and help identify potential biases or patterns in the data.

# Analyze pixel intensity distributions per class
fig, axes = plt.subplots(2, 5, figsize=(15, 6))
axes = axes.flatten()

for i, digit in enumerate(range(10)):
    ax = axes[i]
    sns.distplot(X_train[y_train == digit].reshape(-1, 784).ravel(), ax=ax, kde=False)  # Plot pixel intensity distribution
    ax.set_title(f'Digit: {digit}')

plt.tight_layout()
plt.show()

# We analyze the pixel intensity distributions for each digit class using Seaborn's distplot function.
# This step can help identify potential overlaps or separability between classes based on pixel intensity patterns.

# Apply PCA
pca = PCA(n_components=2)  # Initialize PCA with 2 components
X_pca = pca.fit_transform(X_train.reshape(-1, 784))  # Fit and transform training data

# Visualize PCA components
plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y_train, cmap='viridis')  # Scatter plot of PCA components
plt.colorbar()
plt.title('MNIST Dataset Visualized with PCA')
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.show()

# We apply Principal Component Analysis (PCA) to the training data to reduce its dimensionality to 2 components.
# PCA is a dimensionality reduction technique that projects the data onto a lower-dimensional subspace while preserving as much variance as possible.
# We visualize the 2D projection of the training data using a scatter plot, where each point represents an image, and the color corresponds to the digit label.
# This step can help us understand the separability of the classes in a lower-dimensional space and identify potential clusters or overlaps.

# Apply t-SNE
tsne = TSNE(n_components=2, random_state=42)  # Initialize t-SNE with 2 components
X_tsne = tsne.fit_transform(X_train.reshape(-1, 784))  # Fit and transform training data

# Visualize t-SNE components
plt.figure(figsize=(8, 6))
plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y_train, cmap='viridis')  # Scatter plot of t-SNE components
plt.colorbar()
plt.title('MNIST Dataset Visualized with t-SNE')
plt.xlabel('First Component')
plt.ylabel('Second Component')
plt.show()

# We apply t-Distributed Stochastic Neighbor Embedding (t-SNE) to the training data, which is another dimensionality reduction technique.
# t-SNE is particularly useful for visualizing high-dimensional data in a low-dimensional space while preserving local structure.
# We visualize the 2D projection of the training data using a scatter plot, similar to the PCA visualization.
# Comparing the PCA and t-SNE visualizations can provide insights into the separability and clustering of the classes in different low-dimensional representations.

class CNN(nn.Module):
    """
    Convolutional Neural Network (CNN) model for MNIST digit classification.
    
    The model consists of the following layers:
    1. conv1: A 2D convolutional layer with 32 output channels, a kernel size of 3x3, and padding of 1.
    2. conv2: A 2D convolutional layer with 64 output channels, a kernel size of 3x3, and padding of 1.
    3. pool: A 2D max pooling layer with a kernel size of 2x2 and stride of 2.
    4. fc1: A fully connected layer with 128 output units.
    5. fc2: A fully connected layer with 10 output units (one for each digit class).
    """
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        """
        Forward pass of the CNN model.
        
        Args:
            x (torch.Tensor): Input tensor of shape (batch_size, 1, 28, 28).
            
        Returns:
            torch.Tensor: Output tensor of shape (batch_size, 10).
        """
        x = self.pool(nn.functional.relu(self.conv1(x)))  # Conv1 -> ReLU -> MaxPool
        x = self.pool(nn.functional.relu(self.conv2(x)))  # Conv2 -> ReLU -> MaxPool
        x = x.view(-1, 64 * 7 * 7)  # Flatten the tensor
        x = nn.functional.relu(self.fc1(x))  # Fully connected layer 1 -> ReLU
        x = self.fc2(x)  # Fully connected layer 2 (output)
        return x

# We define a Convolutional Neural Network (CNN) model for MNIST digit classification using PyTorch's nn.Module class.
# The model consists of two convolutional layers (conv1 and conv2) with ReLU activations and max pooling layers.
# The output of the convolutional layers is flattened and passed through two fully connected layers (fc1 and fc2).
# The final output is a tensor of shape (batch_size, 10), representing the predicted probabilities for each digit class.
# We provide detailed documentation for the model architecture and the forward pass function.

# Create TensorDatasets and DataLoaders
batch_size = 64
train_dataset = TensorDataset(x_train, y_train)  # Create TensorDataset for training data
test_dataset = TensorDataset(x_test, y_test)  # Create TensorDataset for test data
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)  # Create DataLoader for training data
test_loader = DataLoader(test_dataset, batch_size=batch_size)  # Create DataLoader for test data

# We create PyTorch TensorDataset objects for the training and test data, which combine the input tensors (images) and target tensors (labels).
# We then create DataLoader objects for efficient batching and shuffling of the data during training and evaluation.
# The batch_size parameter determines the number of samples in each batch, and shuffle=True ensures that the data is shuffled during training.

# Instantiate the model
model = CNN().to(device)  # Create an instance of the CNN model and move it to the specified device

# We create an instance of the CNN model and move it to the specified device (CPU or GPU) using the .to() method.

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()  # Define the loss function (cross-entropy loss)
optimizer = optim.Adam(model.parameters())  # Define the optimizer (Adam)

# We define the loss function and optimizer for training the model.
# The cross-entropy loss is a common choice for multi-class classification problems like MNIST digit classification.
# The Adam optimizer is a popular choice for its adaptive learning rate and momentum properties.

# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    running_loss = 0.0
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data[0].to(device), data[1].to(device)  # Move input data and labels to the specified device

        optimizer.zero_grad()  # Zero out the gradients from the previous iteration
        outputs = model(inputs)  # Compute the model's output for the current batch
        loss = criterion(outputs, labels)  # Calculate the loss between the output and the true labels
        loss.backward()  # Backpropagate the loss to compute the gradients
        optimizer.step()  # Update the model's parameters using the optimizer

        running_loss += loss.item()  # Accumulate the loss for the current batch
        if i % 200 == 199:  # Print the running loss every 200 iterations
            print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 200:.3f}')
            running_loss = 0.0

print('Finished Training')

# We define the training loop for the CNN model.
# The loop iterates over the specified number of epochs (num_epochs).
# In each epoch, the model iterates over the training data in batches using the train_loader.
# For each batch, the following steps are performed:
#   1. Move the input data and labels to the specified device (CPU or GPU).
#   2. Zero out the gradients from the previous iteration.
#   3. Compute the model's output for the current batch.
#   4. Calculate the loss between the output and the true labels using the cross-entropy loss function.
#   5. Backpropagate the loss to compute the gradients.
#   6. Update the model's parameters using the Adam optimizer.
# The running loss is printed every 200 iterations for monitoring purposes.

# Accuracy
correct = 0
total = 0
y_true = []
y_pred = []

with torch.no_grad():  # Disable gradient computation for evaluation
    for data in test_loader:
        images, labels = data
        images, labels = images.to(device), labels.to(device)  # Move input data and labels to the specified device
        outputs = model(images)  # Compute the model's output for the current batch
        _, predicted = torch.max(outputs.data, 1)  # Get the predicted labels
        total += labels.size(0)  # Update the total number of samples
        correct += (predicted == labels).sum().item()  # Update the number of correct predictions
        y_true.extend(labels.cpu().numpy())  # Append true labels to y_true
        y_pred.extend(predicted.cpu().numpy())  # Append predicted labels to y_pred

if total != 0:
    accuracy = 100 * correct / total
    print(f'Accuracy on test set: {accuracy:.2f}%')  # Print the accuracy on the test set
else:
    print('No data to compute accuracy.')

# We evaluate the trained CNN model on the test set.
# We disable gradient computation using torch.no_grad() to improve performance during evaluation.
# The model iterates over the test data in batches using the test_loader.
# For each batch, the following steps are performed:
#   1. Move the input data and labels to the specified device (CPU or GPU).
#   2. Compute the model's output for the current batch.
#   3. Get the predicted labels by taking the maximum value along the output dimension.
#   4. Update the total number of samples and the number of correct predictions.
#   5. Append the true labels and predicted labels to separate lists (y_true and y_pred) for further evaluation.
# After iterating over all batches, we calculate the overall accuracy on the test set as the percentage of correct predictions.
# If there is no data to compute accuracy (total == 0), we print a message indicating that.

# Precision, Recall, F1-Score
print('Classification Report:')
print(classification_report(y_true, y_pred))  # Print the classification report

# We use scikit-learn's classification_report function to generate a detailed report on the model's performance.
# The classification report provides metrics such as precision, recall, and F1-score for each class, as well as macro-averaged and weighted averages.
# These metrics are useful for evaluating the model's performance, especially in cases of class imbalance or uneven misclassification costs.

# Confusion Matrix
conf_matrix = confusion_matrix(y_true, y_pred)  # Compute the confusion matrix
df_cm = pd.DataFrame(conf_matrix, index=[i for i in range(10)], columns=[i for i in range(10)])  # Convert to DataFrame
plt.figure(figsize=(10, 7))
sns.heatmap(df_cm, annot=True)  # Plot the confusion matrix as a heatmap
plt.title('Confusion Matrix')
plt.xlabel('Predicted Class')
plt.ylabel('True Class')
plt.show()

# We compute the confusion matrix using scikit-learn's confusion_matrix function.
# The confusion matrix is a table that summarizes the model's predictions versus the true labels.
# The rows represent the true labels, and the columns represent the predicted labels.
# The diagonal elements represent the number of correct predictions for each class, while the off-diagonal elements represent the misclassifications.
# We convert the confusion matrix to a Pandas DataFrame for better visualization.
# We then use Seaborn's heatmap function to plot the confusion matrix as a heatmap, with annotations showing the values in each cell.
# The heatmap provides a visual representation of the model's performance, highlighting the classes that are most often confused with each other.
