# Loan-Prediction
A machine learning model designed to predict whether a loan application will be approved or rejected based on the applicant's personal information and credit history. The model utilizes a dataset containing historical loan application data to train and validate its predictions. 
## Dataset: 
The dataset used for training and testing the model consists of various features that include:
1. Personal information such as gender, marital status, dependents, education, self-employed, and property area.
2. Financial information such as applicant income, co-applicant income, and credit history.
3. Loan-specific details such as loan amount, and loan term.
4. Target variable indicating whether the loan was approved or rejected.
## Dependencies: 
Libraries used: Numpy, Pandas, Matplotlib, missingno, seaborn, scipy, sklearn.
## Visualization:
To gain insights into the dataset before building the model, I tried to visualize the model using some plots like:</br>
BarPlot(): I have plotted the crosstab for each class with the loan prediction class(output). </br>
Histplot(): Showing the distribution of the dataset. </br>
Heatmap(): Checked if our attributes are codependent on one another. If were so, we could have simply used any one of them but all our attributes are independent.</br>
Crosstab(): We observed that loan status is not dependent on gender since we have an almost equal ratio for male and female.</br>
Boxplot(): We observed that we have outliers that need to be taken care of.</br>
## Data Preprocessing
Treating NaN values: For the categorical attributes I used 'mode' to fill in the empty cells and for the numerical values, 'mean' was used.</br>
Treating Outliers: We simply dropped the values that were not in the range. </br>
SMOTE(): Increasing the data for the minority class.</br>
MinMaxScaler: Linearly scales them down into a fixed range. </br>
## Model Training
1. Linear Regression: Accuracy- 92.59%
2. KNN: Best Accuracy- 90.74%
3. SVC: Accuracy- 92.59%
4. Decision Tree: Best Accuracy- 92.59%
5. Random Forest: Best accuracy- 92.59%
6. Gradient Boosting: Best Accuracy- 85.19%
#### Finally I used MaxVoting to ensemble all the models and got final accuracy of 92.59%.

## After running app.py file
![image](https://github.com/sanskritiagr/ML-CaPsule/assets/96240350/71ff508e-7277-40b2-82e0-e7854b7c7b34)

