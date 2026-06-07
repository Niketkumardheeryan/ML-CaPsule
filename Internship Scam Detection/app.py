import os
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

try:
    model = joblib.load(os.path.join(os.path.dirname(__file__), 'models', 'model.pkl'))
    pipeline = joblib.load(os.path.join(os.path.dirname(__file__), 'models', 'pipeline.pkl'))
    print("Models loaded successfully")
except Exception as e:
    print(f"Model loading failed: {e}")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    df = pd.DataFrame([data])
    for col in df.select_dtypes(include=['int64']).columns:
        df[col] = df[col].astype('float64')
    
    features = pipeline.transform(df)
    
    # Calculate the confidence score
    prob = model.predict_proba(features)[0][1]

    flags = []
    if data.get('payment_required') == 1:
        flags.append('Payment required for an internship')
    if data.get('recruiter_email_type') == 'Free':
        flags.append('Recruiter uses a free email domain (e.g., Gmail, Yahoo)')
    if data.get('website_available') == 0:
        flags.append('No official company website provided')

    return jsonify({
        'is_spam': bool(prob > 0.5),
        'spam_probability': float(prob),
        'flags': flags,
        'note': 'Analyzed by ML Pipeline'
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)