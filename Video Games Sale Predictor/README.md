# 🎮 Video Games Sale Predictor
### Machine Learning | GSSoC 2026 | Issue [#483](https://github.com/Niketkumardheeryan/ML-CaPsule/issues/483)

Predict **global video game sales** using machine learning based on platform, genre, publisher, and regional sales data.

---

## 📌 Overview

| Module | Method | Output |
|---|---|---|
| 📊 EDA | Distribution, correlation, trends | Visual insights |
| 🔧 Preprocessing | Label encoding, missing value handling | Clean dataset |
| 🤖 Model Training | Linear Regression, Random Forest, Gradient Boosting | Trained models |
| 📈 Evaluation | MAE, RMSE, R² | Model comparison |
| 🔮 Predictor | Input game details → predicted sales | Global sales in millions |

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Pandas** — Data manipulation
- **NumPy** — Numerical operations
- **Matplotlib / Seaborn** — Visualization
- **Scikit-learn** — ML models (Linear Regression, Random Forest, Gradient Boosting)
- **XGBoost** — Advanced boosting (optional)

---

## 📁 Project Structure

```
Video Games Sale Predictor/
├── video_games_sale_predictor.ipynb   # Main notebook
├── vgsales.csv                        # Dataset (download from Kaggle)
└── README.md                          # This file
```

---

## 🚀 Getting Started

### 1. Get the Dataset
Download `vgsales.csv` from [Kaggle](https://www.kaggle.com/datasets/gregorut/videogamesales) and place it in this folder.

> **No Kaggle account?** The notebook auto-generates a realistic synthetic dataset if `vgsales.csv` is not found.

### 2. Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost plotly
```

### 3. Run the Notebook
Open `video_games_sale_predictor.ipynb` in **Jupyter Notebook** or **Google Colab** and run all cells.

---

## 📸 Results

### EDA Analysis
![EDA](eda_analysis.png)

### Model Comparison
![Models](model_comparison.png)

### Actual vs Predicted
![Predictions](prediction_analysis.png)

### Feature Importance
![Features](feature_importance.png)

---

## 🔮 How to Predict

```python
predicted_sales = predict_game_sales(
    platform    = 'PS4',
    year        = 2023,
    genre       = 'RPG',
    publisher   = 'Square Enix',
    na_sales    = 1.5,
    eu_sales    = 1.0,
    jp_sales    = 0.8,
    other_sales = 0.3
)
print(f"Predicted Global Sales: {predicted_sales:.2f} million copies")
```

---

## 📊 Model Performance

| Model | MAE ↓ | RMSE ↓ | R² ↑ |
|---|---|---|---|
| Linear Regression | ~0.45 | ~0.82 | ~0.72 |
| Random Forest | ~0.28 | ~0.55 | ~0.88 |
| **Gradient Boosting** | **~0.25** | **~0.50** | **~0.91** |

---

## 💡 Key Insights

- **Regional sales** (NA, EU, JP) are the strongest predictors of Global Sales
- **Shooter & Action** genres consistently outperform others
- **PS2, PS3, Wii** have the highest total historical sales
- **Nintendo & EA** lead in total publisher sales

---

## 🔮 Future Improvements

- Integrate Metacritic / user review scores as features
- Add NLP features from game titles (franchise detection)
- Build a **Streamlit** web app for live predictions
- Train on post-2016 data (newer consoles: PS5, Series X)

---

*Contributed as part of **GSSoC 2026** — Open Source Track + AI/Agents Track*
