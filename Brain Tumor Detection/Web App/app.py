from flask import Flask, render_template, request
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import base64

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
        img = Image.open(image.stream)
        img = preprocess_image(img)
        predictions = model.predict(img)
        predicted_class = np.argmax(predictions)
        predicted_label = class_labels[predicted_class]
        img_base64 = image_to_base64(Image.open(image.stream))
        return render_template('result.html', description=predicted_label, image_data=img_base64)
    except Exception as e:
        return render_template('error.html', error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)