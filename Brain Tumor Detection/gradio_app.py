import os
import numpy as np
import tensorflow as tf
import gradio as gr
from PIL import Image

# Automatically find best_model.h5 in any of the possible directories
dir_path = os.path.dirname(os.path.realpath(__file__))
model_locations = [
    os.path.join(dir_path, "best_model.h5"),
    os.path.join(dir_path, "Web App", "best_model.h5"),
    os.path.join(dir_path, "Model", "best_model.h5")
]

model = None
for path in model_locations:
    if os.path.exists(path):
        model = tf.keras.models.load_model(path)
        break

if model is None:
    raise FileNotFoundError("Could not find 'best_model.h5' in any project directories.")

class_labels = ['Glioma', 'Meningioma', 'No tumor', 'Pituitary']

def predict_tumor(img):
    if img is None:
        return "No image uploaded."
    
    # Preprocess image to match training input shape
    img = img.resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Predict
    predictions = model.predict(img_array)[0]
    return {class_labels[i]: float(predictions[i]) for i in range(len(class_labels))}

# Setup Interface
demo = gr.Interface(
    fn=predict_tumor,
    inputs=gr.Image(type="pil", label="Upload Brain MRI Scan"),
    outputs=gr.Label(num_top_classes=4, label="Prediction Confidence"),
    title="Brain Tumor Classification Hub (Gradio)",
    description="Upload an MRI scan to detect if a tumor is present and classify its type."
)

if __name__ == "__main__":
    demo.launch()