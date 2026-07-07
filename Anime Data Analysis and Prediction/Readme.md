## Title: Anime Data Analysis and Prediction

## Goal: To analyze the Anime Dataset using Exploratory Data Analysis using several parameters and then try to make predictions

## Dataset link:
https://www.kaggle.com/datasets/ayush4807/aad-dataset

## Techniques used: 
1. Data Filtering
2. Data Preprocessing
3. Data Extraction
4. Data visualization
5. Data Modelling
6. Pickling the model

## Libraries used:
1. Pandas
2. Pandas profiling
3. Numpy 
4. Matplotlib
5. Scikit Learn
6. Pickle

## Data visuals created:
1. Hsitogram
2. Box plot
3. Scatter Plot
4. Bar plot
5. Heatmap
6. Pairplot

## Machine Learning Models used:
1. Linear Regression
2. Decsion Tree Regression
3. Random Forest Regressor

## Evaluation metrics used:
1. Root Mean Squared error
2. Mean Squared error
3. R2 score
4. Training Score

## Visuals:
<img src = "https://github.com/PiyushBL45t/ML-Crate/blob/main/Anime%20Data%20Analysis%20and%20Prediction/Images/Box%20plot%20pr%20year.png"/>
<img src = "https://github.com/PiyushBL45t/ML-Crate/blob/main/Anime%20Data%20Analysis%20and%20Prediction/Images/Heatmap.png"/>
<img src = "https://github.com/PiyushBL45t/ML-Crate/blob/main/Anime%20Data%20Analysis%20and%20Prediction/Images/Histograms.png"/>
<img src = "https://github.com/PiyushBL45t/ML-Crate/blob/main/Anime%20Data%20Analysis%20and%20Prediction/Images/Normal%20Distributions.png"/>
<img src = "https://github.com/PiyushBL45t/ML-Crate/blob/main/Anime%20Data%20Analysis%20and%20Prediction/Images/Pairplot.png"/>

## Conclusion
### We tried to implement three model on our analyzed data. 
#### 1. Linear Regression
#### 2. Decision Tree Regressor
#### 3. Random Forest Regressor

### This was a continuous data thus, we applied the Regression Algorithms for this purpose.
### The training paramter was "Rating": This depicts the Anime ratings on scale of 10. We trained and tested our model with two random types of Anime Genres: 
#### 1. Animation, Adventure, Drama
#### 2. Animation, Comedy, Fantasy
## Results say that:
### 1. Linear Regression and Random Forest Algorithms show a very low training score and a high error values and due to which they are not the best fit models. The predictions of <u>Ratings</u> based on those models is also very low for the future years.
### 2. The Decision Tree on the other hand makes a very good predictions of ratings and we can say that the type of Animes we selected can catch more attention of audiences in the coming years. The evaluation metrics are stable and error results are very low this makes it fit to create a good predictive analysis example.

## Authors

- Created by [@Priyankesh](https://github.com/priyankeshh), GSSoC 2024
