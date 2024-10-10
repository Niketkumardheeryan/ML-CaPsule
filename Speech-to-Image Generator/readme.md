# 🎨 Speech/Text to Image Converter

This Streamlit application allows users to convert spoken words or text input into images using the Stable Diffusion model. The app leverages speech recognition to capture user input and generates images based on the provided description.

## 📖 Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Acknowledgments](#acknowledgments)

## Features

- **Speech Recognition**: Uses the microphone to capture spoken input and convert it into text.
- **Text Input**: Users can also type in the text if they prefer not to use speech.
- **Image Generation**: The app uses the Stable Diffusion model to generate images based on the text or speech input.

## Requirements

The application requires the following Python libraries:
- `streamlit`
- `PIL`
- `torch`
- `diffusers`
- `speech_recognition`

See the `requirements.txt` file for more details.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Niketkumardheeryan/speech-to-image-converter.git
   cd speech-to-image-converter
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run speech-text_image_generator.py
   ```

## Usage

- **Speech Input**: Click the button to start listening for speech input, and the application will convert it to text and generate an image based on the recognized text.
- **Text Input**: Alternatively, you can type in a description to generate an image.

## Acknowledgments

This application uses the following:
- [Stable Diffusion Pipeline](https://github.com/huggingface/diffusers) for image generation.
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) library for capturing and processing speech input.
