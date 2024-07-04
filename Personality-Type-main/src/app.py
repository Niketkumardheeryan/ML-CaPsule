from flask import Flask, render_template, request, url_for, redirect
from logic.Model import Model,train_models
from logic.Predict import Predictor
from logic.Scraper_Face import  FBScraper, ExecFace
from bson import json_util
import json
import yaml
import pickle

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)


@app.route("/", methods= ['GET', 'POST'])
def index():
    if request.method == 'POST':
        global textpredict
        textpredict = request.form['text']
        return predict_text()
    return render_template('index.html')

def predict_text():
    if textpredict is not None:
        p = Predictor()
        global prediction
        prediction = p.predict([textpredict])
        return redirect(url_for('result'))
    else:
        return str("-----------No Text to Predict------------")

@app.route("/facebook/", methods= ['GET', 'POST'])
def facebook():     
    if request.method == 'POST':
        try:
            email = request.form['email']
            passw = request.form['passw']
            profile = request.form['profile']
            write_yaml(email, passw, profile)
            prediction  = ExecFace()
            return redirect(url_for('result'))
            
        except: 
            prediction  = ExecFace()
            return redirect(url_for('result'))
    return render_template('facebook.html')

@app.route("/result/", methods= ['GET', 'POST'])
def result():
    nombre = prediction.pop(0)
    return render_template('result.html', pred= prediction, nom = nombre)

def write_yaml(nemail, npassword, nprofile):
    data = dict(
    email= nemail, password= npassword, profile_url= nprofile)
    with open('logic/Fb_login_creds.yaml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

if __name__ == '__main__':
    app.run(debug=True)
