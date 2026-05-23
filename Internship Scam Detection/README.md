# Internship Scam Detection System

An end-to-end Machine Learning pipeline built to identify fraudulent internship postings using metadata signals, text features, and recruiter behavior analytics. This system processes **1,000,000 rows of data** completely leak-free using automated Scikit-Learn pipelines and optimizes a classification tree to achieve an **overall baseline accuracy of 90%**.

---

## 📊 Dataset Attribution

This project utilizes a subset of the **Internship Scam Detection Dataset** hosted on Kaggle. 

* **Dataset Author / Credits:** Special thanks to **aiexplorer77** for compiling and sharing this valuable open-source security benchmark.
* **Original Link:** https://www.kaggle.com/datasets/aiexplorer77/internship-scam-detection-dataset
* **Note on Scope:** The data handled in this repository represents a balanced, optimized subset extracted from the larger master dataset to facilitate fast pipeline prototyping and hyperparameter tuning.

---

## 🛠️ System Architecture & Engineering Rigor

This project strictly adheres to robust machine learning practices to ensure the model remains reliable, robust, and capable of generalizing to new, real-world data.

* **Step 1: Raw Data Ingestion & Target Selection**
* **Step 2: Explicit Train-Test Split (80% Train / 20% Test)**
* **Step 3: Automated ColumnTransformer Pipelines**
* **Step 4: GridSearchCV Hyperparameter Tuning**
* **Step 5: Robust Final Assessment**

### 1. Data Isolation (Strict Anti-Leakage Guardrail)
Following strict machine learning discipline, the data is split into **80% training** and **20% testing** partitions *before* any statistical computations (like medians or category frequencies) occur. This keeps the test set completely pristine and ensures zero data leakage.

### 2. Specialized Multi-Path Preprocessing
Because missing data and text types require different mathematical treatments, an automated `ColumnTransformer` handles feature transformations dynamically on the fly:
* **Stipend Path:** Imputes missing stipends with a constant `0` (indicating an unpaid position) and normalizes using `StandardScaler`.
* **Company Age & Trust Score Paths:** Separately impute missing values using the split-isolated `median` strategy to preserve original distributions safely.
* **Categorical Path:** Automatically detects structural text properties (`employment_type`, `work_mode`, `industry`) and converts them into machine-readable numeric formats via `OneHotEncoder`.
* **High-Cardinality Drop-List:** Non-predictive string identifiers like `posting_date`, `internship_title`, `company_name`, and `location` are explicitly excluded from training to keep the model focused entirely on behavior patterns.

### 3. Eliminating Target Leakage
During exploratory data analysis (EDA), a pre-calculated feature (`fraud_score`) showed a massive `0.76` correlation with the target variable, artificially yielding a flawless `1.00` accuracy. To prevent the model from relying on a "cheat code" that wouldn't exist in a live user-facing application, **`fraud_score` was deliberately removed from the feature matrix**, forcing the model to learn entirely from raw behavioral attributes.

---

## 📈 Model Performance & Optimization

The baseline `DecisionTreeClassifier` was systematically optimized using **Grid Search (`GridSearchCV`)** with 3-fold cross-validation across 18 parameter candidates (54 total fits). The grid automatically optimized tree constraints to prevent overfitting.

### Mathematically Optimal Hyperparameters:
* **Criterion:** `entropy`
* **Maximum Depth (`max_depth`):** `15`
* **Minimum Samples to Split (`min_samples_split`):** `20`

### Final Optimized Evaluation Report:
```bash
precision    recall  f1-score   support

       0       0.92      0.95      0.93    155728 (Safe Postings)
       1       0.79      0.71      0.75     44272 (Fake Postings)

accuracy                           0.90    200000
macro avg      0.86      0.83      0.84    200000
weighted avg   0.89      0.90      0.89    200000
```

### Key Metrics Decoded:
* **Overall Accuracy (90%):** The model makes the correct call 9 out of 10 times across the entire 200,000-row testing pool.
* **Scam Precision (79%):** When the system flags an internship as a scam, it is right **79% of the time**, minimizing false alarms for students.
* **Scam Recall (71%):** The model successfully catches **71% of all fraudulent postings** circulating in the dataset based purely on structural patterns.

---

## 🚀 Key Libraries Used
* **Pandas & NumPy** — High-performance data manipulation and distribution analysis.
* **Matplotlib** — Exploratory visualizations (Histograms and Scatter Matrices).
* **Scikit-Learn** — Pipeline automation, `ColumnTransformer`, `GridSearchCV`, and tree classification architectures.