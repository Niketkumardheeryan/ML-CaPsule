## **Startup Profit Prediction**
**GOAL**

The goal of this project is to analyse and predict profit of a startup  from features as 'R&D Spend', 'Administration', 'Marketing Spend', 'State' etc.

**DATASET**

Dataset can be downloaded from [here](https://www.kaggle.com/sonalisingh1411/startup50).

**WHAT I HAD DONE**
- Step 1: Data Exploration
- Step 2: Data Preparation
- Step 3: Data Training
- Step 4: Model Creation
- Step 5: Performance Check


**MODELS USED**
-  Linear Regression
-  Lasso Regression
-  Ridge Regression

**LIBRARIES NEEDED**
- pandas
- numpy
- sklearn (For data training, importing models and performance check)

**Accuracy of different models used**
- By using Linear Regression model 
 ```python
    Accuracy achieved :  94.87
 ``` 
 - By using Lasso Regression model 
 ```python
    Accuracy achieved :  94.87
 ``` 
  - By using Ridge Regression model 
 ```python
    Accuracy achieved :  94.87
 ```

**CONCLUSION**

* All 3 regression algorithms used in this project are equally efficient for the given dataset.
* RMSE for Ridge Regression is least

---

## Additional Feature Added

### Joblib Model Serialization

This contribution adds support for serializing the trained machine learning models using **Joblib** while preserving the original notebook workflow.

### Features Added

- Added Joblib serialization for trained models.
- Models can now be saved and reused without retraining.
- Improved notebook documentation with descriptive markdown cells.
- Executed all notebook cells with outputs displayed for better reproducibility.

### Benefits

- Faster inference.
- Eliminates unnecessary retraining.
- Improves maintainability.
- Makes the notebook easier to understand and ready for future deployment.

**Author** 

[Ayushi Shrivastava](https://github.com/ayushi424)
