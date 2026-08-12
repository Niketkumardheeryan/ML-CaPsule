# 🎙️ Voice & CLI-Driven System Virtual Assistant

A multi-modal, Python-based Virtual Assistant designed to perform automated system operations, fetch live web intelligence, monitor device hardware telemetry, and process user requests via **Speech Recognition (Voice)** and a standard **Command-Line Interface (CLI)**.

---

## 🌟 Key Blueprint Features

### 1. 🗣️ Speech & NLP Layer
* **Dynamic Time-of-Day Greetings**: Context-aware greetings (`Good morning`, `Good afternoon`, `Good evening`, `Good night`) derived from system clock telemetry.
* **Text-to-Speech (TTS) Synthesis**: Offline voice synthesis utilizing `pyttsx3` with console printing and audio driver fallback.
* **Speech-to-Text Processing**: Voice recognition using `speech_recognition` microphone input decoding with automated CLI input fallback.

### 2. 🌐 Web & Knowledge Integrations
* **On-Demand Wikipedia Summaries**: Fast query lookup summarizing key topics with exception safety for disambiguation and page errors.
* **Automated Google Search**: Instant query launcher opening search queries in the default web browser.
* **Direct YouTube Streaming**: Direct video search and playback link launching.

### 3. 📊 Live Data Orchestration
* **Localized Weather Indexing**: Real-time weather index for **Jamshedpur** (and customizable locations) reporting temperature, conditions, humidity, and wind speed.
* **Live News Parsing**: Top headlines parser extracting live news updates from open RSS feeds.

### 4. ⚙️ System Automation Engine
* **Clipboard Reader**: Instant inspection and text extraction from the system clipboard.
* **Timestamped Desktop Screen Capturing**: Automatic desktop screenshots saved with timestamped filenames (`screenshot_YYYYMMDD_HHMMSS.png`).
* **Live Battery Telemetry**: Real-time battery status monitoring reporting charge percentage, power connection state, and time remaining.

### 5. 🛠️ OS-Level Control Hooks
* **Subprocess App / Media Execution**: Cross-platform system file and app launcher (`os.startfile` / `subprocess`).
* **Administrative Power Commands**: Power options (`logout`, `restart`, `shutdown`) equipped with safety confirmation guards (`--confirm`) to prevent accidental invocation.

---

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| `Python 3.8+` | Core programming language |
| `pyttsx3` | Offline Text-to-Speech synthesis engine |
| `SpeechRecognition` | Microphone audio decoding and speech parsing |
| `wikipedia` & `requests` | API querying, web intelligence, and live data extraction |
| `pyautogui` & `psutil` | Desktop automation, screenshot capture, and hardware telemetry |
| `pyperclip` | Clipboard text integration |
| `pytest` | Automated test suite execution |

---

## 📁 Project Structure

```text
Voice_CLI_Virtual_Assistant/
│
├── src/
│   ├── __init__.py           # Package initialization
│   ├── speech_engine.py      # Greetings, TTSManager, SpeechRecognizerManager
│   ├── web_engine.py         # Wikipedia, Google search, YouTube playback
│   ├── live_data_engine.py   # Live weather (Jamshedpur) & top news parser
│   ├── system_engine.py     # Clipboard reader, screenshot, battery telemetry
│   ├── os_control.py        # Media launch & OS power controls (shutdown/restart/logout)
│   ├── assistant.py         # Core VirtualAssistant orchestrator & intent processor
│   └── cli.py               # Command-line interface & argument parser
│
├── tests/
│   └── test_virtual_assistant.py  # Unit and integration tests
│
├── main.py                   # Application entry point
├── README.md                 # Project documentation
└── requirements.txt          # Package dependencies
```

---

## 🚀 Quickstart Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Single Command Mode
```bash
python main.py --cmd "greeting"
python main.py --cmd "weather Jamshedpur"
python main.py --cmd "battery"
python main.py --cmd "news"
python main.py --cmd "wiki Python"
```

### 3. Run Interactive CLI Mode
```bash
python main.py --mode cli
```

### 4. Run Voice Microphone Mode
```bash
python main.py --mode voice
```

### 5. Run with Muted Audio (Silent Mode)
```bash
python main.py --mode cli --silent
```

---

## 💻 Command Reference Cheat-Sheet

| Category | Example Commands |
| :--- | :--- |
| **Greeting** | `hello`, `hi`, `greeting` |
| **Weather** | `weather`, `weather in Jamshedpur`, `weather in Delhi` |
| **News** | `news`, `top headlines` |
| **Battery Telemetry** | `battery`, `battery status` |
| **Clipboard** | `clipboard`, `read clipboard` |
| **Screenshot** | `screenshot`, `capture screen` |
| **Wikipedia** | `wiki Machine Learning`, `who is Isaac Newton` |
| **Google Search** | `google open source projects`, `search python documentation` |
| **YouTube Streaming** | `youtube lofi beats`, `play tutorial` |
| **App Execution** | `open notepad.exe`, `launch calc.exe` |
| **OS Power Guard** | `logout`, `restart`, `shutdown` *(Requires `--confirm` flag)* |
| **Control** | `help`, `exit`, `quit` |

---

## 🧪 Running Automated Tests

Run the test suite using `pytest`:
```bash
pytest tests/
```

---

## 📜 License
Part of the **ML-CaPsule** repository under the MIT License.
