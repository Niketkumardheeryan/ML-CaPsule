"""
Speech & NLP Layer for Voice & CLI Virtual Assistant.
Provides dynamic time-of-day greetings, Text-to-Speech (TTS) synthesis via pyttsx3,
and Speech-to-Text processing via SpeechRecognition with seamless CLI fallback.
"""

from datetime import datetime
import sys


def get_greeting(hour: int = None) -> str:
    """
    Returns a dynamic time-of-day greeting based on local hour (0-23).

    Args:
        hour (int, optional): Explicit hour value for testing or custom time. Defaults to current system hour.

    Returns:
        str: Time-appropriate greeting string.
    """
    if hour is None:
        hour = datetime.now().hour

    if 4 <= hour < 12:
        return "Good morning! How can I assist you today?"
    elif 12 <= hour < 17:
        return "Good afternoon! How can I assist you today?"
    elif 17 <= hour < 22:
        return "Good evening! How can I assist you today?"
    else:
        return "Good night! How can I assist you today?"


def safe_print(text: str, **kwargs) -> None:
    """Prints text safely across all terminal encodings (e.g. CP1252 on Windows)."""
    try:
        print(text, **kwargs)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", "ascii") or "ascii"
        clean_text = str(text).encode(encoding, errors="replace").decode(encoding)
        print(clean_text, **kwargs)


class TTSManager:
    """
    Text-to-Speech synthesis manager using pyttsx3.
    Includes graceful fallbacks for environments without active sound drivers.
    """

    def __init__(self, rate: int = 175, volume: float = 1.0, silent: bool = False):
        self.silent = silent
        self.engine = None
        if not self.silent:
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", rate)
                self.engine.setProperty("volume", volume)
            except Exception as e:
                safe_print(f"[TTS Warning] Could not initialize pyttsx3 engine: {e}. Falling back to text output.")
                self.engine = None

    def speak(self, text: str) -> None:
        """
        Synthesizes speech for the provided text. Always prints to console safely.
        """
        safe_print(f"\n🤖 Assistant: {text}")
        if self.silent or self.engine is None:
            return

        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            safe_print(f"[TTS Error] Speech synthesis failed: {e}")


class SpeechRecognizerManager:
    """
    Speech-to-Text manager using SpeechRecognition with automatic fallback to text input.
    Lazy-initializes microphone audio sources on demand.
    """

    def __init__(self):
        self.sr = None
        self.recognizer = None
        self.microphone = None
        try:
            import speech_recognition as sr
            self.sr = sr
            self.recognizer = sr.Recognizer()
        except Exception as e:
            safe_print(f"[Voice Warning] Speech recognition setup failed ({e}). Defaulting to CLI input.")

    def listen(self, timeout: int = 5, phrase_time_limit: int = 5) -> str:
        """
        Listens to microphone input and converts speech to text.
        Falls back to standard keyboard CLI prompt if speech recognition fails or microphone is unavailable.

        Returns:
            str: Recognized speech string or user CLI input.
        """
        if not self.recognizer or not self.sr:
            return self._cli_fallback()

        if self.microphone is None:
            try:
                self.microphone = self.sr.Microphone()
            except Exception as e:
                safe_print(f"[Voice Warning] Microphone setup failed ({e}). Defaulting to CLI input.")
                return self._cli_fallback()

        try:
            safe_print("\n🎙️  Listening... Speak into your microphone:")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

            safe_print("🧠 Processing speech...")
            query = self.recognizer.recognize_google(audio)
            safe_print(f"👤 You (Voice): {query}")
            return query
        except self.sr.WaitTimeoutError:
            safe_print("[Voice Alert] Listening timed out. No speech detected.")
            return self._cli_fallback()
        except self.sr.UnknownValueError:
            safe_print("[Voice Alert] Could not understand the audio.")
            return self._cli_fallback()
        except self.sr.RequestError as e:
            safe_print(f"[Voice Alert] Speech service request failed: {e}")
            return self._cli_fallback()
        except Exception as e:
            safe_print(f"[Voice Alert] Audio capture error ({e}).")
            return self._cli_fallback()

    def _cli_fallback(self) -> str:
        """Fallback to CLI prompt input."""
        try:
            safe_print("\n👤 You (CLI Input): ", end="")
            return input().strip()
        except (EOFError, KeyboardInterrupt):
            return "exit"
