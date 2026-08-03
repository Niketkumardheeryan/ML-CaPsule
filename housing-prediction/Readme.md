# 🏠 House Price Prediction

## GOAL
Predict California housing prices using regression techniques, leveraging features such as geographic location, household income, and housing characteristics. This project demonstrates a complete supervised machine learning pipeline from data loading to hyperparameter tuning.

---

## DATASET
- **Source:** California Housing Dataset (Aurélien Géron — Hands-On ML2 repository)
- **Auto-fetch:** The notebook automatically downloads the dataset on first run
- **Training Examples:** ~16,512
- **Test Examples:** ~4,128
- **Target Variable:** `median_house_value` (USD)

---

## MODELS USED
| Model | RMSE | Notes |
|---|---|---|
| Linear Regression | ~67,239 | Baseline — underfits the data |
| Decision Tree Regressor | ~69,383 | Overfits — poor cross-val performance |
| **Random Forest Regressor** | **~48,100** | **Best model — used for final evaluation** |

**Final R² Score: 82.25%** (after Grid Search CV hyperparameter tuning)

---

## LIBRARIES NEEDED
```
numpy
pandas
matplotlib
scikit-learn
six
joblib
```

Install all at once:
```bash
pip install numpy pandas matplotlib scikit-learn six joblib
```

---

## HOW TO RUN

**Step 1 — Clone the repository and navigate to the project:**
```bash
cd ML-CaPsule/Housing_Prediction
```

**Step 2 — Install dependencies:**
```bash
pip install numpy pandas matplotlib scikit-learn six joblib
```

**Step 3 — Launch Jupyter Notebook:**
```bash
jupyter notebook main_housing.ipynb
```

**Step 4 — Run all cells in order:**
Go to `Kernel → Restart & Run All`

> **Note:** The first run will automatically download the dataset from the internet. Subsequent runs use the cached local copy.

---

## STEPS FOLLOWED

1. **Data Loading** — Fetches the California Housing dataset from Aurélien Géron's Hands-On ML2 GitHub repository and loads it into a pandas DataFrame.

2. **Stratified Train/Test Split** — Creates an `income_cat` column by binning `median_income` into 5 brackets, then uses `StratifiedShuffleSplit` to maintain the income distribution in both the training (80%) and test (20%) sets. This prevents sampling bias on the most important feature.

3. **Exploratory Data Analysis (EDA)** — Engineers three new informative features:
   - `rooms_per_house` = total_rooms / households
   - `bedrooms_per_rooms` = total_bedrooms / total_rooms
   - `population_per_house` = population / households
   
   Then computes Pearson correlation to identify the strongest predictors of house value.

4. **Data Preprocessing Pipeline** — Applies a `ColumnTransformer` that:
   - Imputes missing values in numeric columns using the median
   - Scales numeric features using `StandardScaler`
   - One-hot encodes the categorical `ocean_proximity` feature

5. **Model Training & Comparison** — Trains three models (Linear Regression, Decision Tree, Random Forest) and compares them using 10-fold cross-validation RMSE scores.

6. **Hyperparameter Tuning** — Uses `GridSearchCV` to find the optimal `n_estimators` and `max_features` for the Random Forest Regressor across 90 training runs.

7. **Final Evaluation** — Evaluates the best model on the held-out test set, reporting RMSE and R² score.

---

## CONCLUSION
The **Random Forest Regressor** significantly outperformed both the Linear Regression and Decision Tree models. The stratified split on `median_income` ensured both the training and test sets accurately reflect the income distribution of the full dataset, leading to more reliable model evaluation. Hyperparameter tuning via Grid Search CV further improved performance, achieving an R² of **82.25%** and an RMSE of **~48,100 USD**.

---

*Contributed by: [Chirag](https://github.com/chiragHimself)*
