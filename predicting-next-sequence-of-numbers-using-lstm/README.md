# Predicting Next Sequence of Numbers using LSTM

This repository contains a Python implementation of a Long Short-Term Memory (LSTM) network to predict the next sequence of numbers in a given sequence. The model is trained on a dataset of numerical sequences and uses the LSTM architecture to learn patterns and relationships in the data.

## Model Architecture

The LSTM model consists of the following layers:

- Input layer: 1 neuron, representing the input sequence.
- LSTM layer: 50 neurons, with a dropout rate of 0.2
- Dense layer: 1 neuron, with a linear activation function

## Working of Predicting Next Sequence of Numbers using LSTM

**Step 1: Data Preparation**

- The dataset consists of numerical sequences of varying lengths. Each sequence is normalized to have values between 0 and 1.

**Step 2: Model Definition**

- The LSTM model is defined using the Keras API in TensorFlow. The model consists of an input layer, an LSTM layer, and a dense layer. The LSTM layer has 50 neurons and a dropout rate of 0.2 to prevent overfitting.

**Step 3: Model Compilation**

- The model is compiled with the Adam optimizer and mean squared error as the loss function.

**Step 4: Training And Prediction**

- The model is trained on the dataset using a batch size of 32 and 100 epochs. Once the model is trained, it is used to predict the next sequence of numbers. The input sequence is fed into the model, and the output is the predicted next sequence of numbers.

## Output

- The predicted next sequence of numbers using the trained LSTM model is:

[0.41865336894989014, 0.42837363481521606, 0.4390440583229065, 0.4428862929344177, 0.44844937324523926, 0.4514892101287842, 0.4522506594657898, 0.45116126537323, 0.45161277055740356, 0.45571017265319824, 0.4642440676689148, 0.4770122170448303]