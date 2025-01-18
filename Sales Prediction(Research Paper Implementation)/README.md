# Sales Forecasting with LSTM and Stacking Models

This repository contains a project for sales forecasting using various machine learning models, including LSTM (Long Short-Term Memory) and stacking models. The project is implemented in a Jupyter Notebook and uses a dataset of sales data.

## Project Structure
.gitignore<br>
Final_sales.ipynb<br>
my_lstm_model.h5<br>
train.csv<br>


### 🔗 Dataset
The dataset used for this project can be downloaded from [https://drive.google.com/file/d/1lpHAejc8c2elvbxhwMlxzNKxllos1_in/view?usp=sharing].

The Dataset contains the following columns:
- `date`: Date of the sales record
- `store`: Store ID
- `item`: Item ID
- `sales`: Number of sales

### 🤖 Model File
The pre-trained LSTM model file can be downloaded from [https://drive.google.com/file/d/18WSV-HzorNzTj90sbmwPLgny93Ptu3jJ/view?usp=sharing].

## Models Used

1. **Linear Regression**
2. **Decision Tree Regressor**
3. **Random Forest Regressor**
4. **Gradient Boosting Regressor**
5. **LSTM (Long Short-Term Memory)**
6. **Stacking Models**

## Evaluation Metrics

The models are evaluated using the following metrics:
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score
- Mean Absolute Error (MAE)
- Percentage Error
- Accuracy

## Results

### Without K-Fold Cross-Validation

| Model                | MSE   | RMSE  | R²   | MAE  | Percentage Error | Accuracy |
|----------------------|-------|-------|------|------|------------------|----------|
| Linear Regression    | 91.06 | 9.54  | 0.89 | 7.27 | 17.05%           | 82.95%   |
| Decision Tree        | 147.82| 12.16 | 0.82 | 9.29 | 21.81%           | 78.19%   |
| Random Forest        | 77.09 | 8.78  | 0.91 | 6.72 | 16.05%           | 83.95%   |
| Gradient Boosting    | 78.71 | 8.87  | 0.91 | 6.80 | 16.15%           | 83.85%   |
| First Stacking Model | 85.94 | 9.27  | 0.90 | 7.08 | 16.78%           | 83.22%   |
| Second Stacking Model| 75.64 | 8.70  | 0.91 | 6.66 | 15.81%           | 84.19%   |

### With K-Fold Cross-Validation

| Model                | MSE   | RMSE  | R²   | MAE  | Percentage Error | Accuracy |
|----------------------|-------|-------|------|------|------------------|----------|
| Linear Regression    | 90.97 | 9.54  | 0.89 | 7.26 | 17.01%           | 82.99%   |
| Decision Tree        | 149.57| 12.23 | 0.82 | 9.35 | 21.96%           | 78.04%   |
| Random Forest        | 78.53 | 8.86  | 0.91 | 6.79 | 16.11%           | 83.89%   |
| Gradient Boosting    | 78.71 | 8.87  | 0.91 | 6.80 | 16.15%           | 83.85%   |

### LSTM Model

| Metric               | Value |
|----------------------|-------|
| Mean Squared Error   | 55.96 |
| Root Mean Squared Error | 7.48 |
| R² Score             | 0.70  |
| Mean Absolute Error  | 5.78  |
| Percentage Error     | 35.95%|
| Accuracy             | 64.05%|

## Usage

1. Clone the repository:
   ```sh
   git clone https://github.com/akshat12-20/Sales_Prediction.git

2. Navigate to the project directory:
    cd sales-forecasting

3. Install the required packages:
    pip install -r requirements.txt

4. Download the model file and dataset files from the links given above.

5. Open the Jupyter Notebook:
    jupyter notebook Final_sales.ipynb

## License
This project is licensed under the MIT License.