# 🍷 Wine Quality Prediction using Machine Learning

A comprehensive Machine Learning project that predicts wine quality using multiple **classification algorithms** while also exploring the dataset using **unsupervised clustering techniques**. The project includes data preprocessing, visualization, model comparison, clustering evaluation, and prediction using the best-performing model.

---

## 📌 Project Overview

Wine quality depends on several physicochemical properties such as acidity, pH, alcohol content, sulphates, and more. This project uses the **Red Wine Quality Dataset** to:

* Analyze and visualize the dataset
* Preprocess and scale the features
* Train multiple classification models
* Compare model performance using several evaluation metrics
* Perform clustering to discover hidden patterns
* Visualize classification and clustering results
* Predict whether a wine is **Good Quality** or **Bad Quality**

---

## 📂 Dataset

**Dataset:** Red Wine Quality Dataset

The dataset contains various physicochemical properties of red wine, including:

* Fixed Acidity
* Volatile Acidity
* Citric Acid
* Residual Sugar
* Chlorides
* Free Sulfur Dioxide
* Total Sulfur Dioxide
* Density
* pH
* Sulphates
* Alcohol

Target Variable:

* **Quality**

  * Good Wine (Quality ≥ 7)
  * Bad Wine (Quality < 7)

---

## 🚀 Features

* Data preprocessing and cleaning
* Exploratory Data Analysis (EDA)
* Feature correlation heatmap
* Standard feature scaling
* Train-test split
* Multiple supervised learning algorithms
* Multiple unsupervised learning algorithms
* Cross-validation
* Performance comparison charts
* Confusion matrices
* PCA-based clustering visualization
* Prediction using the best-performing classifier

---

## 🤖 Classification Algorithms

The following supervised learning models are implemented:

* Random Forest Classifier
* Support Vector Machine (SVM)
* K-Nearest Neighbors (KNN)
* Logistic Regression
* Gradient Boosting Classifier

---

## 📊 Clustering Algorithms

The project also performs unsupervised learning using:

* K-Means Clustering
* Agglomerative Clustering
* DBSCAN

---

## 📈 Evaluation Metrics

### Classification

* Accuracy
* Precision
* Recall
* F1-Score
* ROC-AUC Score
* Confusion Matrix
* Cross Validation

### Clustering

* Silhouette Score
* Davies-Bouldin Index
* Calinski-Harabasz Score

---

## 📉 Visualizations

The notebook generates several visualizations including:

* Wine Quality Distribution
* Volatile Acidity vs Quality
* Correlation Heatmap
* Classification Metrics Comparison
* Confusion Matrices
* Elbow Method for K-Means
* PCA Cluster Visualization
* Clustering Metrics Comparison

---

## 🛠️ Technologies Used

* Python
* NumPy
* Pandas
* Matplotlib
* Seaborn
* Scikit-learn

---

## 📁 Project Structure

```
Wine-Quality-Prediction/
│
├── Wine_Quality.ipynb
├── README.md
└── requirements.txt
├── Wine-Quality-Report.pdf
├── winequality-red.csv
```
## ▶️ How to Run

1. Install all required dependencies.
```bash
pip install -r requirements.txt
```
2. Open the notebook.
3. Execute all cells sequentially.
4. Compare the performance of all classification and clustering models.
5. Use the prediction section to classify new wine samples.

---

## 📌 Sample Prediction

Input Features:

```text
Fixed Acidity
Volatile Acidity
Citric Acid
Residual Sugar
Chlorides
Free SO₂
Total SO₂
Density
pH
Sulphates
Alcohol
```

Output:

```text
Good Quality Wine
```

or

```text
Bad Quality Wine
```

---