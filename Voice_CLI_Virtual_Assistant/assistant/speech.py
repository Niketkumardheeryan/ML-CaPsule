"""Speech layer: offline text-to-speech plus microphone speech-to-text.

Both capabilities are optional. ``pyttsx3`` and ``SpeechRecognition`` are
imported lazily so the assistant still starts on a head-less machine, inside a
container, or on a laptop without a microphone -- it simply degrades to plain
text output and keyboard input.
"""

from __future__ import annotations

import sys
from datetime import datetime

MORNING_END = 12
AFTERNOON_END = 17
NIGHT_START = 21


def greeting_for(moment: datetime | None = None) -> str:
    """Return a time-of-day greeting for ``moment`` (defaults to now)."""
    hour = (moment or datetime.now()).hour
    if hour < MORNING_END:
        return "Good morning"
    if hour < AFTERNOON_END:
        return "Good afternoon"
    if hour < NIGHT_START:
        return "Good evening"
    return "Good night"


def spoken_time(moment: datetime | None = None) -> str:
    """Return the current clock time in a form that reads well aloud."""
    return (moment or datetime.now()).strftime("%I:%M %p").lstrip("0")


def spoken_date(moment: datetime | None = None) -> str:
    """Return today's date in a form that reads well aloud."""
    now = moment or datetime.now()
    return f"{now.strftime('%A')}, {now.day} {now.strftime('%B %Y')}"


class SpeechEngine:
    """Wraps TTS/STT and always keeps a usable text fallback."""

    def __init__(self, config, enable_tts: bool = True, enable_stt: bool = False,
                 stream=None) -> None:
        self.config = config
        self.enable_tts = enable_tts
        self.enable_stt = enable_stt
        self.stream = stream or sys.stdout
        self._tts_engine = None
        self._tts_failed = False
        self._recognizer = None
        self._microphone = None
        self._stt_failed = False

    # ------------------------------------------------------------------ TTS
    @property
    def tts_available(self) -> bool:
        """True when a speech synthesiser could be initialised."""
        return self.enable_tts and not self._tts_failed and self._ensure_tts() is not None

    def _ensure_tts(self):
        if self._tts_engine is not None or self._tts_failed:
            return self._tts_engine
        try:
            import pyttsx3  # imported lazily: needs a system speech driver

            engine = pyttsx3.init()
            engine.setProperty("rate", self.config.speech_rate)
            engine.setProperty("volume", self.config.speech_volume)
            self._tts_engine = engine
        except Exception:  # pragma: no cover - depends on host audio stack
            self._tts_failed = True
            self._tts_engine = None
        return self._tts_engine

    def speak(self, text: str) -> str:
        """Print ``text`` and, when possible, say it out loud."""
        if not text:
            return ""
        print(f"assistant > {text}", file=self.stream)
        if self.enable_tts and not self._tts_failed:
            engine = self._ensure_tts()
            if engine is not None:
                try:
                    engine.say(text)
                    engine.runAndWait()
                except Exception:  # pragma: no cover - host audio stack
                    # One failure is enough: fall back to text for the session.
                    self._tts_failed = True
        return text

    # ------------------------------------------------------------------ STT
    @property
    def stt_available(self) -> bool:
        """True when a microphone and recogniser could be initialised."""
        return self.enable_stt and not self._stt_failed and self._ensure_stt()

    def _ensure_stt(self) -> bool:
        if self._stt_failed:
            return False
        if self._recognizer is not None:
            return True
        try:
            import speech_recognition as sr  # lazily imported: needs PyAudio

            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            recognizer.dynamic_energy_threshold = True
            self._recognizer = recognizer
            self._microphone = microphone
            return True
        except Exception:  # pragma: no cover - depends on host audio stack
            self._stt_failed = True
            return False

    def listen(self, prompt: str = "you > ", timeout: float = 6.0,
               phrase_limit: float = 8.0) -> str:
        """Return a transcribed utterance, or typed text when audio is absent."""
        if not self.stt_available:
            return self._read_line(prompt)

        import speech_recognition as sr

        try:
            with self._microphone as source:
                print("listening...", file=self.stream)
                self._recognizer.adjust_for_ambient_noise(source, duration=0.4)
                audio = self._recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_limit
                )
            heard = self._recognizer.recognize_google(audio)
            print(f"you (voice) > {heard}", file=self.stream)
            return heard
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            self.speak("Sorry, I did not catch that.")
            return ""
        except Exception:  # pragma: no cover - network or driver failure
            self.speak("Voice input is unavailable, switching to typed input.")
            self._stt_failed = True
            return self._read_line(prompt)

    def _read_line(self, prompt: str) -> str:
        try:
            line = input(prompt)
        except EOFError:
            return "exit"
        except KeyboardInterrupt:
            print(file=self.stream)
            return "exit"
        if not sys.stdin.isatty():
            # Echo piped input so scripted sessions and logs stay readable.
            print(line, file=self.stream)
        return line
