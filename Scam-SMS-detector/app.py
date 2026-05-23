from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

# Load dataset
df = pd.read_csv("spam.csv", encoding='latin-1')

df = df[['v1', 'v2']]
df.columns = ['label', 'message']

df['label'] = df['label'].map({'ham':0, 'spam':1})

X = df['message']
y = df['label']

# Vectorization
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X)

# Train model
model = MultinomialNB()
model.fit(X, y)

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = ""

    if request.method == "POST":

        message = request.form["message"]

        data = vectorizer.transform([message])

        result = model.predict(data)

        if result[0] == 1:
            prediction = "Spam Message 🚨"
        else:
            prediction = "Safe Message ✅"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)