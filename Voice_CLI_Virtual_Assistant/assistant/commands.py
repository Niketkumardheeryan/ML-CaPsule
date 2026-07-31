"""Intent router.

An utterance (typed or transcribed) is normalised, matched against an ordered
list of regular expressions and dispatched to a handler. Keeping the router
separate from the I/O layers means the whole command surface can be unit tested
without a microphone, a browser or a network connection.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable

from . import knowledge, live_data, system_tools
from .speech import greeting_for, spoken_date, spoken_time

_PUNCTUATION = re.compile(r"[^\w\s:/\\.\-']")
_WHITESPACE = re.compile(r"\s+")


@dataclass
class Response:
    """What the assistant says back, plus loop control flags."""

    text: str
    handled: bool = True
    should_exit: bool = False


@dataclass
class Intent:
    """A named command with the patterns that trigger it."""

    name: str
    patterns: tuple[str, ...]
    handler: Callable[..., Response]
    help: str = ""
    compiled: tuple[re.Pattern, ...] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.compiled = tuple(re.compile(p, re.IGNORECASE) for p in self.patterns)

    def match(self, text: str) -> re.Match | None:
        """Return the first pattern match for ``text``, if any."""
        for pattern in self.compiled:
            found = pattern.search(text)
            if found:
                return found
        return None


def normalise(text: str, wake_word: str = "") -> str:
    """Lower-case, strip punctuation and drop a leading wake word."""
    cleaned = _PUNCTUATION.sub(" ", (text or "").lower())
    cleaned = _WHITESPACE.sub(" ", cleaned).strip()
    if wake_word:
        cleaned = re.sub(rf"^(?:hey\s+|ok\s+)?{re.escape(wake_word.lower())}\b[\s,]*",
                         "", cleaned).strip()
    return cleaned


# --------------------------------------------------------------- handlers
def handle_greet(assistant, match) -> Response:
    return Response(f"{greeting_for()}! How can I help you?")


def handle_time(assistant, match) -> Response:
    return Response(f"The time is {spoken_time()}.")


def handle_date(assistant, match) -> Response:
    return Response(f"Today is {spoken_date()}.")


def handle_wikipedia(assistant, match) -> Response:
    topic = (match.group("topic") or "").strip()
    if not topic:
        return Response("What should I look up on Wikipedia?")
    summary = knowledge.search_wikipedia(
        topic,
        sentences=assistant.config.wikipedia_sentences,
        timeout=assistant.config.request_timeout,
    )
    return Response(f"According to Wikipedia: {summary}")


def handle_google(assistant, match) -> Response:
    query = (match.group("query") or "").strip()
    if not query:
        return Response("What should I search for?")
    url = knowledge.search_google(query, opener=assistant.opener)
    return Response(f"Searching Google for {query}. Opened {url}")


def handle_youtube(assistant, match) -> Response:
    query = (match.group("query") or "").strip()
    if not query:
        return Response("Which video should I play?")
    url = knowledge.play_on_youtube(query, opener=assistant.opener)
    return Response(f"Opening YouTube results for {query}. Opened {url}")


TRAILING_FILLER = {"today", "now", "please", "tomorrow", "currently", "right", "there"}


def clean_city(raw: str) -> str:
    """Tidy a city captured from normalised (lower-cased) speech."""
    words = [word for word in raw.split() if word]
    while words and words[-1] in TRAILING_FILLER:
        words.pop()
    return " ".join(words).title()


def handle_weather(assistant, match) -> Response:
    city = clean_city(match.groupdict().get("city") or "") or assistant.config.city
    return Response(live_data.fetch_weather(city, assistant.config))


def handle_news(assistant, match) -> Response:
    headlines = live_data.fetch_headlines(assistant.config)
    return Response(live_data.format_headlines(headlines))


def handle_clipboard(assistant, match) -> Response:
    return Response(f"The clipboard says: {system_tools.read_clipboard()}")


def handle_screenshot(assistant, match) -> Response:
    _, message = system_tools.capture_screenshot(assistant.config)
    return Response(message)


def handle_battery(assistant, match) -> Response:
    status = system_tools.battery_status()
    if status is None:
        return Response("No battery was detected on this machine.")
    return Response(status.describe())


def handle_open_media(assistant, match) -> Response:
    path = (match.group("path") or "").strip()
    if not path:
        return Response("Tell me the path of the file you want to play.")
    _, message = system_tools.open_media(path)
    return Response(message)


def handle_system_info(assistant, match) -> Response:
    return Response(system_tools.system_summary())


def handle_power(assistant, match) -> Response:
    raw = match.group("action").lower().replace(" ", "")
    action = {
        "shutdown": "shutdown",
        "poweroff": "shutdown",
        "restart": "restart",
        "reboot": "restart",
        "logout": "logout",
        "signout": "logout",
        "logoff": "logout",
    }.get(raw, raw)
    _, message = system_tools.run_power_command(
        action, assistant.config, confirm=assistant.confirm
    )
    return Response(message)


def handle_help(assistant, match) -> Response:
    return Response(assistant.router.help_text())


def handle_exit(assistant, match) -> Response:
    return Response("Goodbye! Shutting down the assistant.", should_exit=True)


# ----------------------------------------------------------------- router
def default_intents() -> list[Intent]:
    """Return the built-in intents in priority order.

    Order matters: narrow patterns such as ``what is the time`` must be tried
    before the catch-all ``what is <topic>`` Wikipedia lookup.
    """
    return [
        Intent("exit", (r"^(?:exit|quit|stop|bye|goodbye|shut up)$",),
               handle_exit, "exit / quit / bye - close the assistant"),
        Intent("help", (r"^(?:help|commands|what can you do)\b",),
               handle_help, "help - list every supported command"),
        Intent("greet", (r"^(?:hello|hi|hey|namaste|good (?:morning|afternoon|evening))\b",),
               handle_greet, "hello - time aware greeting"),
        Intent("time", (r"\b(?:what(?:'s| is) the )?time\b(?! in)", r"^time$"),
               handle_time, "what is the time - current clock time"),
        Intent("date",
               (r"\b(?:today'?s date|what(?:'s| is) the date|which day is it)\b", r"^date$"),
               handle_date, "what is the date - today's date"),
        Intent("weather",
               (r"\b(?:weather|temperature|forecast)\b(?:\s+(?:in|at|for)\s+(?P<city>[\w\s]+))?",),
               handle_weather, "weather [in <city>] - live weather report"),
        Intent("news", (r"\b(?:news|headlines|top stories)\b",),
               handle_news, "news - top headlines of the day"),
        Intent("battery", (r"\b(?:battery|charge level|power level)\b",),
               handle_battery, "battery - charge percentage and time left"),
        Intent("screenshot", (r"\b(?:screenshot|screen shot|capture (?:the )?screen)\b",),
               handle_screenshot, "screenshot - timestamped desktop capture"),
        Intent("clipboard", (r"\b(?:clipboard|copied text|read clip)\b",),
               handle_clipboard, "clipboard - read back the copied text"),
        Intent("system", (r"\b(?:system info|system information|about this (?:pc|mac|system))\b",),
               handle_system_info, "system info - host operating system summary"),
        Intent("open_media", (r"^(?:play|open)\s+(?:file|media|song file)\s+(?P<path>.+)$",),
               handle_open_media, "play file <path> - open media in the default player"),
        Intent("power",
               (r"^(?P<action>shut ?down|power ?off|restart|reboot"
                r"|log ?out|sign ?out|log ?off)\b",),
               handle_power, "shutdown / restart / logout - guarded power controls"),
        Intent("youtube", (r"^(?:play|youtube|open youtube)\s+(?P<query>.+)$",),
               handle_youtube, "play <query> - stream the top YouTube result"),
        Intent("wikipedia",
               (r"^(?:wikipedia|search wikipedia for|look up)\s+(?P<topic>.+)$",
                r"^(?:who|what)(?:'s| is|are|was|were)\s+(?P<topic>.+)$",
                r"^tell me about\s+(?P<topic>.+)$"),
               handle_wikipedia, "who is <topic> - Wikipedia summary"),
        Intent("google", (r"^(?:google|search(?: for)?)\s+(?P<query>.+)$",),
               handle_google, "google <query> - open Google results"),
    ]


class CommandRouter:
    """Matches normalised text against intents and dispatches handlers."""

    def __init__(self, intents: list[Intent] | None = None) -> None:
        self.intents = intents if intents is not None else default_intents()

    def match(self, text: str) -> tuple[Intent, re.Match] | None:
        """Return the first matching ``(intent, match)`` pair, if any."""
        for intent in self.intents:
            found = intent.match(text)
            if found:
                return intent, found
        return None

    def dispatch(self, assistant, text: str) -> Response:
        """Route ``text`` to a handler and return its :class:`Response`."""
        if not text.strip():
            return Response("", handled=False)
        result = self.match(text)
        if result is None:
            return Response(
                "I did not understand that. Say 'help' to see what I can do.",
                handled=False,
            )
        intent, found = result
        return intent.handler(assistant, found)

    def help_text(self) -> str:
        """Return a readable list of every supported command."""
        lines = ["Here is what I can do:"]
        lines += [f"  - {intent.help}" for intent in self.intents if intent.help]
        return "\n".join(lines)


__all__ = [
    "CommandRouter",
    "Intent",
    "Response",
    "default_intents",
    "normalise",
]
