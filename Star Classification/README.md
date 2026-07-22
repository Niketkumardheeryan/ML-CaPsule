## Star Classification using Machine Learning

### Project Title: Stellar Type Classification System

#### Dataset Used: *Star Classification Dataset (Kaggle)*

The dataset contains physical characteristics of stars including temperature, luminosity, radius, absolute magnitude, spectral class, and color. Stars are classified into 6 stellar types: Brown Dwarf, Red Dwarf, White Dwarf, Main Sequence, Supergiant, and Hypergiant.

### Features

- Data preprocessing and cleaning (handling missing values, outliers, encoding)
- Exploratory Data Analysis (EDA) with visualizations
- Feature engineering and correlation analysis
- Model comparison using multiple classification algorithms
- Performance evaluation using accuracy, precision, recall, F1-score, and confusion matrix
- Prediction examples with sample inputs
- Well-documented Jupyter Notebook
- README with results and conclusions

### Libraries Required

```
numpy
pandas
matplotlib
seaborn
scikit-learn
xgboost
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Algorithms Used

- **Logistic Regression** - Linear model for multiclass classification
- **Decision Tree** - Tree-based classifier with interpretability
- **Random Forest** - Ensemble method reducing overfitting
- **Support Vector Machine (SVM)** - Kernel-based classifier for complex boundaries
- **K-Nearest Neighbors (KNN)** - Instance-based learning algorithm
- **XGBoost** - Gradient boosting classifier for high performance

### Steps to Implement

1. Load the dataset and perform initial exploration
2. Handle missing values and outliers
3. Encode categorical features (spectral class, color)
4. Perform EDA with correlation heatmaps, distribution plots, and pair plots
5. Split data into training and testing sets
6. Train multiple classification models
7. Evaluate models using accuracy, precision, recall, F1-score
8. Plot confusion matrices for each model
9. Compare model performances and select the best one
10. Make predictions on sample data

### Expected Results

| Model | Accuracy |
|-------|----------|
| Logistic Regression | ~95% |
| Decision Tree | ~97% |
| Random Forest | ~98% |
| SVM | ~96% |
| KNN | ~94% |
| XGBoost | ~98% |

### Conclusion

Random Forest and XGBoost achieve the highest accuracy for star classification. The project demonstrates an end-to-end supervised learning workflow for multiclass classification on a real-world astronomy dataset.

### Author

Contributed under GSSoC'26

### License

This project is licensed under the MIT License.
