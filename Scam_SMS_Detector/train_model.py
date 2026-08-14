import os
import sys
import re
import joblib
import pandas as pd
import numpy as np

# Force UTF-8 stdout encoding on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

def preprocess_text(text):
    """
    Normalizes and cleans input SMS text for NLP training and prediction.
    """
    if not isinstance(text, str):
        return ""
    # Convert to lowercase
    text = text.lower()
    # Normalize URLs, phone numbers, and currency symbols as special tokens
    text = re.sub(r'https?://\S+|www\.\S+', ' urltoken ', text)
    text = re.sub(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', ' phonetoken ', text)
    text = re.sub(r'[\$£€₹]', ' moneytoken ', text)
    # Remove non-alphanumeric characters except space and tokens
    text = re.sub(r'[^a-z0-9\s_]', ' ', text)
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def train_and_evaluate():
    print("=" * 60)
    print(" 🚀 SCAM SMS DETECTOR - MODEL TRAINING PIPELINE")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, 'data', 'sms_spam_collection.csv')
    models_dir = os.path.join(base_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")

    print(f"📂 Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    print(f"📊 Dataset size: {len(df)} samples")
    print(f"   - Ham (Safe): {sum(df['label'] == 'ham')}")
    print(f"   - Spam (Scam): {sum(df['label'] == 'spam')}")

    # Preprocess text
    print("\n🧹 Preprocessing text messages...")
    df['clean_message'] = df['message'].apply(preprocess_text)
    df['binary_label'] = df['label'].apply(lambda x: 1 if x == 'spam' else 0)

    # Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        df['clean_message'],
        df['binary_label'],
        test_size=0.2,
        random_state=42,
        stratify=df['binary_label']
    )

    print(f"\n✂️  Split dataset: {len(X_train)} training samples, {len(X_test)} test samples")

    # TF-IDF Vectorizer
    print("\n🔤 Extracting TF-IDF Features...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=3000,
        sublinear_tf=True
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Candidate Models
    models = {
        'Multinomial Naive Bayes': MultinomialNB(alpha=0.1),
        'Logistic Regression': LogisticRegression(max_iter=1000, C=1.0, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
    }

    best_model = None
    best_f1 = -1.0
    best_model_name = ""

    print("\n🤖 Training and Evaluating Models...")
    print("-" * 60)

    for name, model in models.items():
        model.fit(X_train_tfidf, y_train)
        y_pred = model.predict(X_test_tfidf)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        print(f"📌 {name}:")
        print(f"   - Accuracy:  {acc:.4f}")
        print(f"   - Precision: {prec:.4f}")
        print(f"   - Recall:    {rec:.4f}")
        print(f"   - F1-Score:  {f1:.4f}")

        if f1 > best_f1:
            best_f1 = f1
            best_model = model
            best_model_name = name

    print("-" * 60)
    print(f"🏆 Best Model Selected: {best_model_name} (F1-Score: {best_f1:.4f})")

    # Final evaluation of best model
    y_pred_best = best_model.predict(X_test_tfidf)
    print("\n📋 Detailed Classification Report for Best Model:")
    print(classification_report(y_test, y_pred_best, target_names=['Safe (Ham)', 'Scam (Spam)']))

    print("🧩 Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred_best)
    print(f"   TN: {cm[0][0]} | FP: {cm[0][1]}")
    print(f"   FN: {cm[1][0]} | TP: {cm[1][1]}")

    # Save model and vectorizer
    model_save_path = os.path.join(models_dir, 'model.pkl')
    vectorizer_save_path = os.path.join(models_dir, 'vectorizer.pkl')

    joblib.dump(best_model, model_save_path)
    joblib.dump(vectorizer, vectorizer_save_path)

    print(f"\n💾 Model saved to: {model_save_path}")
    print(f"💾 Vectorizer saved to: {vectorizer_save_path}")
    print("\n✅ Model training completed successfully!")

if __name__ == '__main__':
    train_and_evaluate()
