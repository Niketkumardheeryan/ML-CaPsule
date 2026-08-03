# ₿ Bitcoin Price Prediction using Machine Learning

A machine learning web application that predicts **Bitcoin prices** using **Lasso Regression**. The project includes data preprocessing, exploratory data analysis (EDA), model training, model comparison, and deployment with **Streamlit**.

---

## 📌 Project Overview

Bitcoin is one of the most volatile financial assets, making price prediction an interesting machine learning problem. This project analyzes historical Bitcoin price data and builds regression models to predict future prices.

After comparing multiple machine learning algorithms, **Lasso Regression** achieved the best performance on the dataset and was selected as the final model for deployment.

---

## 🎯 Objectives

* Perform **Exploratory Data Analysis (EDA)** on historical Bitcoin data.
* Analyze feature relationships using statistical analysis and correlation.
* Visualize trends and patterns using data visualization techniques.
* Train and compare multiple regression algorithms.
* Deploy the best-performing model as an interactive **Streamlit** web application.

---

## 📊 Exploratory Data Analysis (EDA)

The project includes the following analysis:

* Loading and inspecting the dataset
* Displaying the first five rows
* Computing descriptive statistics
* Identifying missing values
* Correlation analysis between features
* Statistical analysis of the dataset
* Data visualization using:

  * Matplotlib
  * Seaborn

Visualizations help understand feature distributions, relationships, and trends before model training.

---

## 🤖 Machine Learning Models

The following regression models were trained and compared:

* Linear Regression
* Decision Tree Regressor
* **Lasso Regression (Best Performing Model)**

### Best Model

| Model                | Performance                 |
| -------------------- | --------------------------- |
| **Lasso Regression** | **99% Accuracy (R² Score)** |

> **Note:** For regression problems, metrics such as **R² Score**, **Mean Absolute Error (MAE)**, **Mean Squared Error (MSE)**, and **Root Mean Squared Error (RMSE)** provide a more complete evaluation than reporting accuracy alone.

---

## 🛠️ Technologies Used

* Python
* NumPy
* Pandas
* Matplotlib
* Seaborn
* Scikit-learn
* Streamlit

---

## 🌐 Web Application

The application is deployed using **Streamlit** and provides an interactive interface for predicting Bitcoin prices.

### Web App

https://share.streamlit.io/tandrimasingha/bitcoin-price-prediction-web-app/main/app.py

---

## 📷 Application Preview

### Home Page

![image](https://user-images.githubusercontent.com/78292851/156793113-3f6d9e91-665e-47b1-a1f6-316aaeeb2aa7.png)

### Prediction Page

![image](https://user-images.githubusercontent.com/78292851/156793297-039024d7-d263-4444-9bbb-c05e8a945d47.png)

---

## 🚀 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/bitcoin-price-prediction.git
cd bitcoin-price-prediction
```

### 2. Install the required dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 🐳 Docker Deployment

Build the Docker image:

```bash
docker build -t bitcoin-price-prediction .
```

Run the Docker container:

```bash
docker run -p 8501:8501 bitcoin-price-prediction
```

Open the application in your browser:

```text
http://localhost:8501
```

---

## 📁 Project Structure

```text
bitcoin-price-prediction/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── model/
├── dataset/
├── notebooks/
├── images/
└── README.md
```

---

## 📈 Workflow

1. Load the Bitcoin dataset.
2. Perform data cleaning and preprocessing.
3. Conduct Exploratory Data Analysis (EDA).
4. Visualize feature distributions and correlations.
5. Train multiple regression models.
6. Compare model performance.
7. Select the best-performing model.
8. Deploy the model using Streamlit.
9. Package the application with Docker for portable deployment.

---

## 📌 Key Features

* Interactive Streamlit interface
* Exploratory Data Analysis (EDA)
* Feature correlation analysis
* Multiple regression model comparison
* Real-time Bitcoin price prediction
* Docker support for easy deployment

---

## 🔮 Future Improvements

* Integrate real-time cryptocurrency market data.
* Experiment with advanced models such as XGBoost, LightGBM, and CatBoost.
* Explore deep learning models such as LSTM for time-series forecasting.
* Add model performance dashboards and prediction history.
* Deploy on cloud platforms such as AWS, Azure, or Google Cloud.

---

## 📝 Conclusion

This project demonstrates an end-to-end machine learning workflow for Bitcoin price prediction, including data analysis, feature exploration, model comparison, and deployment.

Among the evaluated models, **Lasso Regression** produced the best performance on the available dataset and was selected for the deployed application.
