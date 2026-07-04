import os
import logging
from flask import Flask, request, render_template
import numpy as np
import cv2
import tensorflow as tf

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

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)