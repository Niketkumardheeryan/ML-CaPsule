# 🩺 Health Prediction using Machine Learning

A comprehensive Machine Learning project that predicts whether an individual is at risk of a health condition based on medical, physiological, and lifestyle factors. This project demonstrates a complete machine learning pipeline, including data preprocessing, exploratory data analysis (EDA), feature engineering, model training, evaluation, and comparison of multiple classification algorithms.

---

## 📌 Features

- 📊 Exploratory Data Analysis (EDA)
- 🧹 Data preprocessing and cleaning
- 🔄 Handling categorical features using encoding
- 📏 Feature scaling
- 🤖 Training multiple machine learning classification models
- 📈 Model performance comparison
- 🎯 Health risk prediction
- 📉 Model evaluation using Accuracy precision and Recall

---

## 📂 Dataset

The dataset contains medical, physiological, and lifestyle-related information that can be used to predict an individual's health risk.

**Dataset Link:**  
https://gist.githubusercontent.com/semicolonSimp/f775e3e61b6dd5c0b31417f5208f405b/raw/2d344704811e2f6b38979b65b7892ee4a9b032ac/healthprediction

### Dataset Features

| Feature | Description |
|---------|-------------|
| Age | Age of the individual |
| BMI | Body Mass Index |
| Blood_Pressure | Blood pressure level |
| Cholesterol | Cholesterol level |
| Glucose_Level | Blood glucose level |
| Heart_Rate | Heart rate (BPM) |
| Sleep_Hours | Average sleep hours per day |
| Exercise_Hours | Daily exercise duration |
| Water_Intake | Daily water intake |
| Stress_Level | Stress level |
| Smoking | Smoking habit |
| Alcohol | Alcohol consumption |
| Diet | Overall diet quality |
| MentalHealth | Mental health status |
| PhysicalActivity | Physical activity level |
| MedicalHistory | Existing medical conditions |
| Allergies | Allergy information |
| Diet_Type | Vegan / Vegetarian / Others (One-Hot Encoded) |
| Blood_Group | Blood Group (One-Hot Encoded) |

### 🎯 Target Variable

- **0** → Healthy / Low Risk
- **1** → Health Risk / Disease

> **Note:** The exact meaning of the target depends on the dataset labeling.

---

## 🛠️ Workflow

1. Import Dataset
2. Data Cleaning
3. Exploratory Data Analysis (EDA)
4. Feature Encoding
5. Feature Scaling
6. Train-Test Split
7. Train Machine Learning Models
8. Evaluate Models
9. Compare Performance
10. Predict Health Risk

---

## 🤖 Models Used

- Logistic Regression
- K-Nearest Neighbors (KNN)
- Random Forest Classifier
- Gradient Boosting Classifier
- Voting Classifier

---

## 📊 Results

| Model | Recall |
|----------------------|:------:|
| Logistic Regression | **82.8%** |
| K-Nearest Neighbors (KNN) | **88.3%** |
| Random Forest | **95.8%** |
| Gradient Boosting | **94.9%** |
| Voting Classifier | **92.9%** |

### 🏆 Best Model

**Random Forest Classifier**

- **Accuracy:** **92.5%**
- **Recall:** **95.8%**

Random Forest achieved the highest recall and overall accuracy, making it the best-performing model for this health prediction task.

---

## 📦 Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook

---

## 📁 Project Structure

```text
Health Prediction/
├──novagen_lab.ipynb
├── README.md

```
## 📜 License

This project is intended for educational and research purposes.