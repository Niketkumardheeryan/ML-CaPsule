## **Startup Profit Prediction**
**GOAL**

The goal of this project is to analyse and predict profit of a startup  from features as 'R&D Spend', 'Administration', 'Marketing Spend', 'State' etc.

**DATASET**

Dataset can be loaded using opendatasets module.
Steps to create a Kaggle API to use the dataset.
- Step 1: Go to https://kaggle.com and login with your ID.
- Step 2: Then nagivate to settings->API Tokens.
- Step 3: Click Create Legacy API Key and download the kaggle.json
- Step 4: Run the ipynb file and Enter the username and API key from the downloaded kaggle.json

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

This contribution enhances the original notebook while preserving its workflow.

### Features Added

- Added Joblib serialization for trained machine learning models.
- Models can now be saved and reused without retraining.
- Added automatic dataset download from Kaggle using the `opendatasets` library.
- Improved notebook documentation with detailed markdown explanations for every major step.
- Executed all notebook cells with outputs displayed for better reproducibility.

### Benefits

- Faster inference by reusing serialized models.
- Eliminates unnecessary retraining.
- Automatically downloads the dataset from Kaggle when running the notebook.
- Improves maintainability and reproducibility.
- Makes the notebook easier to understand and ready for future deployment.

### Additional Contribution

- Joblib model serialization and reusable model workflow.
- Automatic Kaggle dataset download using `opendatasets`.
- Enhanced notebook documentation with step-by-step explanations.
- Notebook executed end-to-end with all outputs displayed.

**Author**

[Ayushi Shrivastava](https://github.com/ayushi424)
