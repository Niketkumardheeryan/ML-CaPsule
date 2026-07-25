# Flood Prediction Machine Learning Model

This Python project focuses on predicting floods using machine learning algorithms. The dataset used in this project contains various meteorological features from historical Indian monsoonal rainfall records, and different classification algorithms are employed to predict flood occurrences.

---

## 📊 Dataset

The dataset is fetched dynamically on the fly via `kagglehub` from Kaggle:

* **Kaggle Dataset Link**: [varshithnagubandi/indian-flood-prediction](https://www.kaggle.com/datasets/varshithnagubandi/indian-flood-prediction)
* **File**: `India.csv` (86 historical annual records × 16 columns)
* **Features**: `YEAR`, `JAN`, `FEB`, `MAR`, `APR`, `MAY`, `JUN`, `JUL`, `AUG`, `SEP`, `OCT`, `NOV`, `DEC`, `ANNUAL RAINFALL`
* **Target Variable**: `FLOODS` (`YES` / `NO`)

> **Note**: You do NOT need to manually download `.csv` files into your project folder. The dataset is fetched automatically over the web on your first run.

---

## ⚙️ Installation

### Step 1: Clone the Repository & Setup Environment

1.1 Clone the repository:
```sh
git clone https://github.com/v4rshh/FLOOD-PRED.git
cd "FLOOD-PRED/Classical_Prediction"
```

1.2 (Optional) Create and activate a Python environment:
```sh
# Using Conda
conda create -n flood-prediction python=3.10
conda activate flood-prediction
```

### Step 2: Install Required Packages

Install the required packages using `pip`:
```sh
pip install -r requirements.txt
```

*(Packages included: `numpy`, `pandas`, `matplotlib`, `scikit-learn`, `seaborn`, `kagglehub`)*

### Step 3: Start JupyterLab

Launch JupyterLab:
```sh
jupyter lab
```

---

## 🚀 Running the Code

### Option 1: Running the Jupyter Notebook

1. Open and run the Jupyter Notebook `Model/Flood_Prediction.ipynb` in JupyterLab, VS Code, or upload to [Google Colab](https://colab.research.google.com):
   ```sh
   Model/Flood_Prediction.ipynb
   ```
2. Use `Shift + Enter` (or click **Run All Cells**) to execute code cells step by step. Each cell will provide the output of different processes, including dynamic dataset loading, data exploration, model training, and evaluation.

---

## 📈 Conclusion & Results Summary

* The project utilizes several machine learning algorithms to predict flood occurrences.
* **Models Compared**:
  * **K-Nearest Neighbors (KNN)**
  * **Support Vector Classification (SVC)**
  * **Logistic Regression**
  * **Random Forest Classifier**
  * **Decision Tree Classifier**

### Final Results Table:

| Model | Accuracy (%) | Recall (%) | ROC-AUC (%) |
|---|---|---|---|
| **K-Nearest Neighbors** | **77.78%** | **100.00%** | **71.43%** |
| **SVC** | 72.22% | 100.00% | 64.29% |
| **Logistic Regression** | 66.67% | 63.64% | 67.53% |
| **Random Forest** | 66.67% | 100.00% | 57.14% |
| **Decision Tree** | 61.11% | 72.73% | 57.79% |

---

## 📌 Notice

Make sure you have an active internet connection on your first run so `kagglehub` can fetch the dataset automatically. Subsequent runs will execute instantly using the local cache.