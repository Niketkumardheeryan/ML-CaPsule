# C++ Neural Network for MNIST 🧠🤖

This is a simple 3-layer (784-128-10) feedforward neural network built from scratch in C++ to recognize handwritten digits. It is trained on the MNIST dataset and can be used to test against the MNIST test set or predict custom 28x28 images.

The project is split into two main parts:

A training program 🏋️‍♂️ that learns from the 60,000 MNIST training images and saves the resulting model.

Two testing programs 🧪 that load the saved model to either:

Calculate its accuracy against the 10,000 MNIST test images.

Predict a single custom-drawn digit image.

## Project Structure 📂

<img width="1632" height="1174" alt="image" src="https://github.com/user-attachments/assets/97facc74-e742-42bc-9b37-611deb83cd7c" />

## Prerequisites 🛠️

A C++ compiler (e.g., g++ on Linux/macOS or MinGW on Windows).

The four MNIST dataset files, which must be placed inside the data/ folder.

## How to Use 🚀

The project must be compiled in two stages. First, you train the model. Second, you test it.

## Step 1: Train the Model 🏋️‍♂️

This executable will read the 60,000 images from the data/ folder, train the network for 3 epochs, and save the resulting mnist_model.dat file in the project's root directory.

### 1. Navigate to the training directory
cd training

### 2. Compile the training program
g++ main.cpp NeuralNetwork.cpp -o train

### 3. Run the compiled program to start training
./train


After this finishes, you will see a new mnist_model.dat file in the NeuralNetwork2/ root folder.

## Step 2: Test the Model 🧪

You can now use the mnist_model.dat file to make predictions. You have two options.
<br>

### Option A: Test Accuracy on MNIST Test Set 📊

This will load the 10,000 test images and print the final accuracy percentage of the model.

### 1. Navigate to the testing directory
cd testing

### 2. Compile the accuracy test program
g++ accuracy.cpp NeuralNetwork.cpp -o test_accuracy

### 3. Run the program
./test_accuracy


Example Output:<br>
--- Test Complete --- <br>
Correct Predictions: 9523/10000<br>
Accuracy: 95.23%
<br>

### Option B: Test with a Custom Image ✍️
This will load a single 28x28 image, predict the digit, and show the confidence scores.

Note: Before compiling, open testing/custom_test.cpp and change the customImagePath variable to point to your desired test image inside the number_images/ folder.

// Inside testing/custom_test.cpp
string customImagePath = "../number_images/num7.png"; // <-- CHANGE THIS
<br>

## Image Requirements:

Size: Exactly 28x28 pixels.

Format: Grayscale .png (or .jpg, .bmp).

Style: The model was trained on white digits on a black background. The code will automatically detect if your image is black-on-white and invert it for you.

Compile and Run:

### 1. Navigate to the testing directory
cd testing

### 2. Compile the custom test program
g++ custom_test.cpp NeuralNetwork.cpp -o test_custom

### 3. Run the program
./test_custom

Example Output: <br>
--- Prediction ---<br>
The model predicts the digit is: 7


This project uses the public domain stb_image.h library by Sean Barrett for loading custom images.
