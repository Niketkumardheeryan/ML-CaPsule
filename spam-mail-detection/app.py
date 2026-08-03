import os
import pickle
import string
from flask import Flask, render_template, request, jsonify
import nltk
from nltk.corpus import stopwords

app = Flask(__name__)

# --- NLTK Data and preprocessing ---
nltk.download('stopwords', quiet=True)
STOPWORDS = stopwords.words('english')

def message_text_process(mess):
    """Remove punctuation and stop words; must exactly match save_model.py / training notebook."""
    no_punctuation = [char for char in mess if char not in string.punctuation]
    no_punctuation = ''.join(no_punctuation)
    return [word for word in no_punctuation.split() if word.lower() not in STOPWORDS]

# --- Load model ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'Model', 'spam_model.pkl')
if not os.path.exists(MODEL_PATH):
    # Try lowercase model folder
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'spam_model.pkl')

model = None
model_error = None

try:
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
    else:
        model_error = "Model file not found. Please run model/save_model.py first."
except Exception as e:
    model_error = f"Error loading model: {str(e)}"

@app.route('/')
def index():
    """Render main interface"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Predict path endpoint"""
    if model is None:
        return jsonify({
            'error': model_error or "Prediction model is currently unavailable."
        }), 500
        
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Invalid request metadata. Missing message field.'}), 400
            
        user_input = data['message']
        if not user_input.strip():
            return jsonify({'error': 'Message content cannot be empty.'}), 400
            
        # Perform prediction
        prediction = model.predict([user_input])[0]
        
        response = {
            'prediction': prediction.lower()
        }
        
        # Add confidence metrics if available
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba([user_input])[0]
            classes = model.classes_
            proba_dict = dict(zip(classes, proba))
            
            # Map classes ensuring safe conversion to percentage values
            ham_score = float(proba_dict.get('ham', proba_dict.get('Ham', 0)))
            spam_score = float(proba_dict.get('spam', proba_dict.get('Spam', 0)))
            
            response['confidence'] = {
                'ham': ham_score,
                'spam': spam_score
            }
            
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f"Prediction failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
