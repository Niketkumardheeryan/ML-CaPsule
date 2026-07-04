import os
from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import base64
import os

def load_model_and_labels():
    # Get the directory path of the current file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    model_path = os.path.join(dir_path, "best_model.h5")
    model = tf.keras.models.load_model(model_path)
    class_labels = ['Glioma', 'Meningioma', 'No tumor', 'Pituitary']
    return model, class_labels


def preprocess_image(img):
    img = img.resize((224, 224))  # Ensure consistent size with model training
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return img

def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

app = Flask(__name__)
model, class_labels = load_model_and_labels()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        image = request.files['image']

        # Read uploaded image only once
        image_bytes = image.read()

        # Create image object for display
        img_pil = Image.open(io.BytesIO(image_bytes))

        # Create separate image object for model preprocessing
        img = preprocess_image(
            Image.open(io.BytesIO(image_bytes))
        )

        predictions = model.predict(img)
        predicted_class = np.argmax(predictions)
        predicted_label = class_labels[predicted_class]

        # Convert uploaded image to base64 for rendering
        img_base64 = image_to_base64(img_pil)

        return render_template(
            'result.html',
            description=predicted_label,
            image_data=img_base64
        )

    except Exception as e:
        return render_template(
            'error.html',
            error_message=str(e)
        )

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)
