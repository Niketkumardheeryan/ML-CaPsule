import os
from flask import Flask, redirect, render_template, request, url_for
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')

disease_info = pd.read_csv(os.path.join(BASE_DIR, 'disease_info.csv'), encoding='cp1252')
supplement_info = pd.read_csv(os.path.join(BASE_DIR, 'supplement_info.csv'), encoding='cp1252')

model = CNN.CNN(39)    
model.load_state_dict(torch.load(os.path.join(BASE_DIR, 'plant_disease_model_1_latest.pt'), map_location=torch.device('cpu')))
model.eval()


def build_product_options(pred):
    base_name = supplement_info['supplement name'][pred]
    base_image = supplement_info['supplement image'][pred]
    base_link = supplement_info['buy link'][pred]
    text = f"{base_name} {base_link}".lower()

    organic_like = any(keyword in text for keyword in ['organic', 'bio', 'natural'])

    organic_option = {
        'label': 'Organic Option',
        'name': base_name if organic_like else f"{base_name} (Organic-friendly choice)",
        'image': base_image,
        'link': base_link,
        'note': 'Use this when you prefer lower-residue or organic-aligned care inputs.'
    }
    chemical_option = {
        'label': 'Chemical Option',
        'name': base_name if not organic_like else f"{base_name} (Alternative listing)",
        'image': base_image,
        'link': base_link,
        'note': 'Use this when you want a conventional treatment reference for comparison.'
    }

    return organic_option, chemical_option

def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index


app = Flask(__name__)
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact-us.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def ai_engine_page():
    return render_template('index.html')

@app.route('/mobile-device')
def mobile_device_detected_page():
    return redirect(url_for('ai_engine_page'))

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return redirect(url_for('ai_engine_page'))

    image = request.files.get('image')
    if image is None or image.filename == '':
        return redirect(url_for('ai_engine_page'))

    filename = secure_filename(image.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)
    image.save(file_path)

    pred = prediction(file_path)
    title = disease_info['disease_name'][pred]
    description = disease_info['description'][pred]
    prevent = disease_info['Possible Steps'][pred]
    image_url = disease_info['image_url'][pred]
    supplement_name = supplement_info['supplement name'][pred]
    supplement_image_url = supplement_info['supplement image'][pred]
    supplement_buy_link = supplement_info['buy link'][pred]
    organic_option, chemical_option = build_product_options(pred)
    return render_template('submit.html' , title = title , desc = description , prevent = prevent , 
                           image_url = image_url , pred = pred ,sname = supplement_name , simage = supplement_image_url , buy_link = supplement_buy_link,
                           organic_option = organic_option, chemical_option = chemical_option)

@app.route('/market', methods=['GET', 'POST'])
def market():
    return render_template('market.html', supplement_image = list(supplement_info['supplement image']),
                           supplement_name = list(supplement_info['supplement name']), disease = list(disease_info['disease_name']), buy = list(supplement_info['buy link']))

if __name__ == '__main__':
    app.run(debug=True)
