# YT_transcriber-(venv: conda)

import streamlit as st
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline
import speech_recognition as sr

# Set up the Streamlit app
st.title("Speech/Text to Image Converter")
st.markdown("### Using Speech Recognition and Stable Diffusion")
st.markdown("Please be patient, Image Generation takes some time.")

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening for speech...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        
        try:
            st.info("Recognizing speech...")
            text = recognizer.recognize_google(audio)
            st.success(f"Recognized: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio")
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
        return None

# Function to generate image
@st.cache_resource
def load_pipeline():
    modelid = "CompVis/stable-diffusion-v1-4"
    device = "cuda"
    pipe = StableDiffusionPipeline.from_pretrained(modelid, revision="fp16", torch_dtype=torch.float16)
    pipe.to(device)
    return pipe

def generate_image(prompt):
    pipe = load_pipeline()
    with torch.autocast("cuda"):
        output = pipe(prompt, guidance_scale=8.5)
    return output.images[0]

# Text input for prompt
prompt_text = st.text_input("Enter a prompt for the image generation:")

# Button to trigger speech recognition
if st.button("Recognize Speech"):
    recognized_text = recognize_speech()
    if recognized_text:
        prompt_text = f"{recognized_text}, 4k, High Resolution"
        if prompt_text:
            st.text_input("Recognized Prompt", value=prompt_text)
            with st.spinner("Generating image..."):
                image = generate_image(prompt_text)
                st.image(image, caption="Generated Image", use_column_width=True)
                st.success("Image generated successfully!")

# Generate button
if st.button("Generate Image"):
    if prompt_text:
        with st.spinner("Generating image..."):
            image = generate_image(prompt_text)
            st.image(image, caption="Generated Image", use_column_width=True)
            # Optionally, save the image
            image.save('generated_image.png')
            st.success("Image generated successfully!")
    else:
        st.warning("Please enter a prompt or use speech recognition first.")

