import streamlit as st
import pandas as pd
import joblib
import numpy as np

st.set_page_config(page_title='Migraine Type Prediction', page_icon=':brain:', layout='wide')

model = joblib.load('migraine_trained_model.sav')

def user_input_features():
    age = st.text_input('Age', '25')
    duration = st.selectbox('Duration of the migraine attack (in hours)', [1, 2, 3])
    frequency = st.selectbox('Frequency of migraine attacks (per month)', list(range(1, 9)))
    location = st.selectbox('Location of the headache', ['One side', 'Both sides'])
    character = st.selectbox('Character of the pain', ['Throbbing', 'Pulsating', 'Sharp', 'Dull'])
    intensity = st.selectbox('Intensity of the pain', [0, 1, 2, 3])
    nausea = st.selectbox('Presence of nausea', ['Yes', 'No'])
    vomit = st.selectbox('Presence of vomiting', ['Yes', 'No'])
    phonophobia = st.selectbox('Sensitivity to sound', ['Yes', 'No'])
    photophobia = st.selectbox('Sensitivity to light', ['Yes', 'No'])
    visual = st.selectbox('Presence of visual disturbances', ['Yes', 'No'])
    sensory = st.selectbox('Presence of sensory disturbances', ['Yes', 'No'])
    dysphasia = st.selectbox('Difficulty in speaking or understanding speech', ['Yes', 'No'])
    dysarthria = st.selectbox('Difficulty in articulating words', ['Yes', 'No'])
    vertigo = st.selectbox('Presence of vertigo', ['Yes', 'No'])
    tinnitus = st.selectbox('Presence of ringing in the ears', ['Yes', 'No'])
    hypoacusis = st.selectbox('Reduced hearing ability', ['Yes', 'No'])
    diplopia = st.selectbox('Presence of double vision', ['Yes', 'No'])
    defect = st.selectbox('Presence of any neurological defect', ['Yes', 'No'])
    ataxia = st.selectbox('Lack of muscle coordination', ['Yes', 'No'])
    conscience = st.selectbox('Altered state of consciousness', ['Yes', 'No'])
    paresthesia = st.selectbox('Presence of abnormal skin sensations', ['Yes', 'No'])
    dpf = st.text_input('Duration, frequency, and pattern of the migraine attacks', '1')
    
    data = {
        'Age': int(age),
        'Duration': int(duration),
        'Frequency': int(frequency),
        'Location': 1 if location == 'One side' else 0,
        'Character': ['Throbbing', 'Pulsating', 'Sharp', 'Dull'].index(character),
        'Intensity': int(intensity),
        'Nausea': 1 if nausea == 'Yes' else 0,
        'Vomit': 1 if vomit == 'Yes' else 0,
        'Phonophobia': 1 if phonophobia == 'Yes' else 0,
        'Photophobia': 1 if photophobia == 'Yes' else 0,
        'Visual': 1 if visual == 'Yes' else 0,
        'Sensory': 1 if sensory == 'Yes' else 0,
        'Dysphasia': 1 if dysphasia == 'Yes' else 0,
        'Dysarthria': 1 if dysarthria == 'Yes' else 0,
        'Vertigo': 1 if vertigo == 'Yes' else 0,
        'Tinnitus': 1 if tinnitus == 'Yes' else 0,
        'Hypoacusis': 1 if hypoacusis == 'Yes' else 0,
        'Diplopia': 1 if diplopia == 'Yes' else 0,
        'Defect': 1 if defect == 'Yes' else 0,
        'Ataxia': 1 if ataxia == 'Yes' else 0,
        'Conscience': 1 if conscience == 'Yes' else 0,
        'Paresthesia': 1 if paresthesia == 'Yes' else 0,
        'DPF': int(dpf)
    }
    features = pd.DataFrame(data, index=[0])
    return features

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.title('Migraine Type Prediction')
    input_df = user_input_features()

    if st.button('Predict'):
        prediction = model.predict(input_df)
        st.subheader('Prediction')
        st.write(f"**Migraine Type:** {prediction[0]}")