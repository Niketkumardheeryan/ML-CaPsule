# Online Shoppers Intention Prediction

## Overview
This project predicts whether an online shopping session will end in a purchase. It combines deep learning models with a Flask web application so the trained model can be used through a browser for prediction and simple analytics.

## Problem statement
Online stores receive a large number of visits, but only some sessions convert into purchases. The goal of this project is to predict purchase intent from session behavior so businesses can better understand user activity and improve targeting, remarketing, and conversion strategies.

## Dataset
This project uses the Online Shoppers Purchasing Intention Dataset.

- Dataset name: Online Shoppers Purchasing Intention Dataset
- Source: Kaggle
- Dataset link: [Online Shoppers Intention](https://www.kaggle.com/datasets/henrysue/online-shoppers-intention)
- Records: 12,330 sessions
- Features: 18 columns including the target variable
- Target variable: `Revenue`

The dataset contains session-level e-commerce behavior such as page visits, time spent on pages, bounce rate, exit rate, page value, traffic source, visitor type, browser, operating system, and weekend activity.

### Target meaning
- `True` means the session resulted in a purchase.
- `False` means the user left without making a purchase.

## Why this dataset fits the problem
This dataset works well for purchase prediction because it contains direct behavior signals that are closely related to buying intent. Features such as product-related page activity, exit rate, bounce rate, and page value make it a good fit for binary classification.

## Data preprocessing
The project follows these preprocessing steps:

- Remove duplicate records where needed.
- Handle missing values for numeric and categorical data.
- Encode categorical features using label encoders.
- Scale numeric features using `StandardScaler`.
- Split the dataset into training and testing sets with stratification.

## Project workflow
1. Load the dataset from the `Dataset` folder.
2. Clean and preprocess the data.
3. Encode categorical columns.
4. Scale the features.
5. Train multiple deep learning models.
6. Evaluate each model using classification metrics.
7. Save trained models and preprocessing objects.
8. Build a Flask web app for prediction and dashboard views.
9. Add production-oriented security settings to the app.

## Models implemented

### MLP
Used as a baseline neural network model for tabular classification.

### Deep Neural Network
A deeper feedforward model that gave the best overall performance and is used in the web application for inference.

### LSTM
Used to test sequence-style learning on the prepared session data.

### GRU
Used as a lighter recurrent alternative to LSTM.

## Model assets
The `Model` folder contains everything required for training review and inference.

### Files included
- Jupyter Notebook implementation
- Trained deep learning models
- Feature scaler
- Label encoders
- Target encoder

These files are kept because the Flask application depends on them for preprocessing and prediction.

## Performance summary

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| MLP | 0.8895 | 0.7248 | 0.5876 | 0.6481 | 0.8672 |
| Deep Neural Network | 0.8965 | 0.7658 | 0.6521 | 0.7037 | 0.8952 |
| LSTM | 0.8931 | 0.7412 | 0.6124 | 0.6708 | 0.8823 |
| GRU | 0.8947 | 0.7521 | 0.6287 | 0.6849 | 0.8891 |

The Deep Neural Network performs best overall, especially on F1 score and ROC-AUC, so it is used as the main model in the web app.

## Visualizations
The visual outputs are consolidated into a single file:

- `Images/model_visualizations.pdf`

This PDF includes:
1. Training history
2. Model comparison
3. Confusion matrices
4. ROC curves
5. Feature importance
6. Data distribution

### What the visualizations show
- Training history shows how the models learned over epochs.
- Model comparison shows how all four models perform across metrics.
- Confusion matrices show correct and incorrect predictions.
- ROC curves show class separation performance.
- Feature importance highlights the most influential input signals.
- Data distribution gives a quick view of feature spread and target balance.

### Visualization Details

#### 1. Training History
Shows the training and validation accuracy/loss across epochs. This helps evaluate how well the models learned during training and whether they experienced overfitting or underfitting.

#### 2. Model Comparison
Compares the performance of all implemented models (MLP, Deep Neural Network, LSTM, and GRU) using metrics such as Accuracy, Precision, Recall, F1 Score, and ROC-AUC to identify the best-performing model.

#### 3. Confusion Matrices
Illustrates the number of correct and incorrect predictions for each model, helping evaluate classification performance through true positives, true negatives, false positives, and false negatives.

#### 4. ROC Curves
Displays the Receiver Operating Characteristic (ROC) curves and ROC-AUC scores for each model, showing how effectively they distinguish between purchase and non-purchase sessions.

#### 5. Feature Importance
Highlights the most influential features contributing to purchase intent prediction, providing insight into which browsing behaviors have the greatest impact on model decisions.

#### 6. Data Distribution
Visualizes the distribution of dataset features and the balance between purchase and non-purchase classes, helping understand the data before preprocessing and model training.

## Web application
The project includes a Flask web application for prediction and analysis.

### Goal
The app allows users to enter session details and get a real-time purchase intent prediction from the trained Deep Neural Network.

### Main pages

#### Home page
Introduces the project and links users to the prediction and dashboard pages.

#### Prediction page
Accepts session input values and returns:
- Purchase intent prediction
- Confidence score
- Short explanation
- Important indicators behind the prediction

#### Dashboard page
Displays:
- Dataset statistics
- Purchase and non-purchase session ratio
- Top correlated features
- Model comparison results

## Demo and screenshot
The repository includes:
- `Web App/web_app.mp4` for the demo video
- `Images/webapp_screenshot.png` for the web app screenshot

## Repository structure

```text
Online Shoppers Intention Prediction/
├── Dataset/
│   └── online_shoppers_intention.csv
├── Images/
│   ├── model_visualizations.pdf
│   └── webapp_screenshot.png
├── Model/
│   ├── online_shoppers_intention_prediction.ipynb
│   ├── 01_mlp_model.h5
│   ├── 02_lstm_model.h5
│   ├── 03_gru_model.h5
│   ├── 04_deep_network_model.h5
│   ├── feature_scaler.pkl
│   ├── label_encoders.pkl
│   └── target_encoder.pkl
├── Web App/
│   ├── app.py
│   ├── static/
│   ├── templates/
│   └── web_app.mp4
├── requirements.txt
└── README.md
```

## Installation

Clone the repository and install the required dependencies before running the project.

```bash
git clone <repository-url>
cd "Online Shoppers Intention Prediction"
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

If you encounter an error such as:

```text
ModuleNotFoundError: No module named 'numpy'
```

install the project dependencies after activating your virtual environment:

```bash
python3 -m pip install -r requirements.txt
```

Using `python3 -m pip` helps make sure packages are installed into the same Python environment that runs the application.

## Run the web app

After installing the dependencies, start the Flask application:

```bash
cd "Web App"
python3 app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://127.0.0.1:5000/
```

## Security improvements
The Flask application was updated to address the warnings raised during review and to make the app safer for deployment.

### Applied fixes
- `PREFERRED_URL_SCHEME = "https"`
- `SESSION_COOKIE_SECURE = True`
- `SESSION_COOKIE_HTTPONLY = True`
- `SESSION_COOKIE_SAMESITE = "Lax"`
- Added `Flask-Talisman` for HTTPS enforcement and security headers
- Added a Content Security Policy for safer script and style loading

These changes improve secure cookie handling, browser-side protections, and deployment readiness.

> **Local Development:** Flask-Talisman enforces HTTPS for production deployments. If you are running the application locally with Flask's built-in development server, you may temporarily disable the `Talisman(...)` configuration in `Web App/app.py`. Re-enable it before deploying to production so HTTPS enforcement, secure cookies, and security headers stay enabled. [web:9]

## Future improvements
- Handle class imbalance more explicitly
- Add SHAP-based explainability
- Improve dashboard interactivity
- Add API endpoints for integration
- Deploy the app to a production platform

## Author
Somapuram Uday

- GitHub: [udaycodespace](https://github.com/udaycodespace)
- LinkedIn: [Somapuram Uday](https://www.linkedin.com/in/somapuram-uday)