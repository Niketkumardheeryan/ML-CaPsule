"""
Virtual Assistant Core Orchestration Engine.
Integrates speech, NLP, web intelligence, live data, system automation, and OS control hooks into a single unified assistant.
"""

from typing import Tuple
from .speech_engine import get_greeting, TTSManager, SpeechRecognizerManager, safe_print
from .web_engine import search_wikipedia, search_google, play_youtube
from .live_data_engine import get_weather, get_top_news
from .system_engine import read_clipboard, take_screenshot, get_battery_telemetry
from .os_control import open_media, power_command


class VirtualAssistant:
    """
    Core Virtual Assistant class coordinating input processing, execution, and speech feedback.
    """

    def __init__(self, silent: bool = False, default_city: str = "Jamshedpur"):
        self.tts = TTSManager(silent=silent)
        self.speech_rec = SpeechRecognizerManager()
        self.default_city = default_city
        self.running = True

    def greet_user(self) -> str:
        """Generates dynamic time-of-day greeting and speaks it."""
        greeting = get_greeting()
        self.tts.speak(greeting)
        return greeting

    def process_command(self, command_str: str, confirm_power: bool = False) -> Tuple[str, bool]:
        """
        Parses intent from the input command string and executes the matching subsystem hook.

        Args:
            command_str (str): Raw input command string.
            confirm_power (bool): Whether to confirm administrative power commands.

        Returns:
            Tuple[str, bool]: Response message and flag indicating if assistant should continue running (True) or exit (False).
        """
        if not command_str or not command_str.strip():
            return "No command received. Type 'help' for available commands.", True

        cmd = command_str.strip().lower()

        # Exit commands
        if cmd in ["exit", "quit", "bye", "goodbye", "stop"]:
            self.running = False
            response = "Goodbye! Have a great day."
            self.tts.speak(response)
            return response, False

        # Greeting intent
        if any(keyword in cmd for keyword in ["greet", "greeting", "hello", "hi", "hey"]):
            greeting = get_greeting()
            self.tts.speak(greeting)
            return greeting, True

        # Weather intent
        if "weather" in cmd:
            city = self.default_city
            if "in " in cmd:
                city = cmd.split("in ", 1)[1].strip()
            elif "for " in cmd:
                city = cmd.split("for ", 1)[1].strip()

            result = get_weather(city=city)
            self.tts.speak(result)
            return result, True

        # News intent
        if any(keyword in cmd for keyword in ["news", "headline", "headlines"]):
            result = get_top_news(limit=5)
            self.tts.speak(result)
            return result, True

        # Battery telemetry intent
        if any(keyword in cmd for keyword in ["battery", "power status", "charging", "battery status"]):
            result = get_battery_telemetry()
            self.tts.speak(result)
            return result, True

        # Clipboard intent
        if "clipboard" in cmd or "read clip" in cmd:
            result = read_clipboard()
            self.tts.speak(result)
            return result, True

        # Screenshot intent
        if any(keyword in cmd for keyword in ["screenshot", "snapshot", "screen capture", "capture screen"]):
            result = take_screenshot()
            self.tts.speak(result)
            return result, True

        # Wikipedia search intent
        if cmd.startswith("wikipedia") or cmd.startswith("wiki ") or "search wikipedia" in cmd:
            query = cmd.replace("search wikipedia", "").replace("wikipedia", "").replace("wiki", "").strip()
            result = search_wikipedia(query)
            self.tts.speak(result)
            return result, True

        # YouTube intent
        if cmd.startswith("youtube") or cmd.startswith("play ") or "search youtube" in cmd:
            query = cmd.replace("search youtube", "").replace("youtube", "").replace("play", "").strip()
            result = play_youtube(query)
            self.tts.speak(result)
            return result, True

        # Google search intent
        if cmd.startswith("google") or cmd.startswith("search ") or "search google" in cmd:
            query = cmd.replace("search google", "").replace("google", "").replace("search", "").strip()
            result = search_google(query)
            self.tts.speak(result)
            return result, True

        # OS Open Media/App intent
        if cmd.startswith("open ") or cmd.startswith("launch "):
            target = cmd.replace("open", "", 1).replace("launch", "", 1).strip()
            result = open_media(target)
            self.tts.speak(result)
            return result, True

        # OS Power actions (logout, restart, shutdown)
        for power_act in ["shutdown", "restart", "logout"]:
            if power_act in cmd:
                result = power_command(power_act, confirm=confirm_power)
                self.tts.speak(result)
                return result, True

        # General question fallback -> Try Wikipedia first or Google search
        if cmd.startswith("who is") or cmd.startswith("what is") or cmd.startswith("tell me about"):
            query = cmd.replace("who is", "").replace("what is", "").replace("tell me about", "").strip()
            result = search_wikipedia(query)
            self.tts.speak(result)
            return result, True

        # Help menu intent
        if cmd in ["help", "commands", "menu", "?", "--help"]:
            help_text = self.get_help_menu()
            safe_print(f"\n{help_text}")
            return help_text, True

        # Unrecognized fallback
        fallback_msg = f"Unknown command: '{command_str}'. Searching Google..."
        safe_print(f"\n🤖 {fallback_msg}")
        search_res = search_google(command_str)
        return search_res, True

    @staticmethod
    def get_help_menu() -> str:
        """Returns assistant available command capabilities menu."""
        return (
            "===========================================================\n"
            "🤖 VOICE & CLI SYSTEM VIRTUAL ASSISTANT - COMMAND MANUAL\n"
            "===========================================================\n"
            "• Greeting           : 'hello', 'hi', 'greeting'\n"
            "• Weather Indexing   : 'weather', 'weather in Jamshedpur', 'weather in Mumbai'\n"
            "• Live Top News      : 'news', 'headlines'\n"
            "• Battery Telemetry  : 'battery', 'battery status'\n"
            "• Clipboard Reader   : 'clipboard', 'read clipboard'\n"
            "• Screen Capture     : 'screenshot', 'capture screen'\n"
            "• Wikipedia Search   : 'wiki Python', 'who is Albert Einstein', 'what is Machine Learning'\n"
            "• Google Search      : 'google ML-CaPsule repository', 'search Python tutorials'\n"
            "• YouTube Streaming  : 'youtube lofi music', 'play machine learning tutorial'\n"
            "• Open Media / App   : 'open notepad.exe', 'launch calc.exe'\n"
            "• Power Controls     : 'logout', 'restart', 'shutdown'\n"
            "• Help / Exit        : 'help', 'exit', 'quit'\n"
            "==========================================================="
        )
