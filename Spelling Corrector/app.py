import streamlit as st
import tensorflow as tf


@st.cache(allow_output_mutation=True)
def load_model():
  model=tf.keras.models.load_model('./Model/seq2seq_epoch_100.h5')
  return model
with st.spinner('Model is being loaded..'):
  model=load_model()

st.write("""
         # Spelling Corrector
         """
         )

test_sentence="My name is Shreya"

