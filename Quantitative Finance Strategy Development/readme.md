# Quantitative Finance Strategy Development

## 🎯 Goal
The main goal of this project is to develop and compare different deep learning models for predicting stock prices. This project utilizes historical stock price data and technical indicators to forecast future stock prices using LSTM and GRU models.

## 📁 Dataset
The dataset used for this project is `quantitative_finance_data.csv`, which contains historical stock price data and various technical indicators.

## 📜 Description
This project involves the implementation of LSTM and GRU models for stock price prediction. The models are trained to recognize patterns in historical stock price data and technical indicators, and their performance is evaluated and compared.

## 🧮 What I Had Done!
1. Loaded and preprocessed the dataset.
2. Performed EDA to understand the distribution and characteristics of the data.
3. Implemented two different models: LSTM and GRU.
4. Trained and evaluated each model.
5. Compared the models based on their mean squared error (MSE) and mean absolute error (MAE) metrics.

## 🚀 Models Implemented
- **Long Short-Term Memory (LSTM):** A type of recurrent neural network (RNN) that is well-suited for time series forecasting due to its ability to capture long-term dependencies.
- **Gated Recurrent Unit (GRU):** Another type of RNN that is similar to LSTM but has a simpler architecture, making it computationally efficient.

## 📚 Libraries Needed
- numpy
- pandas
- matplotlib
- scikit-learn
- tensorflow

## 📊 Exploratory Data Analysis (EDA) Results
### Dataset Information
- Dataset shape: (1000, 8)
- Missing values: None

### Visualizations
- Distribution of Technical Indicators
- Correlation Heatmap
- Stock Price Time Series Plot

## 📈 Performance of the Models Based on the Metrics
- **LSTM:**
  - MSE: <0.10148382186889648>
  - MAE: < 0.27419179677963257>

- **GRU:**
  - MSE: <0.09099733829498291>
  - MAE: <0.2616104483604431>

## 📢 Conclusion
In this project, we explored the use of LSTM and GRU models for stock price prediction. Both models showed promising results, with the GRU model performing slightly better in terms of MSE and MAE metrics. These models can be further tuned and optimized for better performance.


