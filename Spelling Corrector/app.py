import streamlit as st
import tensorflow as tf
import joblib

@st.cache(allow_output_mutation=True)
def load_model():
  model=tf.keras.models.load_model('./Model/seq2seq_epoch_100.h5')
  return model
def load_transformer():
  transformer = joblib.load("./Model/data_transformer.joblib")
  return transformer
with st.spinner('Model is being loaded..'):
  model=load_model()
  transformer=load_transformer()

st.title('Spell Checker Using Sequence to Sequence Model')

text = st.text_area("Enter Text:", value='', height=None, max_chars=None, key=None)

if st.button('Correct Spelling'):
    if text == '':
        st.write('Please enter text for checking') 
    else: 
        prediction = model.predict(transformer.transform(text))
        corrected_spell=prediction[0]
        st.write('Corrected Word - ' + str(corrected_spell))
else: pass
