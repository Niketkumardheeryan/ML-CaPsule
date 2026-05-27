import pandas as pd
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

def train():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'songs_dataset.csv')
    model_path = os.path.join(base_dir, 'data', 'intent_model.joblib')
    
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    # We only need User_Text and Sentiment_Label for the AI model
    df_train = df[['User_Text', 'Sentiment_Label']].dropna()
    
    X = df_train['User_Text']
    y = df_train['Sentiment_Label']
    
    # Simple Pipeline: TF-IDF -> Logistic Regression
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=1000)),
        ('clf', LogisticRegression(random_state=42, max_iter=200))
    ])
    
    print("Training model...")
    pipeline.fit(X, y)
    
    # Simple evaluation on training data
    predictions = pipeline.predict(X)
    print("Training Report:")
    print(classification_report(y, predictions))
    
    print(f"Saving model to {model_path}...")
    joblib.dump(pipeline, model_path)
    print("Model saved successfully!")

if __name__ == "__main__":
    train()
