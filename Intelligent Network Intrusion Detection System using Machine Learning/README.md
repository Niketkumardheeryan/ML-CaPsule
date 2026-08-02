# Intelligent Network Intrusion Detection System using Machine Learning

An end-to-end Machine Learning-based Intrusion Detection System (IDS) following the schema of the **CICIDS2017** dataset. This project performs network packet feature engineering, addresses class imbalance using SMOTE, trains and compares multiple ML classifiers, incorporates SHAP explainability, and hosts an interactive Streamlit dashboard for real-time packet classification simulation and benchmarking.

## 🚀 Key Features
1. **Synthetic Data Simulator**: Generates realistic network flows modeled after CICIDS2017 attacks (DoS, Brute Force, Botnet, Infiltration, Benign).
2. **SMOTE Balancing**: Synthetically balances the training set to prevent model bias towards normal traffic (Benign).
3. **Multi-Model Comparison**: Evaluates 4 ML models:
   - Random Forest Classifier
   - XGBoost Classifier
   - LightGBM Classifier
   - Support Vector Machine (SVM)
4. **SHAP-based Explainability**: Computes SHAP values to explain feature contributions for model predictions.
5. **Real-time Packet Simulation**: A Streamlit dashboard simulating a stream of network packet flows and classifying them live.
6. **Inference Speed Benchmarking**: Compares the prediction throughput (microseconds per packet) of each ML model.

## 📁 Project Structure
```
Intelligent Network Intrusion Detection System using Machine Learning/
├── requirements.txt            # Package dependencies
├── README.md                   # Project documentation
├── dataset_generator.py        # Generates realistic synthetic traffic sample
├── train_models.py             # Preprocessing, SMOTE, and model training
├── app.py                      # Streamlit interactive dashboard
└── intrusion_detection_notebook.ipynb  # Interactive ML Pipeline Notebook
```

## 🛠️ Setup and Usage

### 1. Install Dependencies
Navigate to this directory and install the requirements:
```bash
pip install -r requirements.txt
```

### 2. Generate Dataset and Train Models
Run the training script to prepare the datasets, train models, and compute evaluation metrics & SHAP values:
```bash
python train_models.py
```
This saves `trained_artifacts.pkl` and `shap_artifacts.pkl` to the directory.

### 3. Launch the Streamlit Dashboard
Run the following command to start the interactive web UI:
```bash
streamlit run app.py
```
Open the provided URL (default: `http://localhost:8501`) in your browser.

## 📊 Evaluation Metrics
The models are evaluated on:
- **Accuracy, Precision, Recall, and F1-Score**
- **ROC-AUC Score** (weighted one-vs-rest)
- **Confusion Matrix**
- **Inference Speed** (microsecond delay per packet)
