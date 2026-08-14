# 🎨 Speech/Text to Image Converter

This Streamlit application allows users to convert spoken words or text input into images using the Stable Diffusion model. The app leverages speech recognition to capture user input and generates images based on the provided description.

## 📖 Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Acknowledgments](#acknowledgments)

## Features

- **Speech Recognition with Ambient Noise Calibration**: Uses the microphone to capture spoken input, with configurable ambient noise calibration, energy sensitivity, timeout, and phrase limits for noisy environments.
- **Editable Prompt Workflow**: Captured speech seamlessly populates an editable text prompt, allowing users to review and adjust the text before generating images.
- **Text Input**: Users can also type in the text manually if preferred.
- **Image Generation**: Generates high-quality images from prompts using the Stable Diffusion model.

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

- **Speech Recognition Settings**: Adjust ambient noise calibration duration, sensitivity factor, timeout, and phrase limit in the sidebar for optimal performance in noisy environments.
- **Speech Input**: Click "🎙️ Recognize Speech", remain quiet during initial background noise calibration, and speak your prompt.
- **Edit & Generate**: Review or edit the recognized text in the prompt field, then click "🎨 Generate Image" to produce the image with Stable Diffusion.

## Demo Video/Image 

<img src="https://github.com/jaidh01/ML-CaPsule/blob/Speech-to-Image-Generator/Speech-to-Image%20Generator/screenshot1.png" alt="Speech to Image Converter Screenshot" width="500" />

<img src="https://github.com/jaidh01/ML-CaPsule/blob/Speech-to-Image-Generator/Speech-to-Image%20Generator/screenshot2.png" alt="Speech to Image Converter Screenshot" width="500" />

[Watch the demo video here](https://raw.githubusercontent.com/Niketkumardheeryan/speech-to-image-converter/main/speech-to-image.mp4)


## Acknowledgments

This application uses the following:
- [Stable Diffusion Pipeline](https://github.com/huggingface/diffusers) for image generation.
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) library for capturing and processing speech input.
