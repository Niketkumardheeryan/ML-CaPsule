# Flood Prediction System using Comparative Machine Learning Models

This project focuses on predicting flood occurrences using machine learning algorithms. The dataset contains various meteorological and hydrological features, and different classification algorithms are employed to evaluate prediction capabilities, feature importance, and model performance.

The dataset is fetched dynamically on the fly via `kagglehub` from Kaggle: [varshithnagubandi/flood-prediction](https://www.kaggle.com/datasets/varshithnagubandi/flood-prediction).

---

## 📊 Dataset

The dataset contains environmental and meteorological parameters used for flood prediction:

* **Kaggle Dataset Link**: [varshithnagubandi/flood-prediction](https://www.kaggle.com/datasets/varshithnagubandi/flood-prediction)
* **Features Used**: `rainfall`, `temperature_c`, `humidity`, `water_level_m`, `elevation_m`
* **Target Variable**: `flood_occurred` (`1` → Flood likely, `0` → Flood not likely)

> **Note**: You do NOT need to manually download `.csv` files into your project folder. The dataset is fetched automatically over the web on your first run.

---

## ⚙️ Installation

### Step 1: Clone the Repository & Setup Environment

1.1 Clone the repository:
```sh
git clone https://github.com/v4rshh/FLOOD-PRED.git
cd "FLOOD-PRED/Comparative Prediction Models"
```

1.2 (Optional) Create and activate a Python environment:
```sh
# Using Conda
conda create -n flood-prediction python=3.10
conda activate flood-prediction
```

### Step 2: Install Required Packages

Install all required dependencies using `pip`:
```sh
pip install -r requirements.txt
```

*(Packages included: `pandas`, `numpy`, `scikit-learn`, `xgboost`, `matplotlib`, `seaborn`, `joblib`, `kagglehub`)*

### Step 3: Start JupyterLab (Optional)

If you plan to use Jupyter Notebooks:
```sh
jupyter lab
```

---

## 🚀 Running the Code

### Option 1: Running Terminal Python Scripts

1. **Run Exploratory Data Analysis (EDA)**:
   ```sh
   python scripts/eda.py
   ```
   *Fetches dataset via `kagglehub` and generates distribution plots saved in `eda_plots/`.*

2. **Run Model Training Scripts**:
   ```sh
   python scripts/random_forest/rf_training.py
   python scripts/xgboost/xgboost_training.py
   python scripts/logistic_regression/lr_training.py
   python scripts/svm/svm_training.py
   ```
   *Trains the model, outputs accuracy & classification reports, and saves `.joblib` model artifacts to `models/`.*

3. **Run Interactive Prediction Demo**:
   ```sh
   python scripts/random_forest/rf_prediction.py
   ```
   *Prompts for input values (Rainfall, Temperature, Humidity, Water Level, Elevation) and prints predictions.*

---

### Option 2: Running in Jupyter Notebook or Google Colab

1. Open [notebooks/Comparative_Prediction_Models_Master.ipynb](file:///c:/Users/varsh/Downloads/FLOOD-PRED/ML-CaPsule/Flood_Prediction%20models/Comparative%20Prediction%20Models/notebooks/Comparative_Prediction_Models_Master.ipynb) in JupyterLab, VS Code, or upload to [Google Colab](https://colab.research.google.com).
2. Select **Run All Cells** (`Ctrl + F9`).
3. Each cell will execute step-by-step, including data loading, EDA plots, model training, evaluation metrics, and sample inference.

---

## 🤖 Algorithms & Conclusion

### Models Compared:
* **Logistic Regression**: Probabilistic linear baseline classification.
* **Random Forest**: Tree ensemble classification and feature importance ranking.
* **Support Vector Machine (SVM)**: Hyperplane-based kernel classification.
* **XGBoost**: Gradient boosted decision tree ensemble.

### Final Results Summary:
* Each model generates Accuracy Scores, Confusion Matrices, Classification Reports, and Feature Importance Graphs.
* The workflow demonstrates how different machine learning classification models behave on environmental datasets and how to structure production-oriented ML projects.

---

## 📌 Notice

Make sure you have an active internet connection on your first run so `kagglehub` can fetch the dataset automatically. Subsequent runs will execute instantly using the local cache.
