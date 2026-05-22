# Bank Marketing Campaign Prediction with Random Forest

A comprehensive machine learning project that predicts bank marketing campaign outcomes using Random Forest classification, complete with data processing, PostgreSQL integration, and extensive model evaluation.

## 📊 Project Overview

This project analyzes bank marketing data to predict whether customers will subscribe to a term deposit based on various demographic and campaign-related features. The implementation includes data preprocessing, exploratory data analysis, feature engineering, model training with hyperparameter tuning, and comprehensive evaluation metrics.

## 🎯 Objective

Predict whether a customer will subscribe to a bank's term deposit (`yes`/`no`) based on:
- **Personal Information**: Age, job, marital status, education
- **Financial Data**: Account balance, housing loan, personal loan
- **Campaign Details**: Contact type, duration, number of contacts
- **Previous Campaign**: Outcome of previous marketing campaigns

## 🗂️ Dataset Information

The dataset contains **45,213 records** with **17 features**:

| Feature | Description | Type |
|---------|-------------|------|
| `age` | Customer age | Numerical |
| `job` | Type of job | Categorical |
| `marital` | Marital status | Categorical |
| `education` | Education level | Categorical |
| `default` | Has credit in default? | Categorical |
| `balance` | Average yearly balance | Numerical |
| `housing` | Has housing loan? | Categorical |
| `loan` | Has personal loan? | Categorical |
| `contact` | Contact communication type | Categorical |
| `day` | Last contact day of the month | Numerical |
| `month` | Last contact month of year | Categorical |
| `duration` | Last contact duration | Numerical |
| `campaign` | Number of contacts performed | Numerical |
| `pdays` | Number of days since last contact | Numerical |
| `previous` | Number of contacts before campaign | Numerical |
| `poutcome` | Outcome of previous campaign | Categorical |
| `y` | **Target**: Has subscribed to term deposit? | Binary |

## 🏗️ Project Structure

```
Random-Forest/
Bank_Marketing_Prediction_Random_Forest/
├── bank_marketing_prediction.ipynb
├── bank.csv
|── bank_sec.csv
└── README.md
```

## 🔧 Technical Implementation

### **Data Processing Pipeline**
- **Data Loading**: Custom CSV parser handling semicolon-separated values
- **Data Cleaning**: Removal of malformed records and handling missing values
- **Feature Engineering**: One-hot encoding for categorical variables
- **Database Integration**: PostgreSQL storage and retrieval system

### **Machine Learning Workflow**
1. **Exploratory Data Analysis**
   - Distribution analysis of numerical features
   - Categorical feature visualization
   - Correlation analysis
   - Target variable distribution

2. **Model Development**
   - Random Forest Classifier implementation
   - Train-test split (70/30)
   - Feature importance analysis
   - Cross-validation

3. **Hyperparameter Optimization**
   - RandomizedSearchCV for parameter tuning
   - Grid search for fine-tuning
   - Performance comparison across configurations

4. **Model Evaluation**
   - Accuracy, Precision, Recall, F1-Score
   - ROC Curve and AUC analysis
   - Confusion Matrix visualization
   - Feature importance ranking

## 📈 Model Performance

### **Key Metrics**
- **Model Type**: Random Forest Classifier
- **Number of Trees**: 100-500 (optimized)
- **Cross-validation**: 5-fold CV
- **Feature Engineering**: One-hot encoding for categorical variables

### **Evaluation Results**
- **Accuracy**: ~90%+ (actual results in notebook)
- **AUC Score**: ROC curve analysis included
- **Feature Importance**: Duration, balance, and age as top predictors
- **Confidence Intervals**: High, medium, and low confidence predictions

## 🛠️ Technologies Used

### **Core Libraries**
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning algorithms
- **matplotlib/seaborn**: Data visualization

### **Database**
- **PostgreSQL**: Data storage and retrieval
- **psycopg2**: PostgreSQL adapter for Python

### **Machine Learning**
- **Random Forest**: Primary classification algorithm
- **RandomizedSearchCV**: Hyperparameter optimization
- **Cross-validation**: Model validation

## 🚀 Getting Started

### **Prerequisites**
```bash
pip install pandas numpy scikit-learn matplotlib seaborn psycopg2-binary
```

### **Database Setup** (Optional)
1. Install PostgreSQL
2. Create database named `postgres`
3. Update database credentials in the notebook
4. Run database integration cells

### **Running the Project**
1. Clone the repository
2. Navigate to the `code/` directory
3. Open `code.ipynb` in Jupyter Notebook/Lab
4. Run cells sequentially for complete analysis

## 📊 Key Features

### **Data Analysis**
- ✅ Comprehensive EDA with visualizations
- ✅ Statistical summary and distribution analysis
- ✅ Correlation matrix and feature relationships
- ✅ Missing value analysis and handling

### **Machine Learning**
- ✅ Random Forest implementation with optimization
- ✅ Hyperparameter tuning with RandomizedSearchCV
- ✅ Feature importance analysis
- ✅ Cross-validation and model selection

### **Evaluation & Visualization**
- ✅ ROC Curve and AUC analysis
- ✅ Confusion matrix visualization
- ✅ Performance metrics dashboard
- ✅ Feature importance plots

### **Database Integration**
- ✅ PostgreSQL connection and data storage
- ✅ SQL query examples for data analysis
- ✅ Database retrieval and validation

## 📝 Usage Examples

### **Quick Prediction**
```python
# Load the trained model
rf_model.fit(X_train, y_train)

# Make predictions
predictions = rf_model.predict(X_test)
probabilities = rf_model.predict_proba(X_test)
```

### **Feature Importance**
```python
# Get top features
feature_importance = pd.DataFrame({
    'feature': X_train.columns,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)
```

## 🔍 Analysis Insights

The Random Forest model reveals several key insights:
- **Duration** of the last contact is the most important predictor
- **Balance** and customer **age** are significant factors
- **Previous campaign outcome** strongly influences current results
- **Contact method** and **timing** affect subscription likelihood

## 🎯 Business Applications

This model can be used for:
- **Targeted Marketing**: Focus on high-probability customers
- **Resource Optimization**: Allocate campaign resources effectively  
- **Customer Segmentation**: Identify customer personas
- **Campaign Strategy**: Optimize contact timing and methods

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📧 Contact

**Author**: Raghav  
**GitHub**: [@Raghav0079](https://github.com/Raghav0079)

---

⭐ **Star this repository** if you find it helpful for your machine learning projects!

*Built with ❤️ using Python, scikit-learn, and Random Forest*
