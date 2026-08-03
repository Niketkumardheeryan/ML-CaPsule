import streamlit as st
import tensorflow as tf
import time
from PIL import Image, ImageOps
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input

# import json
# import requests

# from streamlit_lottie import st_lottie

# Load the saved model
model = tf.keras.models.load_model(r"Model\vgg_model.keras", compile=False)
# TODO : train generalized model by inverting colour of half of the digits.


def contrast_stretching(image):
    # Calculate the minimum and maximum pixel values in the image
    min_val = np.min(image)
    max_val = np.max(image)

    # Apply contrast stretching
    stretched_image = ((image - min_val) / (max_val - min_val)) * 255  # min-max
    stretched_image = stretched_image.astype(np.uint8)  # Convert to uint8

    return stretched_image


def preprocess_image(image_path):

    # Load the image with the target size
    img = image.load_img(image_path, target_size=(224, 224))

    # Convert the image to a numpy array
    img_array = image.img_to_array(img)

    # Expand the dimensions to match the input shape (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)

    # Preprocess the image using VGG16 preprocess_input function
    preprocessed_img = preprocess_input(img_array)

    # Resize image to match model input size
    # resized_image = equalized_image.resize((224, 224))

    # Apply contrast stretching
    return preprocessed_img


# Define a function for model inference
# @tf.function
def predict(image):
    # Open and preprocess the image
    # img = Image.open(image)
    preprocessed_image = preprocess_image(image)
    # st.image(preprocessed_image, width=500, caption="pre")

    # Convert image to NumPy array
    img_array = np.array(preprocessed_image)
    # img_array = np.expand_dims(img_array, axis=-1)  # Add batch dimension

    # Make predictions using the loaded model
    prediction = model.predict(img_array)

    return prediction


# Streamlit app code
st.set_page_config(
    page_title="Pneumonia Prediction from Chest X-Ray images",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        # "Get Help": "https://github.com/Subhranil2004/digits-in-ink#live-demo",
        # "Report a bug": "https://github.com/Subhranil2004/handwritten-digit-classification/issues",
    },
)

# Sidebar
with st.sidebar:
    st.image(
        "./images/image.jpg",
        use_column_width=True,
        output_format="JPEG",
    )

# st.sidebar.subheader(":blue[[Please use a desktop for the best experience.]]")

st.sidebar.title("Pneumonia Prediction from Chest X-Ray images")
st.sidebar.write(
    "The model is trained on the ***Pneumonia X-Ray Images dataset*** from **Kaggle** and uses Convolutional Neural Network with Data augmentation."  # It has an exceptional accuracy rate of 99.45% on MNIST test dataset."
)

# st.sidebar.write(
#     "There is always a scope for improvement and I would appreciate suggestions and/or constructive criticisms."
# )

st.sidebar.link_button("GitHub", "https://github.com/Subhranil2004")

st.markdown(
    f"""
        <style>
            .sidebar {{
                width: 500px;
            }}
        </style>
    """,
    unsafe_allow_html=True,
)

# Main content

st.title("Pneumonia Prediction")
# st.subheader("from Chest X-Ray images")
uploaded_file = st.file_uploader(
    "Choose a chest X-Ray image...",
    type=["jpg", "png", "bmp", "tiff"],
)

if uploaded_file is not None:
    # Display the uploaded image with border
    st.image(
        uploaded_file,
        caption="Uploaded Image",
        width=300,
        clamp=True,
        # output_format="JPEG",
    )

    # Perform prediction
    if st.button("Predict"):
        result = predict(uploaded_file)
        st.write("Done!")

        # Display the prediction result
        # max_index = round(result)
        if result > 0.5:
            output = ":red[PNEUMONIA  AFFECTED] ⚠️"
            conf = result * 100
        else:
            output = "NORMAL ✅"
            conf = (1 - result) * 100

        st.write(f"Prediction :  {output}  [Confidence: :green[{conf[0][0]:.2f} %] ]")


expander = st.expander("Some sample X-ray images to try with...", expanded=True)
expander.write("Just drag-and-drop your chosen image above ")
expander.image(
    [
        "./images/viral2.jpeg",
        "./images/bacterial1.jpg",
        "./images/viral1.jpg",
        "./images/IM-0028-0001.jpeg",
        "./images/person101_bacteria_484.jpeg",
        "./images/person3_virus_17.jpeg",
    ],
    width=200,
)
# expander.write(
#     "All images might not give the desired result as the *1st* prediction due to low contrast. Check the probability scores in such cases."
# )
# expander = st.expander("View Model Training and Validation Results")
# expander.write("Confusion Matrix: ")
# expander.image("./images/CNN_ConfusionMatrix.png", use_column_width=True)
# expander.write("Graphs: ")
# expander.image("./images/CNN_Graphs.png", use_column_width=True)

# Footer
st.write("\n\n\n")
st.markdown("---")
st.markdown(
    f"""Drop in any discrepancies or give suggestions in `Report a bug` option within the `⋮` menu"""
)

st.markdown(
    f"""<div style="text-align: right"> Developed by Subhranil Nandy </div>""",
    unsafe_allow_html=True,
)
