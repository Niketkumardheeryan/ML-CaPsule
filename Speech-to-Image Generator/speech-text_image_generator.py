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

# Sidebar Settings for Speech Recognition
st.sidebar.header("Speech Recognition Settings")
calib_duration = st.sidebar.slider(
    "Ambient Noise Calibration (seconds)",
    min_value=1.0,
    max_value=5.0,
    value=2.0,
    step=0.5,
    help="Duration to analyze background noise before listening. Increase in noisy environments."
)
energy_ratio = st.sidebar.slider(
    "Energy Sensitivity Factor",
    min_value=1.1,
    max_value=2.5,
    value=1.5,
    step=0.1,
    help="Higher values require louder speech relative to background noise."
)
listen_timeout = st.sidebar.slider(
    "Listening Timeout (seconds)",
    min_value=3,
    max_value=15,
    value=7,
    help="Maximum time to wait for speech input to begin."
)
phrase_limit = st.sidebar.slider(
    "Phrase Limit (seconds)",
    min_value=5,
    max_value=30,
    value=15,
    help="Maximum duration allowed for a single spoken sentence."
)

# Initialize Session State
if "prompt_text" not in st.session_state:
    st.session_state["prompt_text"] = ""

# Function to recognize speech
def recognize_speech(calibration_duration=2.0, dynamic_energy_ratio=1.5, timeout=7, phrase_time_limit=15):
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_ratio = dynamic_energy_ratio
    
    status = st.empty()
    try:
        with sr.Microphone() as source:
            status.info("Calibrating background noise... Please remain quiet.")
            recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)
            
            status.info("Listening... Speak now!")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            
            status.info("Processing speech...")
            text = recognizer.recognize_google(audio)
            status.success(f"Recognized: '{text}'")
            return text
    except sr.WaitTimeoutError:
        status.warning("No speech was detected within the timeout period. Please try again.")
    except sr.UnknownValueError:
        status.error("Could not understand the audio. Please speak clearly or adjust noise calibration.")
    except sr.RequestError as e:
        status.error(f"Speech recognition service error: {e}")
    except OSError as e:
        status.error(f"Microphone input error: {e}. Please ensure a working microphone is connected.")
    except Exception as e:
        status.error(f"An unexpected error occurred during speech recognition: {e}")
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

# Speech Recognition Trigger
if st.button("Recognize Speech"):
    recognized_text = recognize_speech(
        calibration_duration=calib_duration,
        dynamic_energy_ratio=energy_ratio,
        timeout=listen_timeout,
        phrase_time_limit=phrase_limit
    )
    if recognized_text:
        formatted_prompt = f"{recognized_text}, 4k, High Resolution"
        st.session_state["prompt_text"] = formatted_prompt
        st.rerun()

# Text input for prompt linked to session state
prompt_text = st.text_area(
    "Enter or edit prompt for image generation:",
    value=st.session_state["prompt_text"],
    key="prompt_input_field",
    help="You can manually type a prompt or edit text captured via speech recognition."
)
st.session_state["prompt_text"] = prompt_text

# Generate Button
if st.button("Generate Image"):
    current_prompt = st.session_state["prompt_text"].strip()
    if current_prompt:
        with st.spinner("Generating image..."):
            image = generate_image(current_prompt)
            st.image(image, caption="Generated Image", use_column_width=True)
            # Optionally, save the image
            image.save('generated_image.png')
            st.success("Image generated successfully!")
    else:
        st.warning("Please enter a prompt or use speech recognition first.")
