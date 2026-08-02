import os
import sys
import re
import joblib
from flask import Flask, render_template, request, jsonify

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__, static_folder='static', template_folder='templates')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'models', 'vectorizer.pkl')

# Load trained model and vectorizer
model = None
vectorizer = None

def load_artifacts():
    global model, vectorizer
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(VECTORIZER_PATH)
            print("Model and Vectorizer loaded successfully.")
        except Exception as e:
            print(f"Error loading artifacts: {e}")
    else:
        print("Model or vectorizer file missing. Please run `python train_model.py` first.")

load_artifacts()

def preprocess_text(text):
    """Normalizes input SMS text for model inference."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', ' urltoken ', text)
    text = re.sub(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', ' phonetoken ', text)
    text = re.sub(r'[\$£€₹]', ' moneytoken ', text)
    text = re.sub(r'[^a-z0-9\s_]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def analyze_triggers(raw_text):
    """Extracts suspicious indicators and risk keywords for explainability."""
    triggers = []
    
    # Check for URLs
    if re.search(r'https?://\S+|www\.\S+|bit\.ly|\.info|\.xyz|\.top|\.net|\.site|\.org', raw_text, re.IGNORECASE):
        triggers.append({"type": "Suspicious Link", "desc": "Contains an external link or shortened domain URL."})
        
    # Check for monetary amounts or currency
    if re.search(r'[\$£€₹]|\b\d+\s*(dollars|usd|cash|bonus|prize|reward|gift card)\b', raw_text, re.IGNORECASE):
        triggers.append({"type": "Monetary Incentive", "desc": "References money, cash prizes, gift cards, or financial incentives."})
        
    # Check for urgency words
    urgency_terms = ['urgent', 'immediately', 'final warning', 'action required', 'suspended', 'locked', 'compromised', 'expire', 'cut off', 'arrest']
    found_urgency = [w for w in urgency_terms if re.search(r'\b' + re.escape(w) + r'\b', raw_text, re.IGNORECASE)]
    if found_urgency:
        triggers.append({"type": "Urgent Language", "desc": f"Uses high-pressure words: {', '.join(found_urgency[:3])}."})
        
    # Check for credential / account requests
    cred_terms = ['verify', 'password', 'login', 'kyc', 'social security', 'ssn', 'account', 'credit card', 'banking']
    found_cred = [w for w in cred_terms if re.search(r'\b' + re.escape(w) + r'\b', raw_text, re.IGNORECASE)]
    if found_cred:
        triggers.append({"type": "Account Verification Request", "desc": f"Asks for account or security credentials ({', '.join(found_cred[:3])})."})

    return triggers

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or vectorizer is None:
        load_artifacts()
        if model is None or vectorizer is None:
            return jsonify({
                'status': 'error',
                'message': 'Model is not loaded. Please run `train_model.py` to generate the model artifacts.'
            }), 500

    # Handle JSON and Form Data
    if request.is_json:
        data = request.get_json()
        message = data.get('message', '')
    else:
        message = request.form.get('message', '')

    message = message.strip()
    if not message:
        return jsonify({
            'status': 'error',
            'message': 'Please enter an SMS text message to analyze.'
        }), 400

    clean_msg = preprocess_text(message)
    features = vectorizer.transform([clean_msg])
    
    prediction_code = int(model.predict(features)[0]) # 1 = Scam, 0 = Safe
    
    # Calculate probability score if model supports predict_proba
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(features)[0]
        scam_prob = float(proba[1])
        confidence_percent = round(scam_prob * 100, 1)
    else:
        scam_prob = 1.0 if prediction_code == 1 else 0.0
        confidence_percent = 95.0 if prediction_code == 1 else 5.0

    is_scam = bool(prediction_code == 1)
    
    # Determine risk tier
    if scam_prob >= 0.75:
        risk_level = "High Scam Risk"
        risk_badge = "critical"
    elif scam_prob >= 0.50:
        risk_level = "Moderate Scam Risk"
        risk_badge = "warning"
    elif scam_prob >= 0.25:
        risk_level = "Low Risk / Precaution Needed"
        risk_badge = "caution"
    else:
        risk_level = "Safe / Legitimate"
        risk_badge = "safe"

    triggers = analyze_triggers(message)

    return jsonify({
        'status': 'success',
        'is_scam': is_scam,
        'prediction': 'SCAM' if is_scam else 'SAFE',
        'confidence_score': confidence_percent,
        'risk_level': risk_level,
        'risk_badge': risk_badge,
        'triggers': triggers,
        'original_message': message
    })

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1')
    print("Starting Scam SMS Detector Flask App at http://127.0.0.1:5000")
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
