## **Startup Profit Prediction**

**GOAL**

The goal of this project is to analyze and predict the profit of a startup using key features: 'R&D Spend', 'Administration', 'Marketing Spend', and 'State'.

**DATASET**

The dataset can be downloaded from [here](https://www.kaggle.com/sonalisingh1411/startup50). The raw dataset is located in `dataset/50_Startups.csv`.

---

## **PROJECT STRUCTURE**

```
Startup_Profit_Prediction/
│
├── dataset/
│   └── 50_Startups.csv         # Raw startup dataset
│
├── models/
│   ├── linear_regression.joblib # Serialized Linear Regression model
│   ├── lasso_regression.joblib  # Serialized Lasso Regression model
│   └── ridge_regression.joblib  # Serialized Ridge Regression model
│
├── train.py                    # Script to train and serialize all models
├── predict.py                  # Script to handle CLI & API profit predictions
├── utils.py                    # Shared loading and preprocessing pipeline logic
├── Startup_Profit_Prediction.ipynb # Original exploration Jupyter Notebook
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

---

## **SETUP & INSTALLATION**

1. Clone or navigate to the project directory:
   ```bash
   cd Startup_Profit_Prediction
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## **TRAINING THE MODELS**

To train all three models (Linear, Lasso, and Ridge Regression) and generate their corresponding serialized `.joblib` files, run:

```bash
python train.py
```

### Advanced Training Options:
You can specify custom train/test split size, random state seed, and target output directory:
```bash
python train.py --test-size 0.2 --seed 42 --output-dir models/
```

---

## **MAKING PREDICTIONS**

To predict the profit of a startup, run `predict.py` and specify which model type to load (`linear`, `lasso`, or `ridge`):

```bash
python predict.py --rd 165349 --admin 136897 --marketing 471784 --state "New York" --model ridge
```

### Parameters:
- `--rd`: R&D Spend (float)
- `--admin`: Administration Spend (float)
- `--marketing`: Marketing Spend (float)
- `--state`: State location (e.g. `"New York"`, `"California"`, `"Florida"`)
- `--model`: Specific estimator to load: `linear`, `lasso`, or `ridge` (default: `ridge`)
- `--model-dir`: (Optional) Directory containing the model joblib files.
- `--model-path`: (Optional) Direct path to a specific model joblib file.

---

## **MODELS USED & ACCURACY**

Three regression algorithms are evaluated on the dataset:
- **Linear Regression**
- **Lasso Regression**
- **Ridge Regression**

### Model Scores
- **Training Accuracy (R²):** `0.9487` for all models.
- **Root Mean Square Error (RMSE):**
  - Linear Regression: `9085.1958`
  - Lasso Regression: `9083.8880`
  - Ridge Regression: `9052.1743` (Default model due to lowest RMSE)

### **CONCLUSION**
* All 3 regression algorithms used in this project are highly efficient for the given dataset.
* RMSE for Ridge Regression is least, making it the most optimal choice for deployment.

---

**Author** 

[Ayushi Shrivastava](https://github.com/ayushi424)
