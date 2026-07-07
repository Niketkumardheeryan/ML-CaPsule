import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import requests
import io

# Load the pre-trained model
model = load_model('final_chess.h5')

# Define the classes
class_names = ['queen', 'rook', 'bishop', 'king', 'knight', 'pawn']

piece_descriptions = {
    'bishop': 'The Bishop moves diagonally, any number of squares.',
    'king': 'The King moves one square in any direction.',
    'knight': 'The Knight moves in an L-shape: two squares in one direction and then one square perpendicular.',
    'pawn': 'The Pawn moves forward one square, with the option to move two squares on its first move.',
    'queen': 'The Queen moves any number of squares in any direction: horizontally, vertically, or diagonally.',
    'rook': 'The Rook moves any number of squares horizontally or vertically.'
}

# Fetch move images from an external chess API or a predefined URL
def fetch_move_image(piece_name):
    piece_images = {
        'bishop': 'https://upload.wikimedia.org/wikipedia/commons/1/1d/Chess_piece_-_White_bishop.JPG',
        'king': 'https://files.herculeschess.com/file/herculeschess/2020/04/moving-300x300.png',
        'knight': 'https://mrcoles.com/media/img/chess/knight-1-move.png',
        'pawn': 'https://www.chessbazaar.com/blog/wp-content/uploads/2019/05/Pawn.gif',
        'queen': 'https://chesseasy.com/wp-content/uploads/2022/10/image-56.png',
        'rook': 'https://brilliant-staff-media.s3-us-west-2.amazonaws.com/tiffany-wang/MTXdYoA8k9.png'
    }
    image_url = piece_images.get(piece_name, '')
    response = requests.get(image_url)
    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    return None

# Streamlit app layout
st.set_page_config(page_title='Chess Piece Classification', layout='centered')

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #333;
        color: #f0f0f5;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
    }
    .title {
        text-align: center;
        color: #f0f0f5;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .info-box {
        border: 2px solid #007bff;
        border-radius: 10px;
        padding: 20px;
        background-color: #444;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    .info-box h2 {
        color: #007bff;
    }
    .info-box p {
        color: #f0f0f5;
    }
    .img-container {
        text-align: center;
        margin-bottom: 20px;
    }
    .uploaded-img {
        border: 2px solid #007bff;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
    }
    .uploaded-img img {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">Chess Piece Classification</div>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload a chess piece image", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Display the uploaded image
    st.markdown('<div class="img-container">', unsafe_allow_html=True)
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Preprocess the image
    image = Image.open(uploaded_file)
    img = image.resize((128, 128))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict the class
    prediction = model.predict(img_array)
    predicted_class_index = np.argmax(prediction, axis=1)[0]
    predicted_class_name = class_names[predicted_class_index]

    # Display the prediction
    st.success(f"The predicted chess piece is: **{predicted_class_name.capitalize()}**", icon="✅")

    # Display information about the chess piece
    piece_info = piece_descriptions.get(predicted_class_name, "No information available.")
    st.markdown(f"""
        <div class="info-box">
            <h2>Information about {predicted_class_name.capitalize()}</h2>
            <p>{piece_info}</p>
        </div>
        """, unsafe_allow_html=True)

    # Fetch and display move image
    move_image = fetch_move_image(predicted_class_name)
    if move_image:
        st.markdown('<div class="img-container">', unsafe_allow_html=True)
        st.image(move_image, caption=f"Moves of {predicted_class_name.capitalize()}", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Move image not available.")
else:
    st.info("Please upload an image of a chess piece.")
