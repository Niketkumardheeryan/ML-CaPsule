# importing necessary Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib


# Loading your dataset
data_path = r"dataset/BBC_News_Train.csv"

data = pd.read_csv(data_path)
# text/news articles
X = data['Text']
# target category
y = data['Category']


# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# creating a pipeline with vectorizer and classifier
model_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_df=0.7)),
    ('classifier', LogisticRegression())
])

# Training the model
model_pipeline.fit(X_train, y_train)

# Evaluating the model
accuracy = model_pipeline.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Export the model and vectorizer using joblib
joblib.dump(model_pipeline, 'news_category_prediction.pkl')
print("Model exported as news_category_prediction.pkl")