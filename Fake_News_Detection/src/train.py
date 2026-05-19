import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from preprocess import preprocess_text

def train_model():
    print("Loading datasets...")
    # Load fake and true datasets
    fake_path = os.path.join(os.path.dirname(__file__), '../data/Fake.csv')
    true_path = os.path.join(os.path.dirname(__file__), '../data/True.csv')
    
    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)
    
    # Assign labels (0 for Fake, 1 for True)
    fake_df['label'] = 0
    true_df['label'] = 1
    
    # Combine and shuffle
    df = pd.concat([fake_df, true_df], axis=0).reset_index(drop=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    print(f"Total dataset size: {len(df)} rows")
    
    print("Preprocessing text...")
    # Combine title and text for better context
    df['full_text'] = df['title'] + " " + df['text']
    
    # Apply preprocessing
    df['cleaned_text'] = df['full_text'].apply(preprocess_text)
    
    # Define features and target
    X = df['cleaned_text']
    y = df['label']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Extracting features (TF-IDF)...")
    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(max_features=5000)
    
    # Fit and transform training data, transform test data
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print("Training Logistic Regression model...")
    # Initialize and train model
    model = LogisticRegression()
    model.fit(X_train_tfidf, y_train)
    
    print("Evaluating model...")
    # Make predictions
    y_pred = model.predict(X_test_tfidf)
    
    # Print metrics
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # Save the model and vectorizer
    models_dir = os.path.join(os.path.dirname(__file__), '../models')
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'model.pkl')
    vectorizer_path = os.path.join(models_dir, 'vectorizer.pkl')
    
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    print(f"\nModel saved to {model_path}")
    print(f"Vectorizer saved to {vectorizer_path}")

if __name__ == "__main__":
    train_model()
