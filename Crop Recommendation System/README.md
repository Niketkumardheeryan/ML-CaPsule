# 🌾 Crop Recommendation System

A machine learning system that recommends the most suitable crop to cultivate based on soil nutrients and environmental conditions: **Nitrogen (N)**, **Phosphorus (P)**, **Potassium (K)**, **temperature**, **humidity**, **pH**, and **rainfall**.

## 📌 Overview

Farmers often struggle to choose the right crop for their land given varying soil composition and climate. This project trains and compares several classification models on soil/weather data to recommend the crop best suited to a given set of conditions, helping improve yield and resource use.

**Key features**

- Data preprocessing and exploratory data analysis (EDA)
- Feature engineering (label encoding, train/test split, feature scaling)
- Model training with multiple classification algorithms: Decision Tree, Random Forest, K-Nearest Neighbors, Naive Bayes, SVM, and Logistic Regression
- Model evaluation and comparison (accuracy, cross-validation, confusion matrix, feature importance)
- Prediction on new input values via a simple `recommend_crop()` function
- Well-documented Jupyter Notebook

## 📊 Dataset

**Source:** [Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset) (Kaggle)

- 2,200 samples, 22 crop classes, 100 samples per class (perfectly balanced)
- 7 numeric input features: `N`, `P`, `K`, `temperature`, `humidity`, `ph`, `rainfall`
- Target column: `label` (crop name)
- No missing values

| Column | Description |
|---|---|
| N | Ratio of Nitrogen content in soil |
| P | Ratio of Phosphorus content in soil |
| K | Ratio of Potassium content in soil |
| temperature | Temperature in °C |
| humidity | Relative humidity in % |
| ph | Soil pH value |
| rainfall | Rainfall in mm |
| label | Recommended crop (target) |

The dataset is downloaded automatically at runtime using `kagglehub`:

\`\`\`python
import kagglehub
path = kagglehub.dataset_download("atharvaingle/crop-recommendation-dataset")
\`\`\`
```

## 📈 Results

Six models were trained and evaluated with an 80/20 train-test split and 5-fold cross-validation:

| Model | Test Accuracy | 5-Fold CV Accuracy |
|---|---|---|
| Random Forest | ~99.5% | ~99.5% |
| Naive Bayes | ~99.5% | ~99.5% |
| SVM | ~98.4% | ~98.2% |
| Decision Tree | ~98.0% | ~98.7% |
| KNN | ~98.0% | ~97.1% |
| Logistic Regression | ~97.3% | ~97.1% |

The most influential features for crop choice (via Random Forest feature importance) are **rainfall**, **humidity**, and **potassium (K)**.

> Exact numbers are reproducible by running the notebook — see `Crop_Recommendation_System.ipynb` for full outputs, plots, and the confusion matrix.

## 🗂️ Project Structure

```
Crop Recommendation System/
├── README.md
├── requirements.txt
├── Crop_Recommendation_System.ipynb   # main notebook: EDA -> training -> evaluation -> prediction
└── model/                             # generated after running the notebook
    ├── crop_recommendation_model.pkl
    ├── label_encoder.pkl
    └── scaler.pkl
```

## ⚙️ Installation

1. Clone the repository and navigate to this project folder:
   ```bash
   git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
   cd "ML-CaPsule/Crop Recommendation System"
   ```
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. Launch Jupyter Notebook:
   ```bash
   jupyter notebook Crop_Recommendation_System.ipynb
   ```
2. Run all cells top to bottom. This will:
   - Load and explore the dataset
   - Train and compare six classification models
   - Save the best-performing model to `model/`
3. To get a recommendation for new soil/weather values, use the `recommend_crop()` function defined near the end of the notebook:
   ```python
   recommend_crop(N=90, P=42, K=43, temperature=20.9, humidity=82.0, ph=6.5, rainfall=202.9)
   # -> 'rice'
   ```

## 🛠️ Tech Stack

- Python
- pandas, NumPy
- scikit-learn
- matplotlib, seaborn
- Jupyter Notebook

## 🙌 Contributing

Suggestions and improvements are welcome — e.g. hyperparameter tuning, adding a Flask/Streamlit front end, or extending the dataset with more regional crop data. Please follow the main repository's [Contributing Guidelines](../CONTRIBUTING.md).

## 📄 License

This project follows the license of the parent repository (MIT).