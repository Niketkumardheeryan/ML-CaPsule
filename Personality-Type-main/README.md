## Personality Types Predictor

*Personality* is a fundamental basis of human behavior, it affects the interaction and preferences of an individual. *Social networks* have become a prominent platform for opinions and thoughts, this indicated that there is a strong correlation between the personality of users and the way they behave on social networks. 

In this work we explore the use of **Machine Learning** techniques to infer **personality traits** of a user from Facebook status updates. 

For **personality recognition**, the models were trained for each of the five personality traits, given by the **Big-5** personality classification, using **LIWC** (Linguistic Inquiry and Word Count) characteristics and were compared different classification methods, such as *Logistic Regression, RandomForestClassifier, Mul tinomialNB, GradientBoostingClassifier, SVC, LinearRegression, Ridge,SGDRegressor*; the performance of the systems was measured using precision.

### Requeriments
Run the following commands if you don't have them already:

```
pip install streamlit
pip install nltk
pip install Flask
pip install bson
pip install scikit-learn
pip install numpy
pip install os-sys
pip install scipy
pip install pandas
pip install matplotlib
pip install liwc
pip install selenium
```
To install it all:
```
pip install requeriments.txt
```

### Documentation
For a more in-depth documentation read [here](https://github.com/dayfundora/Personality-Type/blob/9b1755003480280821d40af5041032f1e07a854c/doc/report.pdf)

### Download
If you want to download this project to work on it, you will need the models for each aspect of the personality, both for LIWC and TFIDF.
```
AGR_categorical_model_liwc.pkl
AGR_categorical_model_tfidf.pkl
CON_categorical_model_liwc.pkl
CON_categorical_model_tfidf.pkl
EXT_categorical_model_liwc.pkl
EXT_categorical_model_tfidf.pkl
NEU_categorical_model_liwc.pkl
NEU_categorical_model_tfidf.pkl
OPN_categorical_model_liwc.pkl
OPN_categorical_model_tfidf.pkl
```
You can send me an email [here](mailto:dayfundoraglez@gmail.com) or write me [here](t.me/AGirlHas_No_Name)
