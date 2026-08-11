# 🤖 AI-JARVIS Voice Assistant

> An intelligent, Python-powered desktop voice assistant inspired by JARVIS, designed to automate everyday tasks, control desktop functions, retrieve real-time information, and provide an immersive futuristic GUI experience.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green?logo=qt)]
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🎬 **[Watch the Video Demo on YouTube](https://youtu.be/c5g8Q0sDR0g)**

---

## 📖 Overview

**AI-JARVIS** is a desktop-based voice assistant built with Python. It combines speech recognition, text-to-speech, web services, desktop automation, machine learning, and a Sci-Fi-inspired PyQt5 interface into a single interactive application.

The assistant is designed to understand natural voice commands and respond by performing actions such as:

* Launching desktop applications
* Searching the web
* Retrieving Wikipedia information
* Checking weather conditions
* Tracking stock prices
* Sending emails
* Playing music and YouTube content
* Reporting news headlines
* Providing entertainment such as jokes
* Performing location and geocoding operations
* Running cricket score and match prediction models
* Providing spoken responses through text-to-speech

---

## ✨ Features

### 🎙️ Voice Interaction

* Speech-to-text using `SpeechRecognition`
* Offline text-to-speech using `pyttsx3`
* Voice-driven command execution
* Context-aware greetings based on the time of day
* Spoken feedback for assistant actions

### 🖥️ Desktop & System Automation

* Launch installed applications
* Open websites directly
* Perform Google searches
* Control selected system functions
* Execute system shutdown commands
* Play local media files
* Interact with desktop resources through voice commands

### 🌐 Web & Information Retrieval

* Wikipedia summaries
* Google searches
* YouTube searches
* News headline retrieval
* Real-time weather information
* City and location lookup
* Geographical coordinates using Geopy

### 🌤️ Weather & Geolocation

Retrieve weather information such as:

* Temperature
* Current weather conditions
* Location information
* City coordinates

Weather data can be retrieved through the OpenWeather API.

### 📈 Financial Information

Track real-time market information using Yahoo Finance integrations.

Example supported queries include:

* Amazon stock price
* Apple stock price
* Other supported market symbols

### 🏏 Cricket Prediction

Cricket prediction support is planned, but the required model file (`model.h5`) is not included in this directory yet.

The model can be used for cricket-related predictions, including:

* Innings score prediction
* Match winner prediction

### 📧 Email Automation

Send emails using voice commands through Python's SMTP functionality.

The project supports secure credential configuration through environment variables.

> **Security recommendation:** Never hard-code email passwords or API keys directly into Python source files.

### 🎵 Media & Entertainment

* Play local music
* Open YouTube content
* Tell jokes
* Provide audio feedback
* Execute media-related commands through voice interaction

### 🧑‍💻 Sci-Fi GUI

The project includes a futuristic PyQt5 interface featuring:

* Animated interface elements
* JARVIS-inspired visual design
* Custom icons and graphics
* Loading animations
* Audio feedback
* Qt Designer UI integration

---

## 🛠️ Tech Stack

| Category             | Technology                  |
| -------------------- | --------------------------- |
| Programming Language | Python 3.9+                 |
| GUI                  | PyQt5                       |
| Speech Recognition   | SpeechRecognition           |
| Text-to-Speech       | pyttsx3                     |
| Web Scraping         | BeautifulSoup4              |
| Knowledge Retrieval  | Wikipedia                   |
| Geolocation          | Geopy                       |
| Financial Data       | Yahoo Finance / `yahoo_fin` |
| Email                | `smtplib`                   |
| Web Navigation       | `webbrowser`                |
| System Interaction   | `os`, `sys`                 |
| Audio                | `winsound`                  |
| ML/DL                | Pre-trained `model.h5`      |
| UI Design            | Qt Designer                 |

---

## 📋 Prerequisites

Before installing AI-JARVIS, make sure you have:

* **Python 3.9 or newer**
* A working microphone
* Speakers or headphones
* An internet connection for online features
* Required API credentials
* Windows for features that depend on `winsound` or Windows-specific application paths

> **Note:** Some system-control and audio functionality may require platform-specific adjustments when running on Linux or macOS.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI-JARVIS-VOICE-ASSISTANT.git
cd AI-JARVIS-VOICE-ASSISTANT
```

> Replace `your-username` with the actual GitHub repository owner.

---

## 2. Create a Virtual Environment

Using a virtual environment is strongly recommended.

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.\.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

## 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

AI-JARVIS uses environment variables for sensitive credentials and API keys.

Create a `.env` file in the root directory of the project.

```env
# Email Configuration
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_specific_password
DEFAULT_RECEIVER=receiver@gmail.com

# Weather API
OPENWEATHER_API_KEY=your_openweathermap_api_key
```

### Gmail Configuration

If you use Gmail for email automation:

1. Enable two-factor authentication on your Google account.
2. Generate a Google **App Password**.
3. Use the generated App Password as `EMAIL_PASSWORD`.
4. Do **not** use your normal Gmail account password.

### ⚠️ Never Commit Secrets

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

---

# ▶️ Running AI-JARVIS

Once the dependencies and environment variables are configured, start the application:

```bash
python run.py
```

After launching:

1. Wait for the Sci-Fi interface to initialize.
2. Ensure your microphone is enabled.
3. Speak clearly into the microphone.
4. AI-JARVIS will process your command.
5. The assistant will execute the requested action and respond using speech and/or the GUI.

---

# 🗣️ Example Voice Commands

You can interact with AI-JARVIS using natural voice commands.

### General

```text
"Hello Jarvis"
"What can you do?"
"Introduce yourself"
"What time is it?"
```

### Web Search

```text
"Search Google for Python tutorials"
"Search YouTube for relaxing music"
```

### Wikipedia

```text
"Who is Albert Einstein?"
"Tell me about artificial intelligence"
```

### Weather

```text
"What's the weather today?"
"What's the temperature?"
```

### Finance

```text
"What's Amazon's stock price?"
"Show me Apple's stock price"
```

### Email

```text
"Send an email"
"Send an email to ..."
```

### Entertainment

```text
"Tell me a joke"
"Play music"
"Open YouTube"
```

> Available commands depend on the functionality implemented in `run.py` and the configured services.

---

# 📁 Project Structure

```text
GUI-JARVIS-2026/
│
├── assets/
│   ├── lib/
│   │   ├── a.png
│   │   ├── b.png
│   │   ├── c.png
│   │   ├── d.png
│   │   ├── exit.png
│   │   ├── initiating system.gif
│   │   ├── iron man.png
│   │   ├── jarvis.png
│   │   ├── loading.gif
│   │   └── tuse.png
│   │
│   └── Material/
│       └── jarvis_gif.gif
│
├── src/
│   ├── backend/
│   │   ├── rec_rc.py
│   │   ├── rec.qrc
│   │   └── run.py
│   │
│   └── frontend/
│       └── scifi.ui
│
├── model.h5
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

### 📂 Directory & File Description

| Path | Description |
|---|---|
| `assets/` | Graphical assets, animations, icons, and UI media |
| `assets/lib/` | JARVIS interface images, icons, and animations |
| `assets/Material/` | Additional project media |
| `src/` | Main application source code |
| `src/backend/` | Backend and application logic |
| `src/backend/run.py` | Main application entry point |
| `src/backend/rec.qrc` | Qt resource collection |
| `src/backend/rec_rc.py` | Generated Python Qt resource module |
| `src/frontend/` | Frontend and GUI-related implementation |
| `model.h5` | Pre-trained machine learning/deep learning model |
| `.env.example` | Environment variable template |
| `.gitignore` | Git exclusion rules |
| `requirements.txt` | Python project dependencies |
| `README.md` | Project documentation |

> `__pycache__` and `.pyc` files are automatically generated by Python and are intentionally excluded from the project structure.
---

# 🧠 How It Works

At a high level, AI-JARVIS follows this workflow:

```text
┌──────────────────────┐
│      Microphone      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Speech Recognition  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Command Interpretation│
└──────────┬───────────┘
           │
     ┌─────┴─────┐
     │           │
     ▼           ▼
System Tasks   Web/API Tasks
     │           │
     └─────┬─────┘
           │
           ▼
┌──────────────────────┐
│    Task Execution    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Text-to-Speech (TTS) │
└──────────┬───────────┘
           │
           ▼
       User Output
```

---

# 🔧 Configuration Notes

## Microphone Permissions

Make sure your operating system allows Python or your terminal application to access the microphone.

If speech recognition does not work:

* Check the default recording device.
* Check operating-system microphone permissions.
* Make sure the microphone is not muted.
* Try speaking clearly and at a moderate distance.

## Internet Connection

Several features require an active internet connection, including:

* Weather
* Financial information
* Wikipedia
* Google searches
* YouTube
* News
* Some speech-recognition functionality

Offline functionality is therefore limited in the current version.

---

# 🐛 Troubleshooting

## `ModuleNotFoundError`

Make sure your virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

## Microphone Not Detected

Check your operating-system audio settings and verify that your microphone is available to Python.

## `.env` Variables Not Working

Verify that:

* The `.env` file is in the project root.
* Variable names match the expected names.
* There are no unnecessary quotation marks or spaces.
* API keys are valid.

## PyQt5 Errors

Try reinstalling PyQt5:

```bash
pip uninstall PyQt5
pip install PyQt5
```

## Audio/TTS Issues

Make sure:

* Your output device is configured correctly.
* `pyttsx3` is installed.
* Your operating system has a compatible speech engine.
* Required audio dependencies are available.

---

# 🗺️ Roadmap

AI-JARVIS can be expanded significantly in future versions.

* [ ] Integrate an LLM for advanced conversations
* [ ] Add OpenAI / Gemini-powered conversational intelligence
* [ ] Add offline speech recognition with Whisper or Vosk
* [ ] Improve natural-language command understanding
* [ ] Add wake-word detection
* [ ] Add vision capabilities using OpenCV
* [ ] Add gesture recognition
* [ ] Add smart-home / IoT integration
* [ ] Add calendar and reminder management
* [ ] Add WhatsApp or messaging integrations
* [ ] Improve cross-platform support
* [ ] Create Windows installer packages
* [ ] Add persistent user preferences
* [ ] Add plugin-based command architecture
* [ ] Improve security and credential management

---

# 🤝 Contributing

Contributions, suggestions, bug reports, and feature requests are welcome!

## Reporting Bugs

When opening an issue, include:

1. Operating system
2. Python version
3. Steps to reproduce the issue
4. Expected behavior
5. Actual behavior
6. Error messages or logs
7. Screenshots, if applicable

## Feature Requests

Describe:

* The proposed feature
* Why it would be useful
* How it could integrate with the existing assistant

## Pull Requests

1. Fork the repository.

2. Clone your fork:

```bash
git clone https://github.com/your-username/AI-JARVIS-VOICE-ASSISTANT.git
```

3. Create a feature branch:

```bash
git checkout -b feature/amazing-feature
```

4. Make your changes.

5. Commit your changes:

```bash
git add .
git commit -m "Add amazing feature"
```

6. Push your branch:

```bash
git push origin feature/amazing-feature
```

7. Open a Pull Request.

---

# 🔒 Security

Please do not commit sensitive information to the repository.

Never commit:

```text
.env
API keys
Email passwords
SMTP credentials
Private tokens
Personal configuration files
```

Use `.env.example` to document the required variables without exposing real credentials.

---

# 📜 License

This project is available under the **MIT License**.

See the [`LICENSE`](LICENSE) file for details.

---

# 👨‍💻 Author

Developed as a Python-based personal AI assistant project combining:

* Voice interaction
* Desktop automation
* Web APIs
* Machine learning
* GUI development
* Automation

---

# ⭐ Support the Project

If you find AI-JARVIS useful or interesting:

* ⭐ Star the repository
* 🍴 Fork the project
* 🐛 Report bugs
* 💡 Suggest features
* 🔧 Submit pull requests
* 📢 Share the project

---

## 🎬 Demo

Watch AI-JARVIS in action:

**[▶️ Watch the Video Demo on YouTube](https://youtu.be/c5g8Q0sDR0g)**

---

> **AI-JARVIS — Bringing a futuristic voice assistant experience to the desktop with Python.** 🤖
