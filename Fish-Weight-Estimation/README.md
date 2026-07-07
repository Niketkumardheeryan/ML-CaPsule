# Fish Weight Estimation


![](https://img.shields.io/badge/Programming_Language-Python-blue.svg)
![](https://img.shields.io/badge/Main_Tool_Used-Jupyter_Notebook-orange.svg)
![](https://img.shields.io/badge/Status-Complete-green.svg)

Abstract:A fish market is a marketplace for selling fish and fish products. It can be dedicated to wholesale trade between fishermen and fish merchants, or to the sale of seafood to individual consumers, or to both. Retail fish markets, a type of wet market, often sell street food as well.

Our Aim is to estimate fish weight on the basis of some measurement of fish body structure

>Steps or Stages:
- Download and preliminary analysis of data

- Linear Regression

- Multiple Regression

- Random Forest Regression

- XGB Regression

- DNN

- Comparison between all models

- Visualization and results of best model

>Prerequisites:
- Python

- Pandas

- Statistics

- NumPy

- Matplotlib

- Keras

- Scikit-Learn

- Tensorflow

Dataset:https://www.kaggle.com/aungpyaeap/fish-market

About: We are  taking train:test = 7:3.

>Results :
- R2 score Length1 and Weight linear regression:                   53.565

- R2 score Height and Weight linear regression:                    29.536

- R2 score Width and Weight linear regression:                     76.911

- R2 score Length1,Length2,Length3 and Weight multiple regression: 77.975

- R2 score Width,Length1,Height and Weight multiple regression:    63.085

- R2 score Width,Height and Weight multiple regression:            66.866

- R2 score Using Random Forest Regression for Weight:               80.996

- R2 score Using XGBRegressor for Weight:                           92.750

- R2 score Using DNN for Weight:                                    95.975

>Visualiztion for DNN:

>Cross section length:

![alt text](https://github.com/shivam-s16/Fish-Weight-Estimation/blob/main/results/cross.png)

>Diagonal length:

![alt text](https://github.com/shivam-s16/Fish-Weight-Estimation/blob/main/results/diagonal.png)

>Vertical Length:

![alt text](https://github.com/shivam-s16/Fish-Weight-Estimation/blob/main/results/vertical.png)

>Height:

![alt text](https://github.com/shivam-s16/Fish-Weight-Estimation/blob/main/results/height.png)

>Width:

![alt text](https://github.com/shivam-s16/Fish-Weight-Estimation/blob/main/results/width.png)



<h3 align="center">Made by Shivam Saxena &nbsp;❤️&nbsp;</h3>
