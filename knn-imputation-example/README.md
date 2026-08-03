# 💡 KNN Imputation vs Mean/Median Imputation

This folder demonstrates the difference between simple univariate imputation (Mean/Median) and multivariate imputation (KNN).

## 📌 What is KNN Imputation?
K-Nearest Neighbors (KNN) Imputation estimates missing values using the average of the 'k' nearest neighbors found in the training set. It respects the underlying relationships between different features, leading to more accurate data reconstruction.

## 📊 Visual Comparison
Visualizations are generated and displayed dynamically inside the Jupyter Notebook.

### Observations:
- **Mean & Median Imputation:** The red imputed dots form a straight horizontal line. They completely ignore the relationship between experience and salary.
- **KNN Imputation:** The red imputed dots follow the natural upward trend of the data, guessing that higher experience equals higher salary.

## ⚖️ Advantages and Limitations
### ✅ Advantages of KNN Imputation:
1. **Higher Accuracy:** Utilizes relationships between multiple variables.
2. **Flexible:** Can be used for continuous and categorical data (if encoded properly).
3. **No strict distribution assumption:** Doesn't assume the data is normally distributed.

### ❌ Limitations of KNN Imputation:
1. **Computationally Expensive:** Calculating distances between all points takes time.
2. **Sensitive to Outliers:** Extreme outliers can skew nearest neighbors.
3. **Requires Feature Scaling:** Variables must be normalized before using KNN.

## 🚀 How to Run
Open `knn_imputation.ipynb` in any Jupyter Notebook environment (like VS Code, Zed, or Jupyter Lab) and run all the cells sequentially to see the data and plots.
