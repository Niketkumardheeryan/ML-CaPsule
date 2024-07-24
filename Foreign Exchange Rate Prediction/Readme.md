# Foreign Exchange Rate Prediction

## Overview

This project demonstrates the prediction of foreign exchange (Forex) rates using machine learning and deep learning algorithms. The system employs models such as Long Short-Term Memory (LSTM) networks and Random Forest to analyze historical Forex data and forecast future exchange rates. The project includes data preprocessing, feature engineering, model training, validation, and deployment functionalities.

## Use Case

In real-world applications, accurate Forex rate predictions are crucial for:

- **Financial Institutions:** Managing foreign currency reserves and optimizing transaction costs.
- **Traders:** Making informed trading decisions to reduce risks and maximize profits.
- **Businesses:** Planning and hedging against currency risks to ensure stable financial operations.

By integrating this feature, users can leverage advanced predictive analytics to enhance decision-making and strategic planning in the volatile Forex market.

## Setup Instructions

### Prerequisites

Before running the project, ensure you have the following libraries installed:

- `keras`
- `tensorflow`
- `numpy`
- `sklearn`
- `matplotlib`
- `pandas`

### Installing Dependencies

To install the required libraries, use the following commands:

```bash
pip install keras
pip install tensorflow
pip install numpy
pip install scikit-learn
pip install matplotlib
pip install pandas
```


## Usage

1. **Upload Data:**
   - Use the upload widget to load your dataset into the project.

2. **Preprocessing:**
   - The dataset is cleaned and interpolated to handle missing values.
   - Exchange rates are scaled using Min-Max normalization.

3. **Data Preparation:**
   - The dataset is split into training and test sets.
   - Features are shaped for the LSTM model.

4. **Model Training:**
   - An LSTM model is defined and compiled.
   - The model is trained using the training dataset.

5. **Prediction:**
   - Predictions are made using the trained model.
   - The results are inverse-transformed to the original scale.

6. **Visualization:**
   - The predicted and actual exchange rates are visualized using matplotlib.

7. **Evaluation:**
   - The model's performance is assessed using metrics like Mean Squared Error (MSE).

## Conclusion

The Foreign Exchange Rate Prediction project effectively demonstrates the application of machine learning and deep learning techniques to forecast exchange rates. By leveraging the LSTM model and comprehensive preprocessing steps, the system provides valuable insights into future currency trends. 

The project's results highlight the potential of predictive analytics in the Forex market, offering users the ability to make more informed decisions. Accurate predictions can significantly benefit financial institutions, traders, and businesses by mitigating risks and optimizing financial strategies.

Thank you for exploring this project. We hope it serves as a useful tool and inspires further developments in Forex rate prediction and financial analytics.
