# Parkinsons-detection
This project aims to Find a model with good metrics to identify if a person has Parkinson's disease.

<h2>Data set</h2>

  <i> this parkinsons dataset is taken from the Kaggle UCI dataset, which contains 24 features and 195 instances </i>


<h2>dataset description</h2>
name - ASCII subject name and recording number

MDVP:Fo(Hz) - Average vocal fundamental frequency

MDVP:Fhi(Hz) - Maximum vocal fundamental frequency

MDVP:Flo(Hz) - Minimum vocal fundamental frequency

MDVP:Jitter(%) , MDVP:Jitter(Abs) , MDVP:RAP , MDVP:PPQ , Jitter:DDP - Several measures of variation in fundamental frequency

MDVP:Shimmer , MDVP:Shimmer(dB) , Shimmer:APQ3 , Shimmer:APQ5 , MDVP:APQ , Shimmer:DDA - Several measures of variation in amplitude

NHR , HNR - Two measures of ratio of noise to tonal components in the voice

status - Health status of the subject (one) - Parkinson's, (zero) - healthy

RPDE , D2 - Two nonlinear dynamical complexity measures

DFA - Signal fractal scaling exponent

spread1 , spread2 , PPE - Three nonlinear measures of fundamental frequency variation

<h2>steps to implement</h2>
<b>EDA:</b><p>checking the description of the data and data types of features, checking any missing value(not found), and found data imbalance between healthy and non-effected instances </p>
<b>data balancing: </b><p>To balance data imbalance here SMOTE enn (undersampling technique ) is used</p>
<b>Feature selection:</b><p> Select k-best and using the chi-square test is used and select the top 20 features</p>
<b>test-train-split : </b><p>data is divided in 80:20 ratio</p>
<b>hyperparameter tuning :</b><p>tuned parameters using Randomized search</p>
<b>Classifiers :</b><li><i>K-Nearest Neighbour</i> </li>  
<li>  <i>Random Forest classifier</i></li>
<li> <i>Decision Tree classifier</i></li> 
<b>Metrics:</b><p>5 metrics are used to predict the best model - Accuracy Score, Precision , Recall, F1 Score , time taken to train and predict</p>

<b>Results : </b>
<i>Random Forest Classifier showed best results by giving 100% in all metrics </i>
<table>
  <tr>
    <td>classifier</td>
    <td>accuracy_score</td>
    <td>precision</td>
    <td>recall </td>
    <td>f1 score</td>
    <td>time taken</td>
  </tr>
  <tr>
    <td>Knn</td>
    <td>97.7%</td>
    <td>100%</td>
    <td>94.1%</td>
    <td>96.9%</td>
    <td>0.05sec</td>
  </tr>
   <tr>
    <td>Random forest</td>
    <td>100%</td>
    <td>100%</td>
    <td>100%</td>
    <td>100%</td>
    <td>0.1sec</td>
  </tr>
   <tr>
    <td>Decision Tree</td>
    <td>93.1%</td>
    <td>100%</td>
    <td>82.3%</td>
    <td>90%</td>
    <td>0.0sec</td>
  </tr>
</table>
