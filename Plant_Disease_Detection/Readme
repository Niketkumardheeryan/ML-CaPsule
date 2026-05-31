# AgriVision

AgriVision is a Flask-based plant disease detection application that helps users identify possible plant diseases from leaf images using a trained deep learning model.

It is designed to make disease awareness faster and easier by combining image-based prediction, disease information, prevention guidance, multilingual access, and product suggestions in one interface.

---

## Architecture

The architecture below shows how AgriVision handles image upload, preprocessing, model inference, CSV-based information mapping, and final result rendering inside the Flask application.

![AgriVision Architecture](docs/agrivision-architecture.png)

---

## Purpose

The purpose of AgriVision is to support farmers, students, gardeners, and plant enthusiasts by making early plant disease recognition more accessible.

Instead of depending only on manual observation, users can upload a leaf image and get structured support for understanding what the disease may be and what action to consider next.

---

## Objective

The main objective of AgriVision is to reduce the gap between symptom detection and decision-making by providing:

- AI-based plant disease prediction
- disease description and prevention guidance
- organic and chemical treatment path suggestions
- multilingual translation support for wider usability

---

## What AgriVision Does

AgriVision allows users to:

- upload or capture a plant leaf image
- run a trained model to predict the disease class
- view disease details and possible prevention steps
- explore supplement and fertilizer suggestions
- compare organic and chemical product paths
- translate the interface into English, Hindi, and Telugu

---

## UI Preview

### Home Page

The home page introduces AgriVision, supported crop categories, and the main AI workflow in a cleaner responsive layout.

![Home Preview](static/docs/homepage.mp4)

### AI Engine

The AI engine allows users to upload a leaf image or capture one using the camera before running prediction.

![AI Engine Preview](static/docs/Aiengine.mp4)

### Supplements Market

Supplement Market contains the supplements for their respective disease of their kind.

![Supplement Market Preview](static/docs/supplements.mp4)

---

## Features

- Plant disease prediction using a trained CNN model
- Upload and camera-based image input
- Disease description and prevention recommendations
- Supplement marketplace page
- Organic and chemical product suggestion paths
- Multilingual translation support
- Responsive UI for modern browsers
- Shared design system across pages

---

## Tech Stack

- Python
- Flask
- PyTorch
- Torchvision
- Pandas
- NumPy
- Pillow
- HTML
- CSS
- Bootstrap
- JavaScript

---

## Project Structure

```text
Deploy_app/
|-- app.py
|-- CNN.py
|-- disease_info.csv
|-- supplement_info.csv
|-- plant_disease_model_1_latest.pt
|-- requirements.txt
|-- static/
|   |-- docs/
|   |   `-- agrivision-architecture.png
|   `-- uploads/
|-- templates/
|   |-- base.html
|   |-- home.html
|   |-- index.html
|   |-- submit.html
|   |-- market.html
|   |-- about.html
|   `-- contact-us.html
`-- Readme
```

---

## Dataset and Model Flow

1. The user uploads a leaf image.
2. The image is resized and converted into tensor format.
3. The trained CNN model predicts one of the supported disease classes.
4. AgriVision maps that predicted class to:
   - disease name
   - description
   - prevention steps
   - supplement suggestions
5. The result is displayed through the web interface.

---

## Supported Experience

AgriVision currently includes:

- disease detection flow
- disease information page
- supplements page
- about page
- contact page
- theme toggle
- translation support

---

## How To Run Locally

1. Open the project folder.
2. Create and activate a virtual environment if needed.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Flask app:

```bash
python app.py
```

5. Open the local server in your browser.

---

## Requirements

Main dependencies used in AgriVision:

- Flask
- gunicorn
- Werkzeug
- Jinja2
- numpy
- pandas
- Pillow
- torch
- torchvision

---

## Notes

- Product links depend on third-party websites and may change over time.
- Some product previews use fallback placeholders if external images are unavailable.
- The model output should be used as decision support, not as a replacement for expert agricultural advice.

---

## Future Improvements

- Add verified separate organic and chemical products for every disease class
- Replace unstable third-party product images with managed assets
- Add confidence score display for predictions
- Add downloadable prediction reports
- Improve product data quality and source consistency
