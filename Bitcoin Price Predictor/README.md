Link to [youtube video](https://youtu.be/n32ETDdp6kM)
# Bitcoin-Price-Prediction-Using-RNN-LSTM
This notebook demonstrates the prediction of the bitcoin price by the neural network model. We are using long short term memory (LSTM)

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes

### Prerequisites
you need to install all the necessary libraries n order to run the project
`sklearn`
`tensorflow`
`pandas`
`matplotlib`

### Installing
```
pip install sklearn
pip install tensorflow
pip install pandas
pip install matplotlib
```

## --------------------------------------------------------------------------
### we will be going through a four step process to predict cryptocurrency prices:
1. Getting real-time crptocurrency data(bitcoin).
2. Prepare data for training and testing.
3. Predict the price of crptocurrency using LSTM neural network (deep learning).
4. Visualize the prediction results.

### 1. Getting real-time crptocurrency data(bitcoin)
You can collect the current data for Bitcoin from [Yahoo Finance](https://in.finance.yahoo.com/quote/BTC-USD/history?p=BTC-USD)
![Data from yahoo Finanace](img/2020-05-30_11-28-54.png)

### 2. Prepare data for training and testing.
You can preprocess the data before dividing it into traning and testing
```
data_training = data[data['Date']< '2020-01-01'].copy()
data_training
```
![Training Data](img/2020-05-30_11-29-47.png)
```
data_test = data[data['Date']> '2020-01-01'].copy()
data_test
```
![Testing data](img/2020-05-30_11-30-09.png)
### 3. Predict the price of crptocurrency using LSTM neural network (deep learning)
```
regressor = Sequential()
regressor.add(LSTM(units = 60, activation = 'relu', return_sequences = True, input_shape = (X_train.shape[1], 5)))
regressor.add(Dropout(0.2))
regressor.compile(optimizer = 'adam', loss='mean_absolute_error')
regressor.fit(X_train, Y_train, epochs = 20, batch_size =50)
```
```
Y_pred = regressor.predict(X_test)
Y_pred, Y_test
```

### 4. Visualize the prediction results.
```
plt.figure(figsize=(14,5))
plt.plot(Y_test, color = 'red', label = 'Real Bitcoin Price')
plt.plot(Y_pred, color = 'green', label = 'Predicted Bitcoin Price')
plt.title('Bitcoin Price Prediction using RNN-LSTM')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()
```
![Final Graph](img/2020-05-30_11-33-41.png)

