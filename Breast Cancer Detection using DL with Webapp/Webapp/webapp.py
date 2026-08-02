import os
import time
import logging
from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.security import safe_join
import numpy as np
import cv2
import tensorflow as tf
from werkzeug.exceptions import NotFound

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Load the VGG16 model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "..", "Model", "model.keras")
# if not os.path.exists(model_path):
#     raise FileNotFoundError(f"The model file {model_path} does not exist.")
logging.info(f"Loading VGG16 model from {model_path}")
model = None

try:
    if os.path.exists(model_path):
        model = tf.keras.models.load_model(model_path)
        logging.info("VGG16 model loaded successfully.")
    else:
        logging.warning("Model file not found. Running app without prediction model.")
except Exception as e:
    logging.error(f"Error loading model: {e}")

def prepare_image(image, target_size=(300, 300)):
    try:
        # Convert to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Resize the image
        image = cv2.resize(image, target_size)
        # Scale the image
        image = image / 255.0
        # Expand dimensions to match the model input
        image = np.expand_dims(image, axis=0)
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=-1)
        return image
    except Exception as e:
        logging.error(f"Error preparing image: {e}")
        raise

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return "No file part"
    
    file = request.files['image']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        try:
            # Read the image
            image = np.frombuffer(file.read(), np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            
            # Prepare the image
            image = prepare_image(image)
            
            # Predict the class
            if model:
                predictions = model.predict(image)
                class_names = ['Benign', 'Malignant', 'Normal']
                predicted_class = class_names[np.argmax(predictions)]
            else:
                predicted_class = "Model Not Available"
            
            return render_template('index.html', prediction=predicted_class)
        except Exception as e:
            logging.error(f"Prediction error: {e}")
            return "An error occurred during prediction"

# ---------------------------------------------------------------------------
# JSON API + single page app
#
# Everything below is additive: the original `/` and `/predict` routes above are
# untouched, so the classic Jinja interface keeps working exactly as before.
# The React PWA in ./frontend talks to these endpoints instead.
# ---------------------------------------------------------------------------

CLASS_NAMES = ['Benign', 'Malignant', 'Normal']
FRONTEND_DIST = os.path.join(BASE_DIR, "frontend", "dist")


@app.route('/api/health', methods=['GET'])
def api_health():
    """Report whether the service is up and the model is loaded."""
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "classes": CLASS_NAMES,
    })


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """Classify an uploaded ultrasound image and return JSON.

    Response shape:
        {"prediction": "Benign", "confidence": 0.93,
         "probabilities": {"Benign": 0.93, ...},
         "model": "VGG16", "elapsed_ms": 118.4}
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image was uploaded."}), 400

    file = request.files['image']
    if not file or file.filename == '':
        return jsonify({"error": "No image was selected."}), 400

    if model is None:
        return jsonify({
            "error": "The model file is not available on the server."
        }), 503

    started = time.perf_counter()
    try:
        raw = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(raw, cv2.IMREAD_COLOR)
        if image is None:
            return jsonify({"error": "The file could not be read as an image."}), 400

        predictions = model.predict(prepare_image(image))
        scores = np.asarray(predictions).reshape(-1).astype(float)

        # Guard against a model whose head is not already normalised.
        total = float(scores.sum())
        if total > 0 and not np.isclose(total, 1.0):
            scores = scores / total

        probabilities = {
            name: float(score) for name, score in zip(CLASS_NAMES, scores)
        }
        best = int(np.argmax(scores))

        return jsonify({
            "prediction": CLASS_NAMES[best],
            "confidence": float(scores[best]),
            "probabilities": probabilities,
            "model": "VGG16",
            "elapsed_ms": (time.perf_counter() - started) * 1000.0,
        })
    except Exception as e:
        logging.error(f"API prediction error: {e}")
        return jsonify({"error": "An error occurred during prediction."}), 500


@app.route('/app', defaults={'path': ''})
@app.route('/app/<path:path>')
def spa(path):
    """Serve the built React PWA, falling back to its index for client routes."""
    # 1. Ensure the build directory actually exists
    if not os.path.isdir(FRONTEND_DIST):
        return (
            "The PWA has not been built yet. Run: "
            "cd frontend && npm install && npm run build",
            404,
        )
    if path and os.path.exists(os.path.join(FRONTEND_DIST, path)):
        return send_from_directory(FRONTEND_DIST, path)
    return send_from_directory(FRONTEND_DIST, 'index.html')


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)