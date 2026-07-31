# 🎙️ Voice & CLI-Driven System Virtual Assistant

A Python virtual assistant that takes commands **two ways** — spoken into a microphone or
typed at a command line — and answers with synthesized speech plus text. It fetches live
intelligence from the web, reads your machine's telemetry, and can drive OS-level actions.

Built for [Issue #1984](https://github.com/Niketkumardheeryan/ML-CaPsule/issues/1984).

---

## 🎯 Goal

Most assistant projects are a single long script that dies the moment a microphone,
speaker or API key is missing. This one is built the other way round:

* **Multi-modal** — the same command surface works over voice *and* the CLI.
* **Degrades instead of crashing** — every optional dependency (`pyttsx3`, `SpeechRecognition`,
  `wikipedia`, `psutil`, `pyautogui`, `pyperclip`) is imported lazily and has a fallback path.
  With none of them installed, the assistant still starts and answers in text.
* **Works with zero API keys** — weather comes from `wttr.in` and news from Google News RSS.
  Export `OPENWEATHER_API_KEY` / `NEWSAPI_KEY` and it upgrades to those providers automatically.
* **Safe by default** — shutdown / restart / logout sit behind two independent gates.
* **Testable** — the intent router and every parser are pure functions, covered by
  **43 offline unit tests**.

---

## ✨ Features

### 🗣️ Speech & NLP layer
- Time-of-day greetings (morning / afternoon / evening / night).
- Offline text-to-speech via `pyttsx3`; falls back to printed output.
- Microphone speech-to-text via `SpeechRecognition`; falls back to typed input.
- Optional wake word (`hey capsule …`), stripped during normalisation.

### 🌐 Web & knowledge integrations
- Wikipedia summaries, with a keyless REST fallback when the `wikipedia` package is absent
  and a readable message on disambiguation.
- Google search launched in the default browser.
- YouTube results opened for streaming.

### 📡 Live data orchestration
- Real-time weather for the configured city (**Jamshedpur** by default), or any city named
  in the command: `weather in Mumbai`.
- Top news headlines of the day, numbered for readability.

### 🖥️ System automation engine
- Clipboard read-back (`pyperclip`, with `pbpaste` / `xclip` / PowerShell fallbacks).
- Timestamped desktop screenshots — `screenshot_YYYYMMDD_HHMMSS.png`.
- Battery telemetry: percentage, charging state and estimated runtime remaining.

### ⚙️ OS-level control hooks
- Media playback through the platform's default player (`open` / `xdg-open` / `os.startfile`).
- Power controls (shutdown, restart, logout) for Windows, macOS and Linux — **guarded**, see below.

---

## 🔐 Safety model for destructive actions

Power commands are the one genuinely irreversible part of the assistant, so they are behind
two independent gates:

| Gate | Requirement | If unmet |
|:----:|-------------|----------|
| 1 | Opt in with `--allow-power` (or `ASSISTANT_ALLOW_POWER=1`) | The exact command that *would* run is reported; nothing executes |
| 2 | Type the action name to confirm | The request is cancelled |

```text
$ python main.py --no-tts --say "shutdown"
assistant > Power commands are disabled. Restart me with --allow-power to enable
            'shutdown' (it would run: osascript -e tell app "System Events" to shut down).

$ python main.py --no-tts --allow-power --say "restart"
Type 'restart' to confirm, anything else cancels: no
assistant > Cancelled the restart request.
```

Both gates are covered by unit tests that assert **no command is ever dispatched** unless
both are satisfied.

---

## 🛠️ Tech Stack

| Package | Role | Required? |
|---------|------|:---------:|
| `requests` | weather, news, Wikipedia REST fallback | ✅ |
| `pyttsx3` | offline text-to-speech | optional |
| `SpeechRecognition` | microphone speech-to-text | optional |
| `wikipedia` | Wikipedia summaries | optional |
| `psutil` | battery telemetry | optional |
| `pyautogui` | desktop screenshots | optional |
| `pyperclip` | clipboard access | optional |

Standard library only for everything else — `argparse`, `subprocess`, `webbrowser`,
`xml.etree`, `dataclasses`, `pathlib`.

---

## 🚀 Installation & Usage

```bash
cd Voice_CLI_Virtual_Assistant
pip install -r requirements.txt
```

> On Linux, `SpeechRecognition` also needs PyAudio (`sudo apt install python3-pyaudio portaudio19-dev`)
> and clipboard reads need `xclip`. Skip both if you only want the CLI mode.

```bash
python main.py                      # interactive text session
python main.py --voice              # interactive voice session (needs a microphone)
python main.py --say "weather"      # one-shot command, handy in scripts
python main.py --list-commands      # print the full command surface
python main.py --no-tts             # text only, no spoken output
python main.py --city Bengaluru     # override the default weather city
python main.py --allow-power        # enable guarded shutdown/restart/logout
```

### Configuration

Every setting has a default; all are overridable through the environment.

| Variable | Default | Purpose |
|----------|---------|---------|
| `ASSISTANT_CITY` | `Jamshedpur` | default city for weather |
| `ASSISTANT_WAKE_WORD` | `capsule` | optional wake word |
| `ASSISTANT_SCREENSHOT_DIR` | `~/Pictures` | where screenshots are written |
| `ASSISTANT_HEADLINES` | `5` | number of headlines to read |
| `ASSISTANT_NEWS_EDITION` | `IN` | Google News / NewsAPI edition |
| `ASSISTANT_TIMEOUT` | `10` | HTTP timeout in seconds |
| `ASSISTANT_ALLOW_POWER` | `0` | enable power commands |
| `OPENWEATHER_API_KEY` | *(unset)* | upgrade weather to OpenWeatherMap |
| `NEWSAPI_KEY` | *(unset)* | upgrade news to NewsAPI |

---

## 💬 Command surface

| Say / type | Intent | What happens |
|------------|--------|--------------|
| `hello`, `hi`, `namaste` | greet | time-aware greeting |
| `what is the time` | time | current clock time |
| `todays date` | date | today's date |
| `weather`, `weather in <city>` | weather | live weather report |
| `news`, `headlines` | news | top headlines of the day |
| `battery` | battery | charge %, state, runtime left |
| `screenshot` | screenshot | timestamped desktop capture |
| `clipboard` | clipboard | reads the copied text back |
| `system info` | system | host OS summary |
| `who is <topic>`, `tell me about <topic>` | wikipedia | Wikipedia summary |
| `google <query>` | google | opens Google results |
| `play <query>` | youtube | opens YouTube results |
| `play file <path>` | open_media | plays a local file |
| `shutdown`, `restart`, `log out` | power | guarded power controls |
| `help` | help | lists every command |
| `exit`, `quit`, `bye` | exit | ends the session |

---

## 📁 Project structure

```
Voice_CLI_Virtual_Assistant/
├── main.py                          # launcher
├── requirements.txt
├── assistant/
│   ├── __init__.py
│   ├── config.py                    # env-driven settings
│   ├── speech.py                    # TTS + STT with fallbacks
│   ├── knowledge.py                 # Wikipedia / Google / YouTube
│   ├── live_data.py                 # weather + news providers and parsers
│   ├── system_tools.py              # clipboard, screenshot, battery, media, power
│   ├── commands.py                  # intent router
│   ├── core.py                      # VirtualAssistant orchestration
│   └── cli.py                       # argument parsing and loops
├── tests/
│   └── test_assistant.py            # 43 offline unit tests
├── assets/
│   └── demo_session.txt             # recorded terminal session
└── voice_cli_assistant_demo.ipynb   # annotated walkthrough notebook
```

---

## 🧪 Tests

```bash
python -m unittest discover -s tests -v     # or: python -m pytest tests -q
```

```text
Ran 43 tests in 0.007s

OK
```

No microphone, browser or network access is required — the suite injects test doubles for
the browser opener, the power-command runner and the speech engine, and feeds the parsers
recorded payloads.

---

## 📸 Demo

Full recorded session: [`assets/demo_session.txt`](assets/demo_session.txt)
(live weather, live news and a real Wikipedia lookup included).

```text
$ python main.py --no-tts
assistant > Good morning! I am your ML-CaPsule assistant, listening in text mode. Say 'help' to see what I can do.
you > hello
assistant > Good morning! How can I help you?
you > battery
assistant > The battery is at 76 percent and on battery. About 7 hours and 41 minutes remaining.
you > what is the time
assistant > The time is 1:16 AM.
you > exit
assistant > Goodbye! Shutting down the assistant.
```

```text
$ python main.py --no-tts --say "weather"
assistant > Mist in Jamshedpur. It is 26 degrees Celsius and feels like 30, with 95% humidity and 4 kilometres per hour of wind.

$ python main.py --no-tts --say "news"
assistant > Here are the top 5 headlines.
1. 'Want To Forgive Them': PM Modi On Students Who Abused Him at Jantar Mantar - NDTV
2. Spain deploys military to Ceuta after migrant surge: What we know - Al Jazeera
...

$ python main.py --no-tts --say "who is Alan Turing"
assistant > According to Wikipedia: Alan Mathison Turing was an English mathematician, computer
scientist, logician, cryptanalyst, philosopher and theoretical biologist. ...

$ python main.py --no-tts --say "make me a sandwich"
assistant > I did not understand that. Say 'help' to see what I can do.
```

The graceful-degradation path, captured on a host without `pyautogui` and without Screen
Recording permission:

```text
$ python main.py --no-tts --say "take a screenshot"
assistant > Screen capture is unavailable. Install pyautogui, and on macOS grant your
            terminal Screen Recording permission in System Settings > Privacy & Security.
```

---

## 🔭 Future improvements

- Offline wake-word detection (Porcupine / Vosk) so voice mode needs no cloud STT.
- Intent classification with a small trained model instead of regex, to handle paraphrases.
- Alarms, reminders and a calendar integration.
- A plugin interface so new intents can be dropped in without touching the router.

---

## 👤 Author

Contributed to **ML-CaPsule** under **GSSoC** by [Anijesh](https://github.com/Anijesh) — resolves issue #1984.
