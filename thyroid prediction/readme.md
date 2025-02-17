# **Thyroid Disease Detection using Machine Learning**  

## **GOAL**  
The goal of this project is to develop a machine learning model that can accurately predict  recurrence of well differentiated thyroid cancer. The project involves **data preprocessing, feature selection, and classification models** to identify the best approach for thyroid disease detection.  

Dataset can be downloaded from [here](https://www.kaggle.com/sudhanshu8897/thyroid-disease-dataset).  

---

## **MODELS USED**  
- Logistic Regression  
- Support Vector Machine (SVM)  
- Decision Trees  
- Random Forest  

---

## **LIBRARIES NEEDED**  
- numpy  
- pandas  
- seaborn  
- matplotlib  
- scikit-learn  

---

## **STEPS BEING FOLLOWED**  

1. Load the dataset  
2. Import libraries  
3. Data Visualization  
4. Data Preprocessing (handling missing values, outliers, and scaling)  
5. Splitting data into training and testing sets
6. Feature Selection Techniques:  
   - Principal Component Analysis (PCA)   
   - Mutual Information  
   - Recursive Feature Elimination with Cross-Validation (RFECV)
7. Model training using different classification algorithms  
8. Model evaluation using accuracy, precision, recall, F1-score, and AUC-ROC  
9. Comparison of models based on performance and training time  

---

## **CONCLUSION : Best Accuracy of Each Model**  

By using Logistic Regression:  
```  
Accuracy: 95.41%
Feature Selection Technique:PCA  
```  

By using Random Forest:  
```  
Accuracy: 98.26%
Feature Selection Technique:MutualInfo
```   

By using Support Vector Machine (SVM):  
```  
Accuracy: 95.11%
Feature Selection Technique:PCA
``` 

By using Decision Trees:  
```  
Accuracy: 93.91%
Feature Selection Technique:MutualInfo
``` 

---