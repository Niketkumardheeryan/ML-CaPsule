from flask import Flask, request, jsonify
from inference import generate_headline

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():

    try:
        data = request.json

        if not data or "article" not in data:
            return jsonify({
                "error": "Article text is required"
            }), 400

        article = data["article"]

        if len(article.strip()) < 20:
            return jsonify({
                "error": "Article text too short"
            }), 400

        headline = generate_headline(article)

        return jsonify({
            "headline": headline
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
    
if __name__ == "__main__":
    app.run(debug=True)