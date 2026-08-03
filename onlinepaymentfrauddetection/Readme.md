# Online Payment Fraud Detection

## Overview

This project focuses on identifying online payment fraud using machine learning techniques. We have utilized a dataset from Kaggle that contains various transaction details to build and deploy a machine learning model capable of classifying transactions as fraudulent or non-fraudulent.

## Dataset

The dataset contains the following columns:

- `step`: Represents a unit of time where 1 step equals 1 hour.
- `type`: Type of online transaction.
- `amount`: The amount of the transaction.
- `oldbalanceOrg`: Balance of the origin account before the transaction.
- `newbalanceOrig`: Balance of the origin account after the transaction.
- `oldbalanceDest`: Initial balance of the recipient before the transaction.
- `newbalanceDest`: The new balance of the recipient after the transaction.
- `isFraud`: Indicator of fraud (1 if the transaction is fraudulent, 0 otherwise).

## Preprocessing

1. **Dropping unnecessary columns**:
   ```python
   data.drop("nameOrig", inplace=True, axis=1)
   data.drop("nameDest", inplace=True, axis=1)
   ```

2. **Mapping transaction types**:
   ```python
   data["type"] = data["type"].map({"CASH_OUT" : 1, "PAYMENT" : 2, "CASH_IN" : 3, "TRANSFER" : 4, "DEBIT" : 5})
   ```

3. **Checking for null values**:
   ```python
   print(data.isnull().sum())  # Confirming no null values are present
   ```

## Data Visualization

We visualized the distribution of transaction types using a pie chart:

```python
import plotly.express as px

type = data["type"].value_counts()
transactions = type.index
quantity = type.values

figure = px.pie(data, values = quantity, names = transactions, hole = 0.5, title = "Distribution of Transaction Type")
figure.show()
```

## Correlation Analysis

We analyzed the correlation between the features and the target variable (`isFraud`):

```python
correlation = data.corr()
print(correlation["isFraud"].sort_values(ascending = False))
```

## Splitting the Data

The data was split into training and testing sets:

```python
from sklearn.model_selection import train_test_split

x = np.array(data[["type", "amount", "oldbalanceOrg", "newbalanceOrig"]])
y = np.array(data[["isFraud"]])

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size = 0.10, random_state = 42)
```

## Model Training

We trained a Decision Tree classifier on the dataset:

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier()
model.fit(xtrain, ytrain)
print(model.score(xtest, ytest))
```

## Deployment

We deployed the model as a web application using Gradio:

```python
!pip install gradio
import gradio as gr

def predict_fraud(transaction_type, amount, oldbalanceOrg, newbalanceOrig):
    features = np.array([[transaction_type, amount, oldbalanceOrg, newbalanceOrig]])
    output = model.predict(features)
    return "Fraud" if output == 1 else "No Fraud"

inputs = [
    gr.Number(label="Transaction Type"),
    gr.Number(label="Amount"),
    gr.Number(label="Old Balance Org"),
    gr.Number(label="New Balance Orig")
]

output = gr.Textbox(label="Fraud Prediction")

gr.Interface(fn=predict_fraud, inputs=inputs, outputs=output, title="Online Fraud Detection").launch(share=True)
```

## Conclusion

This project successfully implements a machine learning model to detect fraudulent transactions based on transaction type, amount, and account balances before and after the transaction. The model is deployed using Gradio for easy interaction and prediction of fraud in real-time.

## Future Work

- **Improving Model Performance**: Experimenting with more complex algorithms like Random Forest, Gradient Boosting, or Neural Networks.
- **Feature Engineering**: Creating additional features that could improve model accuracy.
- **Handling Imbalanced Data**: Implementing techniques to handle imbalanced data to improve fraud detection.
- **Real-time Data Processing**: Integrating the model into a real-time transaction processing system for live fraud detection.

## Requirements

- Python 3.x
- Pandas
- NumPy
- Scikit-learn
- Plotly
- Gradio

## How to Run

1. **Install the required packages**:
   ```bash
   pip install pandas numpy scikit-learn plotly gradio
   ```

2. **Run the script**:
   ```bash
   python script_name.py
   ```

3. **Interact with the web application**:
   - The Gradio interface will launch and provide a URL for accessing the web app.