from flask import Flask, render_template, request

import requests
from bs4 import BeautifulSoup

import logging
import pymongo
import os

application = Flask(__name__)
app = application

# Disable debug mode
app.debug = False

@app.route("/", methods=['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            query = request.form['content'].replace(" ", "")
            save_directory = "images/"
            
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

            response = requests.get(f"https://www.google.com/search?q={query}&sxsrf=AJOqlzUuff1RXi2mm8I_OqOwT9VjfIDL7w:1676996143273&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiq-qK7gaf9AhXUgVYBHYReAfYQ_AUoA3oECAEQBQ&biw=1920&bih=937&dpr=1#imgrc=1th7VhSesfMJ4M")

            soup = BeautifulSoup(response.content, "html.parser")

            image_tags = soup.find_all("img")

            del image_tags[0]
            img_data = []
            for index, image_tag in enumerate(image_tags):
                image_url = image_tag['src']
                image_data = requests.get(image_url).content
                mydict = {"Index": index, "Image": image_data}
                img_data.append(mydict)
                with open(os.path.join(save_directory, f"{query}_{image_tags.index(image_tag)}.jpg"), "wb") as f:
                    f.write(image_data)

            client = pymongo.MongoClient("mongodb://localhost:27017/")
            db = client['image_scrap']
            review_col = db['image_scrap_data']
            review_col.insert_many(img_data)

            return "image loaded"
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0")
