import joblib
import os
from preprocess import preprocess_text

def predict_fake_news(text):
    models_dir = os.path.join(os.path.dirname(__file__), '../models')
    model_path = os.path.join(models_dir, 'model.pkl')
    vectorizer_path = os.path.join(models_dir, 'vectorizer.pkl')
    
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        print("Model or vectorizer not found. Please run train.py first.")
        return
        
    # Load model and vectorizer
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    
    # Preprocess the input text
    cleaned_text = preprocess_text(text)
    
    # Transform using TF-IDF
    tfidf_text = vectorizer.transform([cleaned_text])
    
    # Predict
    prediction = model.predict(tfidf_text)[0]
    probability = model.predict_proba(tfidf_text)[0]
    
    label = "Real" if prediction == 1 else "Fake"
    confidence = probability[prediction] * 100
    
    print(f"\nNews Text: '{text}'")
    print(f"Prediction: {label} News (Confidence: {confidence:.2f}%)")

if __name__ == "__main__":
    sample_texts = [
        "Local man discovers a way to turn lead into gold in his garage using baking soda.",
        "The city council approved the new budget for public schools for the upcoming year."
    ]
    
    print("Testing model predictions...")
    for text in sample_texts:
        predict_fake_news(text)
