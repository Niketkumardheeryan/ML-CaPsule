#  Crop Yield Prediction

This project predicts **crop yield (Q/acre)** using environmental and nutrient parameters such as rainfall, fertilizer, temperature, nitrogen, phosphorus, and potassium.  
It demonstrates a complete **machine learning pipeline** — from data preprocessing and visualization to model training and evaluation.

---

##  Dataset
The dataset used is `crop yield data sheet.xlsx`, containing:
- Rain Fall (mm)
- Fertilizer
- Temperature
- Nitrogen (%)
- Phosphorus (%)
- Potassium (%)
- Yield (Q/acre)

---

##  Workflow Overview
1. **Data Loading & Inspection**
   - Read Excel file using `pandas`
   - Check missing values, data types, and duplicates

2. **Data Cleaning**
   - Convert non-numeric columns using `pd.to_numeric(errors='coerce')`
   - Handle missing values with `SimpleImputer(strategy='median')`
   - Drop duplicates

3. **Exploratory Data Analysis (EDA)**
   - Summary statistics (`data.describe()`)
   - Correlation matrix and heatmap (`sns.heatmap`)
   - Boxplots and KDE plots for feature distributions
   - Scatter plots to visualize relationships with yield

4. **Model Building**
   - Split data into train/test sets
   - Create pipelines with `StandardScaler` and regressors:
     - Linear Regression
     - Random Forest Regressor
     - Gradient Boosting Regressor

5. **Evaluation**
   - Compute `r2_score` for each model
   - Compare performances
   - **Linear Regression achieved best performance (R² ≈ 0.93)**

---

##  Key Insights
- Temperature and nutrient levels strongly correlate with yield.
- Linear Regression provides a simple yet effective baseline.
- Feature scaling and imputation improve model stability.

---

##  Visualizations
- Correlation heatmap
- Boxplots of all features
- KDE plots for distribution analysis
- Scatter plots showing yield relationships


