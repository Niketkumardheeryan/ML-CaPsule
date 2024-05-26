# BIDIRECTIONAL LSTM

Bi-directional long-short term memory(bi-LSTM) is the type of RNN which makes the input sequence information flow in both directions forwards as well as backwards. It helps us preserve the future information as well as the past.

## Use Cases of Bi-Directional LSTM

Bidirectional LSTM is used in cases where flow of information from backward and forward layers makes execution of sequence-to-sequence tasks easier.Some examples are as follows:

- Text classification
- Speech Recognition
- Forecasting Models
- Natural Language Processing
- Dependency Parsing

## Working of Bi-Directional LSTM

- Bi- directional LSTM runs the inputs in two ways, one from past to future and one from future to past.
- This variation in approach from unidirectional LSTM helps to preserve information from the future as well as past.
- This architecture allows the neural networks to have both backward and forward information about the sequence at every time step.
- Forward Pass:
  - Forward states (from t = 1 to N) and backward states (from t = N to 1) are passed.
  - Output neuron values are passed (from t = 1 to N).
- Backward Pass:
  - Output neuron values are passed (t = N to 1).
  - Forward states (from t = N to 1) and backward states (from t = 1 to N) are passed.

Both the forward and backward passes together train a Bidirectional LSTM .

## Advantage of Bi-Directional LSTM

Bi-LSTMs effectively increase the amount of information available to the network, improving the context available to the model.

## When to avoid Bi-Directional LSTM

- One limitation with Bidirectional LSTM is that the entire sequence must be available before we can make predictions.
- In applications such as real-time speech recognition, the entire utterance may not be available before predictions and Bi-Directional LSTMs should be avoided in such cases.
- Stacking many layers of Bi-directional LSTM creates the vanishing gradient problem.So, it should be avoided in case of Deep Stacked layers of LSTM as well.

## Example Use Case of Bi-Directional LSTM

- This notebook demonstrates the prediction of the temperature for the next 30 days by the neural network model.
- We are using Bidirectional LSTM Model in RNN.

## Setup instructions

### Prerequisites

you need to install all the necessary libraries in order to run the project
`pandas`
`sklearn`
`numpy`
`tensorflow`
`keras`

### Installing

```
pip install pandas
pip install tensorflow
pip install numpy
pip install sklearn
pip install keras
```

#### DATASET

[](./Models/my_best_model.epoch05-loss0.00.hdf5)

#### MODEL

[](./Models/testset.csv)

The model has a very high accuracy of 99.99928 % .

## Author(s)

[Shreya Ghosh](https://github.com/shreay024)
