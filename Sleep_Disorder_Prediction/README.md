# Sleep Disorder and Stress Level Prediction

## Dataset
- **Source:** Sleep Health and Lifestyle Dataset
- The notebook downloads the dataset as `dataset.csv` via `gdown`:
- **Link:** `https://drive.google.com/file/d/1DfJ6M4WU_yjlOk-_lZg2JCaWHlaszH6U/view?usp=drive_link`

This project analyzes sleep data and lifestyle factors to predict potential sleep disorders and stress levels. Using machine learning techniques (Random Forest), the study explores the correlation between physical activity, sleep duration, and overall health to build a robust predictive model.

## Key Features
1. Comprehensive Exploratory Data Analysis (EDA) on lifestyle factors.
2. Correlation analysis between sleep duration, heart rate, and stress.
3. Data preprocessing and categorical encoding.
4. Machine Learning model building using Random Forest Classifier.
5. Model evaluation and performance metrics generation.

## Tech Stack
- Python
- Pandas, NumPy
- Matplotlib, Seaborn (visualization)
- Scikit-learn (Machine Learning & preprocessing)
- gdown (dataset download)

## Usage
1. Clone the repository and navigate to the project directory.
2. Open `sleep_disorder_analysis.ipynb` in Jupyter Notebook, VS Code, or Google Colab.
3. Run all cells (requires `gdown` to download `dataset.csv`).
4. Review the generated visualizations and the final model accuracy.