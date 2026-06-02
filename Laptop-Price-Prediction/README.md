# 💻 Laptop Price Predictor

This is a Machine Learning project that predicts the price of a laptop based on its specifications. It includes a complete workflow from data analysis and model training to a fully functional web application built with Streamlit.

## 📂 Project Structure

- `app.py`: The main Streamlit web application.
- `modelTraining.ipynb`: Jupyter Notebook containing the data exploration, preprocessing, and model training.
- `laptop_data.csv`: The dataset used for training the model.
- `df.pkl`: Pickled pandas DataFrame containing processed data used for populating dropdowns in the web app.
- `pipe.pkl`: Pickled machine learning pipeline model used for price prediction.

## 📊 Dataset

The dataset used in this project can be found on Kaggle: [Laptop Price Prediction](https://www.kaggle.com/datasets/eslamelsolya/laptop-price-prediction)

## 🚀 Features

The application takes the following inputs to estimate the laptop's price:
- **Brand / Company**
- **Type** (e.g., Gaming, Ultrabook, Notebook)
- **RAM** (GB)
- **Weight** (kg)
- **Touchscreen & IPS Display**
- **Screen Size (Inches) & Resolution**
- **CPU Brand**
- **Storage** (HDD, SSD, Hybrid, Flash Storage)
- **GPU Brand**
- **Operating System**

## 🛠️ Technologies Used

- **Python**: Programming Language
- **Pandas & NumPy**: Data Manipulation
- **Scikit-Learn**: Machine Learning Models and Pipeline
- **Streamlit**: Web Application Framework

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd LaptopPricePrediction
   ```

2. **Install the required dependencies:**
   Make sure you have Python installed. Then, install the required packages (it is recommended to use a virtual environment). You can install the basic requirements with:
   ```bash
   pip install streamlit pandas numpy scikit-learn
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

## 🤝 Contributing

Contributions are always welcome! If you have any suggestions, bug reports, or feature requests, feel free to open an issue or submit a pull request.
