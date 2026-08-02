# 🛒 Online Shopper Intention Prediction

## 📌 Overview

The **Online Shopper Intention Prediction** project aims to predict whether an online visitor will generate revenue (make a purchase) based on their browsing behavior and session information. Machine learning models are trained to analyze customer interactions and identify purchase intent.

---

## 📂 Dataset

The dataset used in this project can be accessed from the following Gist:

**Dataset:**
https://gist.githubusercontent.com/semicolonSimp/96a697d0d84097bf67c86b37679d5ff4/raw/4e20eb1d62833346cff19363d9ad1e8dbee4c9ad/shop_smart_ecommerce

---

## 📊 Dataset Features

| Feature                 | Description                                                    |
| ----------------------- | -------------------------------------------------------------- |
| Administrative          | Number of administrative pages visited                         |
| Administrative_Duration | Time spent on administrative pages                             |
| Informational           | Number of informational pages visited                          |
| Informational_Duration  | Time spent on informational pages                              |
| ProductRelated          | Number of product-related pages visited                        |
| ProductRelated_Duration | Time spent on product-related pages                            |
| BounceRates             | Percentage of visitors leaving after one page                  |
| ExitRates               | Exit rate of visited pages                                     |
| PageValues              | Average value of visited pages before purchase                 |
| SpecialDay              | Closeness to a special shopping day                            |
| Month                   | Month of the visit                                             |
| OperatingSystems        | Visitor's operating system                                     |
| Browser                 | Browser used                                                   |
| Region                  | Visitor's region                                               |
| TrafficType             | Source of website traffic                                      |
| VisitorType             | Type of visitor (New/Returning)                                |
| Weekend                 | Whether the visit occurred on a weekend                        |
| Revenue                 | Target variable indicating whether the visitor made a purchase |

---

## 🧠 Machine Learning Algorithms Used

* Decision Tree Classifier
* Logistic Regression
* Random Forest Classifier
* Gradient Boosting Classifier
* XGBoost Classifier

---

## ⚙️ Workflow

1. Load and explore the dataset.
2. Perform data preprocessing.
3. Encode categorical features.
4. Split the dataset into training and testing sets.
5. Train multiple machine learning models.
6. Evaluate each model using classification metrics.
7. Compare model performance and identify the best-performing algorithm.

---

## 📈 Model Performance

| Model                        | Performance          |
| ---------------------------- | -------------------- |
| Decision Tree Classifier     | Evaluated            |
| Logistic Regression          | Evaluated            |
| Random Forest Classifier     | Evaluated            |
| Gradient Boosting Classifier | Evaluated            |
| XGBoost Classifier           | **Best Performance** |

### 🏆 Best Model

**XGBoost Classifier achieved the highest accuracy of 89.13%, outperforming all other machine learning algorithms evaluated in this project.**

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-learn
* XGBoost

---

## 🚀 Future Improvements

* Hyperparameter tuning using GridSearchCV or RandomizedSearchCV.
* Feature engineering to improve predictive performance.
* Cross-validation for more robust evaluation.
