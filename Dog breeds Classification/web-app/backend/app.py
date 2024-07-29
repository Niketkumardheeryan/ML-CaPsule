import os
from flask import Flask, render_template,request,jsonify
from reverseProxy import proxyRequest
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import pandas as pd
from tensorflow.keras.applications.vgg16 import preprocess_input 
from keras.applications import ResNet50V2
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, BatchNormalization, GlobalAveragePooling2D
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import array
from check import classifier
from PIL import Image

MODE = os.getenv('FLASK_ENV')
DEV_SERVER_URL = 'http://localhost:3000/'

print('success')
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the file name
file_name = 'breedinfo.csv'

# Get the absolute path of the file
file_path = os.path.join(script_dir, file_name)
b = pd.read_csv(file_path)
# Serialize the dictionary to JSON
# row1_json = json.dumps(row1_dict)

def classifyImage(file):
    img = Image.open(file.stream)
    x = classifier(img)
    row1 = b.iloc[x[0]-1]
    data = row1.to_list()
    return {'dog':str(x[1]),'dat':data}


app = Flask(__name__)
file=""
# Ignore static folder in development mode.
if MODE == "development":
    app = Flask(__name__, static_folder=None)



@app.route('/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return ({'error': 'No file part'}), 400
        return(request)
    if (request.files['image']): 
        file = request.files['image']
        result = classifyImage(file)
        return result

@app.route('/')
@app.route('/<path:path>')
def index(path=''):
    if MODE == 'development':
        return proxyRequest(DEV_SERVER_URL, path)
    else:
        return render_template("index.html")