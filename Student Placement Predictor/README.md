# 🎓 Student Placement Predictor

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikit-learn)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

## 📖 Overview

Student Placement Predictor is an end-to-end Machine Learning project that predicts whether a student is likely to be placed based on their academic performance, technical skills, projects, internships, and extracurricular activities.

This project demonstrates the complete machine learning workflow—from loading a dataset and performing Exploratory Data Analysis (EDA) to preprocessing, model training, evaluation, and building an interactive web application using Streamlit.

The primary objective of this project is educational. It serves as a beginner-friendly example for understanding how a machine learning model is developed, evaluated, saved, and deployed as an interactive web application.

---

# ✨ Features

- 📊 Exploratory Data Analysis (EDA)
- 🧹 Data Cleaning & Preprocessing
- 🤖 Comparison of Multiple Machine Learning Models
- 📈 Model Evaluation using various metrics
- 💾 Save the trained model using Joblib
- 🌐 Interactive Streamlit Web Application
- 💡 Personalized suggestions based on prediction
- 🔍 Feature contribution analysis for explainability

---

# 🛠️ Tech Stack

| Category | Technologies |
|-----------|--------------|
| Programming Language | Python |
| Data Analysis | Pandas, NumPy |
| Data Visualization | Matplotlib, Seaborn |
| Machine Learning | Scikit-Learn |
| Model Serialization | Joblib |
| Web Framework | Streamlit |
| Development Environment | Jupyter Notebook |

---

# 📂 Project Structure

```text
Student Placement Predictor/
│
├── app.py
├── placement_predictor.ipynb
├── placement_classifier.pkl
├── requirements.txt
├── README.md
└── student_placement_prediction_dataset_2026.csv
```

| File | Description |
|------|-------------|
| **placement_predictor.ipynb** | Contains the complete machine learning workflow including EDA, preprocessing, model training, evaluation, and saving the trained model. |
| **placement_classifier.pkl** | Serialized machine learning pipeline used by the Streamlit application for prediction. |
| **app.py** | Interactive Streamlit application for predicting placement status. |
| **requirements.txt** | List of required Python libraries. |
| **student_placement_prediction_dataset_2.csv** | Dataset used to train and evaluate the model. |
| **README.md** | Project documentation. |

---

# 📊 Dataset

The project uses a synthetic student placement dataset consisting of approximately **100,000 student records** and **26 features**.

Each record represents one student's academic profile, technical skills, projects, internships, communication ability, extracurricular involvement, and placement outcome.

The target variable is:

```text
placement_status
```

where

- **Placed**
- **Not Placed**

are the two prediction classes.

---

## 📋 Features in the Dataset

### 👤 Personal Information

- age
- gender

### 🎓 Academic Information

- cgpa
- branch
- college_tier
- attendance_percentage
- backlogs

### 💼 Experience

- internships_count
- projects_count
- certifications_count
- github_repos
- hackathons_participated

### 💻 Technical Skills

- coding_skill_score
- aptitude_score
- communication_skill_score
- logical_reasoning_score
- mock_interview_score

### 🌟 Extracurricular Activities

- extracurricular_score
- leadership_score
- volunteer_experience

### 💤 Lifestyle

- sleep_hours
- study_hours_per_day

---

# 🎯 Project Workflow

The project follows a complete Machine Learning pipeline.

```text
Dataset
   │
   ▼
Exploratory Data Analysis
   │
   ▼
Data Cleaning
   │
   ▼
Preprocessing
   │
   ▼
Feature Engineering
   │
   ▼
Model Training
   │
   ▼
Model Evaluation
   │
   ▼
Model Selection
   │
   ▼
Save Model (.pkl)
   │
   ▼
Streamlit Web Application
```

Every stage of this workflow is implemented inside the Jupyter Notebook, while the trained model is later loaded by the Streamlit application for real-time predictions.

---

# 🔍 Exploratory Data Analysis (EDA)

Before training any machine learning model, the dataset was carefully explored to understand its characteristics.

The following analyses were performed:

- Dataset shape
- Feature names
- Data types
- Missing values
- Duplicate records
- Statistical summary
- Target variable distribution
- Correlation analysis
- Feature distributions

Performing EDA helps identify potential issues such as missing values, imbalanced classes, incorrect data types, outliers, and data leakage before model training.

---

# ⚠️ Data Leakage Detection

One important issue discovered during EDA was **data leakage**.

The column:

```text
salary_package_lpa
```

contained:

```text
Placed      → Salary > 0

Not Placed  → Salary = 0
```

If this feature were used during training, the model would simply learn the answer directly instead of identifying meaningful patterns from student characteristics.

To avoid misleadingly high accuracy, this feature was removed before training.

Similarly,

```text
student_id
```

was also removed because it is only a unique identifier and carries no predictive information.

Removing these columns ensures that the model learns genuine relationships between student attributes and placement outcomes.

---

# 🧹 Data Preprocessing

Raw data cannot always be directly used for training machine learning models. Before model training, several preprocessing steps were performed to ensure that the data was suitable for learning.

## 1. Removing Unnecessary Features

The following columns were removed from the dataset before training:

| Column | Reason |
|---------|--------|
| `student_id` | Unique identifier with no predictive value. |
| `salary_package_lpa` | Introduced data leakage because it directly revealed the placement status. |

Removing these features helps prevent the model from learning misleading patterns.

---

## 2. Separating Features and Target

The dataset was divided into:

- **Features (`X`)** → Student information used for prediction
- **Target (`y`)** → `placement_status`

```python
X = dataset.drop("placement_status", axis=1)
y = dataset["placement_status"]
```

---

## 3. Identifying Numerical and Categorical Features

The dataset contains two types of data.

### Numerical Features

Examples include:

- age
- cgpa
- coding_skill_score
- aptitude_score
- attendance_percentage
- internships_count
- projects_count
- sleep_hours
- study_hours_per_day

### Categorical Features

Examples include:

- gender
- branch
- college_tier
- volunteer_experience

Since machine learning algorithms only understand numbers, categorical values must be converted into numerical representations.

---

## 4. Feature Scaling

Numerical features were standardized using **StandardScaler**.

Standardization transforms every numerical feature so that it has:

- Mean = 0
- Standard Deviation = 1

This ensures that features with larger numerical values do not dominate the learning process.

---

## 5. Encoding Categorical Variables

Categorical variables were transformed using **One-Hot Encoding**.

For example,

```text
Branch

CSE
IT
ECE
Mechanical
Civil
```

becomes

```text
Branch_CSE
Branch_IT
Branch_ECE
Branch_Mechanical
Branch_Civil
```

This enables machine learning algorithms to process categorical information effectively.

---

## 6. ColumnTransformer

Instead of preprocessing columns separately, Scikit-Learn's `ColumnTransformer` was used to combine all preprocessing steps into a single reusable pipeline.

This ensures that:

- Training data
- Testing data
- New user inputs from the Streamlit application

are all transformed consistently.

---

# ✂️ Train-Test Split

The processed dataset was divided into:

- **80% Training Data**
- **20% Testing Data**

```text
100,000 Students
│
├── 80,000 → Training
└── 20,000 → Testing
```

The model only learns from the training data.

The testing dataset remains completely unseen during training and is used to evaluate how well the model generalizes to new data.

---

# 🤖 Machine Learning Models

Two supervised classification algorithms were trained and compared.

---

## 1. Logistic Regression

Logistic Regression is a simple yet powerful linear classification algorithm.

### Advantages

- Fast training
- Easy to interpret
- Works well on structured datasets
- Produces prediction probabilities

---

## 2. Random Forest Classifier

Random Forest is an ensemble learning algorithm that combines multiple decision trees.

### Advantages

- Handles nonlinear relationships
- Robust against overfitting
- Performs automatic feature selection
- Works well with mixed data types

---

# 🔄 Cross Validation

Instead of relying on a single train-test split, **5-Fold Cross Validation** was used to evaluate both models.

```text
Dataset

↓

Split into 5 parts

↓

Train on 4 parts

↓

Test on remaining part

↓

Repeat 5 times

↓

Average Score
```

Cross-validation provides a more reliable estimate of model performance by reducing dependence on a single random split.

---

# 📊 Model Comparison

Both models were compared using **ROC-AUC**, which measures how well a classifier distinguishes between the two classes.

| Model | Mean ROC-AUC |
|---------|-------------|
| Logistic Regression | **0.585** |
| Random Forest | **0.580** |

Although the difference is small, Logistic Regression consistently achieved the higher average score and was selected as the final model.

---

# 📈 Model Evaluation

After selecting the best model, it was evaluated on the unseen test dataset.

| Metric | Score |
|---------|-------|
| Accuracy | 0.570 |
| Precision | 0.579 |
| Recall | 0.772 |
| F1 Score | 0.662 |
| ROC-AUC | 0.585 |

---

## 📖 Understanding the Evaluation Metrics

### Accuracy

Measures the percentage of correctly classified students.

```
Accuracy = Correct Predictions / Total Predictions
```

---

### Precision

Among all students predicted as **Placed**, Precision measures how many were actually placed.

Higher Precision means fewer false positives.

---

### Recall

Recall measures how many actually placed students were successfully identified by the model.

Higher Recall means fewer false negatives.

---

### F1 Score

The F1 Score balances Precision and Recall.

It is especially useful when evaluating classification models where both false positives and false negatives are important.

---

### ROC-AUC

ROC-AUC measures how well the model separates the two classes.

```
0.50 → Random Guess

0.60 → Weak Model

0.70 → Good Model

0.80 → Strong Model

0.90+ → Excellent Model
```

The obtained ROC-AUC of **0.585** indicates that the dataset contains only a weak predictive signal, which was also confirmed during Exploratory Data Analysis.

---

# 💾 Saving the Trained Model

After selecting the best-performing model, the complete machine learning pipeline—including preprocessing and the trained classifier—was saved using **Joblib**.

```python
joblib.dump(model, "placement_classifier.pkl")
```

Saving the pipeline makes it possible to load the trained model directly inside the Streamlit application without retraining it every time.

The saved model file is:

```text
placement_classifier.pkl
```

---

# 📓 Notebook Workflow

The notebook (`placement_predictor.ipynb`) contains the complete machine learning pipeline from start to finish.

The workflow implemented in the notebook is:

1. Import required libraries
2. Load the dataset
3. Explore the dataset
4. Perform Exploratory Data Analysis
5. Detect missing values
6. Remove unnecessary columns
7. Detect and remove data leakage
8. Identify numerical and categorical features
9. Build preprocessing pipeline
10. Split training and testing data
11. Train Logistic Regression
12. Train Random Forest
13. Compare both models using Cross Validation
14. Evaluate the best model
15. Save the trained pipeline using Joblib

The notebook serves as the core of the project, while the Streamlit application uses the saved model to make predictions on new user inputs.

---
# 🌐 Streamlit Web Application

After training the machine learning model, an interactive web application was developed using **Streamlit**. The application loads the saved machine learning pipeline (`placement_classifier.pkl`) and allows users to predict whether a student is likely to be placed based on their academic profile, technical skills, experience, and extracurricular activities.

The application is designed to be simple, interactive, and beginner-friendly, demonstrating how a trained machine learning model can be integrated into a web interface for real-time predictions.

---

## ✨ Features

The Streamlit application provides the following functionality:

- 🎓 Interactive student profile form
- 📊 Placement prediction
- 📈 Placement probability score
- 📉 Progress bar indicating prediction confidence
- 🔍 Top factors contributing positively to placement
- ⚠️ Top factors reducing placement chances
- 💡 Personalized suggestions for improvement
- ℹ️ Information about the model's reliability

---

## 📝 Input Parameters

The application collects the following information from the user.

### 👤 Personal Information

- Age
- Gender

### 🎓 Academic Information

- Branch
- College Tier
- CGPA
- Attendance Percentage
- Number of Backlogs

### 💼 Experience

- Number of Internships
- Number of Projects
- Number of Certifications
- Number of Hackathons Participated
- GitHub Repositories

### 💻 Technical Skills

- Coding Skill Score
- Aptitude Score
- Communication Skill Score
- Logical Reasoning Score
- Mock Interview Score

### 🌟 Activities

- Leadership Score
- Extracurricular Score
- Volunteer Experience

### 💤 Lifestyle

- Sleep Hours
- Study Hours per Day

---

## 📤 Prediction Output

Once all details are entered, clicking the **Predict** button displays:

- Predicted Placement Status
- Placement Probability
- Confidence Progress Bar
- Top Positive Factors influencing placement
- Top Negative Factors affecting placement
- Personalized recommendations to improve placement chances
- Information about the model's reliability

This makes the prediction process more transparent by helping users understand **why** the model generated a particular prediction instead of only displaying the final result.

---



# ▶️ Running the Project

## Step 1: Install the Required Dependencies

Install all the required Python libraries using:

```bash
pip install -r requirements.txt
```

---

## Step 2: Open the Jupyter Notebook

Open the notebook:

```text
placement_predictor.ipynb
```

Run all cells sequentially.

The notebook performs the complete machine learning workflow, including:

- Loading the dataset
- Exploratory Data Analysis (EDA)
- Data cleaning
- Detecting and removing data leakage
- Data preprocessing
- Building the preprocessing pipeline
- Training Logistic Regression and Random Forest models
- Comparing model performance using Cross Validation
- Evaluating the best-performing model
- Saving the trained pipeline as:

```text
placement_classifier.pkl
```

---

## Step 3: Run the Streamlit Application

After the trained model has been saved, launch the Streamlit application using:

```bash
streamlit run app.py
```

The application will automatically open in your default web browser.

Using the application, users can:

- Enter a student's profile
- Predict placement status
- View the placement probability
- Understand the factors influencing the prediction
- Receive personalized suggestions for improvement

---


# 📚 Learning Outcomes

This project demonstrates the complete end-to-end machine learning workflow, including:

- Understanding a structured dataset
- Performing Exploratory Data Analysis (EDA)
- Detecting and removing data leakage
- Cleaning and preprocessing data
- Encoding categorical features
- Scaling numerical features
- Building preprocessing pipelines using Scikit-Learn
- Training and comparing multiple classification models
- Evaluating model performance using standard classification metrics
- Saving trained models for reuse
- Building an interactive web application using Streamlit


---

# 👩‍💻 Author

**Pragya Manna**


---

<p align="center">
Made with ❤️ using Python, Scikit-Learn, and Streamlit.
</p>