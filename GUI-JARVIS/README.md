# AI-JARVIS-VOICE-ASISTANT
AI-JARVIS is an intelligent voice assistant or personal assistant that can perform tasks or services for an individual based on verbal commands i.e. by interpreting human speech and respond via synthesized voices. Users can ask their assistants’ questions, control home automation devices, and media playback via voice, and manage other basic tasks such as email, to-do lists, open or close any application etc with verbal commands.

![Python 3.9](https://img.shields.io/badge/Python-3.9-brightgreen.svg) 
![pysstx3](https://img.shields.io/badge/Library-pysstx3-orange.svg)
![speech_recognition](https://img.shields.io/badge/Library-speech_recognition-blue.svg)
![random](https://img.shields.io/badge/Library-random-red.svg)
![re](https://img.shields.io/badge/Library-re-yellow.svg)
![smtplib](https://img.shields.io/badge/Library-smtplib-pink.svg)
![winsound](https://img.shields.io/badge/Library-winsound-brown.svg)
![wikipedia](https://img.shields.io/badge/Library-wikipedia-white.svg)
![sys](https://img.shields.io/badge/Library-sys-black.svg)
![os](https://img.shields.io/badge/Library-os-violet.svg)
![webbrowser](https://img.shields.io/badge/Library-webbrowser-red.svg)
![datetime](https://img.shields.io/badge/Library-datetime-green.svg)
![PyQt5](https://img.shields.io/badge/Library-PyQt5-orange.svg)
![yahoo_fin](https://img.shields.io/badge/Library-yahoo_fin-purple.svg)
![geopy](https://img.shields.io/badge/Library-geopy-pink.svg)
![bs4](https://img.shields.io/badge/Library-bs4-yellow.svg)
![urllib](https://img.shields.io/badge/Library-urllib-orange.svg)

#### A glimpse of the project:
 ![GIF](Material/jarvis_gif.gif)

# Table of Contents

- [Demo](#demo)
- [Overview](#overview)
- [Motivation](#motivation)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Directory Tree](#directory-tree)
- [Technologies Used](#technologies-used)
- [Bug / Feature Request](#bug--feature-request)
- [Future Scope](#future-scope)

---

# Demo

https://youtu.be/c5g8Q0sDR0g

---

# Overview

AI-JARVIS currently supports the following functionalities:

1. Predicts the innings score
2. Predicts the winner of the match
3. Predicts the current weather conditions
4. Predicts the current temperature
5. Plays a random song
6. Opens installed applications
7. Searches Wikipedia
8. Retrieves Amazon stock price
9. Finds the location of a city
10. Greets according to the current time
11. Searches Google
12. Introduces itself
13. Sends emails
14. Opens websites
15. Tells jokes
16. Reads the latest news
17. Tells its age
18. Searches YouTube
19. Stops the program

---

# Motivation

Who doesn't want an assistant that listens to your commands and performs everyday tasks automatically?

AI-JARVIS is built as a real-world voice assistant application demonstrating speech recognition, desktop automation, APIs, and GUI development using Python.

---

## Run the application

## 1. Create a virtual environment

### Windows

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

```bash
python run.py
```

# Environment Variables

The project uses environment variables to configure sensitive information such as email credentials and API keys.

Create a file named `.env` in the project root.

Example:

```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
DEFAULT_RECEIVER=receiver@gmail.com
OPENWEATHER_API_KEY=your_openweathermap_api_key
```

You can use the provided `.env.example` file as a template.

**Note:** Never commit your `.env` file to version control.

---



## Directory Tree 
```
├── lib
    ├──a.png
    ├──b.png
    ├──dc.png
    ├──c.png
    ├──d.png
    ├──desktop.ini
    ├──exit.png
    ├──initiating system.png
    ├──iron man.png
    ├──jarvis.png
    ├──loading.gif
    ├──tuse.png
├── Material
    ├──jarvis_gif.gif
├──hahaha.wav
├──LICENSE
├──model.h5
├──README.md
├──rec.qrc
├──rec_rc.py
├──run.py
├──scifi.ui
```

---

# Technologies Used

- Python
- PyQt5
- SpeechRecognition
- pyttsx3
- BeautifulSoup4
- Geopy
- Yahoo Finance API
- OpenWeatherMap API
- Wikipedia API

---

# Bug / Feature Request

If you discover a bug or would like to request a new feature, please open an issue on the GitHub repository with:

- A clear description of the problem
- Steps to reproduce
- Expected behavior
- Screenshots (if applicable)

---

# Future Scope

- Implement additional Machine Learning and Deep Learning models
- Add more voice commands
- Improve GUI design
- Integrate gesture recognition and augmented reality
- Add cross-platform support

---
