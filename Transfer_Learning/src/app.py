import json
from io import BytesIO
from PIL import Image
import os


import streamlit as st
import pandas as pd
import numpy as np

from classification import ClassificationModel


@st.cache()
def get_path(file_path):
    path = os.path.dirname(__file__)
    my_file = path+file_path
    return my_file


@st.cache()
def load_model(path: str = get_path('/models/dog_resnet18.pt')) -> ClassificationModel:
    """Retrieves the trained model and maps it to the CPU by default,
    can also specify GPU here."""
    model = ClassificationModel(path_to_pretrained_model=path)
    return model

@st.cache()
def load_index_to_label_dict(path: str = get_path('/index_to_class_label.json')) -> dict:
    """Retrieves and formats the
    index to class label
    lookup dictionary needed to
    make sense of the predictions.
    When loaded in, the keys are strings, this also
    processes those keys to integers."""
    with open(path, 'r') as f:
        index_to_class_label_dict = json.load(f)
    index_to_class_label_dict = {
        int(k): v for k, v in index_to_class_label_dict.items()}
    return index_to_class_label_dict


@st.cache()
def predict(img: Image.Image, index_to_label_dict: dict, model, k: int) -> list:
    """
    Froze all layers of model weights and only learned weights on the final layer (Feature Extraction).
    The weights of the first layer are still what was
    used in the ImageNet paper and we need to process
    the new images just like they did.
    This function transforms the image accordingly,
    puts it to the necessary device (cpu by default here),
    feeds the image through the model getting the output tensor,
    converts that output tensor to probabilities using Softmax,
    and then extracts and formats the top k predictions."""
    formatted_predictions = model.predict_proba(img, k, index_to_label_dict)
    return formatted_predictions


if __name__=='__main__':
    model=load_model()
    index_to_class_label_dict = load_index_to_label_dict()
    cover_image=get_path("/ui/cover.jpg")


    st.markdown("<h1 style='text-align: center; color: red;'>Identify Dog Breeds</h1>", unsafe_allow_html=True)
    st.image(cover_image)
    st.markdown("<h6 style='text-align: center; color: white;'>..Upload an image of any dog to identify the breed..</h6>", unsafe_allow_html=True)

    file = st.file_uploader('Upload An Image')
    if file is not None:  # if user uploaded file
        img = Image.open(file)
        prediction = predict(img, index_to_class_label_dict, model, k=5)
        top_prediction = prediction[0][0]
        st.title("Image you've selected: ")
        resized_image = img.resize((336, 336))
        st.image(resized_image)

        st.title("Likely dog breeds: ")
        df = pd.DataFrame(data=np.zeros((5, 2)),columns=['Breed', 'Confidence Level'], index=np.linspace(1, 5, 5, dtype=int))
        for idx, p in enumerate(prediction):
            link = 'https://en.wikipedia.org/wiki/' + \
                p[0].lower().replace(' ', '_')
            df.iloc[idx,
                    0] = f'<a href="{link}" target="_blank">{p[0].title()}</a>'
            df.iloc[idx, 1] = p[1]
        st.write(df.to_html(escape=False), unsafe_allow_html=True)

