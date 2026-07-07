from flask import Flask, flash, request, redirect, url_for, render_template
from keras.models import load_model
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

word_dict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X', 24:'Y',25:'Z'}
model = load_model('./model.h5')

UPLOAD_FOLDER = 'static/'


app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)
        path = UPLOAD_FOLDER + filename
        img = cv2.imread(path)
        img = cv2.resize(img, (400, 400))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_final = cv2.resize(img, (28, 28))
        img_final = np.reshape(img_final, (1, 28, 28, 1))
        pred = word_dict[np.argmax(model.predict(img_final))]
        flash('The character is '+pred)
        print(pred)
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg')
        return redirect(request.url)


@app.route('/static/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='/' + filename), code=301)


if __name__ == "__main__":
    app.run(debug=True)
