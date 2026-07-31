"""Unit tests for the virtual assistant.

The suite runs completely offline: no microphone, no browser and no network
call is made. Run it with either of:

    python -m unittest discover -s tests -v
    python -m pytest tests -q
"""

from __future__ import annotations

import os
import sys
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from assistant import commands, knowledge, live_data, system_tools  # noqa: E402
from assistant.config import AssistantConfig, load_config  # noqa: E402
from assistant.core import VirtualAssistant  # noqa: E402
from assistant.speech import greeting_for, spoken_date, spoken_time  # noqa: E402


class RecordingSpeech:
    """Speech double that records what would have been spoken."""

    def __init__(self) -> None:
        self.spoken: list[str] = []
        self.enable_stt = False
        self.stt_available = False

    def speak(self, text: str) -> str:
        self.spoken.append(text)
        return text


def build_assistant(**overrides) -> tuple[VirtualAssistant, list[str], RecordingSpeech]:
    """Return an assistant wired to test doubles instead of real I/O."""
    opened: list[str] = []
    speech = RecordingSpeech()
    config = AssistantConfig(city="Jamshedpur", wake_word="capsule", **overrides)
    assistant = VirtualAssistant(
        config=config,
        speech=speech,
        opener=opened.append,
        confirm=lambda action: False,
    )
    return assistant, opened, speech


class GreetingTests(unittest.TestCase):
    def test_greeting_changes_with_time_of_day(self):
        self.assertEqual(greeting_for(datetime(2026, 8, 1, 8, 0)), "Good morning")
        self.assertEqual(greeting_for(datetime(2026, 8, 1, 13, 0)), "Good afternoon")
        self.assertEqual(greeting_for(datetime(2026, 8, 1, 19, 0)), "Good evening")
        self.assertEqual(greeting_for(datetime(2026, 8, 1, 23, 0)), "Good night")

    def test_spoken_time_has_no_leading_zero(self):
        self.assertEqual(spoken_time(datetime(2026, 8, 1, 9, 5)), "9:05 AM")

    def test_spoken_date_is_readable(self):
        self.assertEqual(spoken_date(datetime(2026, 8, 1)), "Saturday, 1 August 2026")


class NormaliseTests(unittest.TestCase):
    def test_punctuation_and_case_are_removed(self):
        self.assertEqual(commands.normalise("What's the TIME??"), "what's the time")

    def test_wake_word_is_stripped(self):
        self.assertEqual(commands.normalise("Hey Capsule, battery", "capsule"), "battery")
        self.assertEqual(commands.normalise("capsule news", "capsule"), "news")

    def test_wake_word_inside_sentence_is_kept(self):
        self.assertEqual(commands.normalise("what is a capsule", "capsule"),
                         "what is a capsule")


class RouterTests(unittest.TestCase):
    def setUp(self):
        self.router = commands.CommandRouter()

    def assert_intent(self, utterance: str, expected: str):
        result = self.router.match(commands.normalise(utterance, "capsule"))
        self.assertIsNotNone(result, f"no intent matched {utterance!r}")
        self.assertEqual(result[0].name, expected, f"wrong intent for {utterance!r}")

    def test_utterances_route_to_the_expected_intent(self):
        cases = {
            "hello there": "greet",
            "what is the time": "time",
            "today's date": "date",
            "what is the weather": "weather",
            "weather in Mumbai": "weather",
            "read me the news": "news",
            "battery status": "battery",
            "take a screenshot": "screenshot",
            "read my clipboard": "clipboard",
            "system info": "system",
            "play file ~/Music/song.mp3": "open_media",
            "shutdown": "power",
            "log out": "power",
            "play shape of you": "youtube",
            "who is Alan Turing": "wikipedia",
            "tell me about neural networks": "wikipedia",
            "google best ML projects": "google",
            "help": "help",
            "exit": "exit",
        }
        for utterance, expected in cases.items():
            with self.subTest(utterance=utterance):
                self.assert_intent(utterance, expected)

    def test_time_intent_wins_over_wikipedia_lookup(self):
        # "what is ..." is also the Wikipedia trigger, so ordering matters.
        self.assert_intent("what is the time", "time")

    def test_media_playback_wins_over_youtube(self):
        self.assert_intent("play file /tmp/clip.mp4", "open_media")

    def test_unknown_command_is_reported_but_not_fatal(self):
        assistant, _, _ = build_assistant()
        response = assistant.handle("make me a sandwich")
        self.assertFalse(response.handled)
        self.assertIn("did not understand", response.text)

    def test_empty_input_is_ignored(self):
        assistant, _, _ = build_assistant()
        self.assertFalse(assistant.handle("   ").handled)

    def test_help_lists_every_documented_command(self):
        text = self.router.help_text()
        for intent in self.router.intents:
            if intent.help:
                self.assertIn(intent.help, text)

    def test_exit_sets_the_exit_flag(self):
        assistant, _, _ = build_assistant()
        self.assertTrue(assistant.handle("bye").should_exit)


class BrowserIntentTests(unittest.TestCase):
    def test_google_opens_the_expected_url(self):
        assistant, opened, _ = build_assistant()
        assistant.handle("google machine learning")
        self.assertEqual(opened, ["https://www.google.com/search?q=machine+learning"])

    def test_youtube_opens_the_expected_url(self):
        assistant, opened, _ = build_assistant()
        assistant.handle("play lofi beats")
        self.assertEqual(
            opened, ["https://www.youtube.com/results?search_query=lofi+beats"]
        )

    def test_url_builders_escape_special_characters(self):
        self.assertEqual(
            knowledge.google_search_url("c++ & python"),
            "https://www.google.com/search?q=c%2B%2B+%26+python",
        )

    def test_trim_sentences_respects_the_limit(self):
        text = "One. Two. Three. Four."
        self.assertEqual(knowledge.trim_sentences(text, 2), "One. Two.")
        self.assertEqual(knowledge.trim_sentences(text, 0), text)


class WeatherParsingTests(unittest.TestCase):
    def test_wttr_payload_is_parsed(self):
        payload = {
            "current_condition": [
                {
                    "temp_C": "29",
                    "FeelsLikeC": "33",
                    "humidity": "74",
                    "windspeedKmph": "11",
                    "weatherDesc": [{"value": "Partly cloudy"}],
                }
            ]
        }
        report = live_data.parse_wttr_payload(payload, "Jamshedpur")
        self.assertEqual(report.temperature_c, 29)
        self.assertEqual(report.humidity, 74)
        self.assertIn("Partly cloudy in Jamshedpur", report.describe())
        self.assertIn("29 degrees Celsius", report.describe())

    def test_openweather_payload_converts_wind_to_kmph(self):
        payload = {
            "name": "Jamshedpur",
            "weather": [{"description": "light rain"}],
            "main": {"temp": 27.4, "feels_like": 30.1, "humidity": 88},
            "wind": {"speed": 5},
        }
        report = live_data.parse_openweather_payload(payload, "Jamshedpur")
        self.assertAlmostEqual(report.wind_kmph, 18.0)
        self.assertIn("Light rain in Jamshedpur", report.describe())

    def test_malformed_payload_does_not_raise(self):
        report = live_data.parse_wttr_payload({}, "Nowhere")
        self.assertEqual(report.temperature_c, 0.0)
        self.assertIn("Nowhere", report.describe())


class CityParsingTests(unittest.TestCase):
    def test_city_is_title_cased_after_normalisation(self):
        self.assertEqual(commands.clean_city("new delhi"), "New Delhi")

    def test_trailing_filler_words_are_dropped(self):
        self.assertEqual(commands.clean_city("mumbai today please"), "Mumbai")

    def test_empty_city_falls_back_to_the_configured_default(self):
        assistant, _, _ = build_assistant()
        match = commands.CommandRouter().match("what is the weather")
        self.assertIsNotNone(match)
        self.assertEqual(commands.clean_city(match[1].groupdict().get("city") or ""), "")


class NewsParsingTests(unittest.TestCase):
    RSS = """<?xml version="1.0"?>
    <rss version="2.0"><channel>
      <item><title>First headline</title></item>
      <item><title>Second headline</title></item>
      <item><title>Third headline</title></item>
    </channel></rss>"""

    def test_rss_titles_are_extracted_up_to_the_limit(self):
        self.assertEqual(
            live_data.parse_news_rss(self.RSS, limit=2),
            ["First headline", "Second headline"],
        )

    def test_invalid_xml_returns_no_headlines(self):
        self.assertEqual(live_data.parse_news_rss("not xml at all"), [])

    def test_headlines_are_numbered(self):
        formatted = live_data.format_headlines(["A", "B"])
        self.assertIn("1. A", formatted)
        self.assertIn("2. B", formatted)

    def test_empty_headlines_produce_a_friendly_message(self):
        self.assertIn("could not fetch", live_data.format_headlines([]))


class SystemToolTests(unittest.TestCase):
    def test_screenshot_filename_is_timestamped(self):
        name = system_tools.screenshot_filename(datetime(2026, 8, 1, 14, 30, 5))
        self.assertEqual(name, "screenshot_20260801_143005.png")

    def test_battery_description_includes_state_and_runtime(self):
        status = system_tools.BatteryStatus(percent=76.4, plugged=False, seconds_left=5400)
        described = status.describe()
        self.assertIn("76 percent", described)
        self.assertIn("on battery", described)
        self.assertIn("1 hours and 30 minutes", described)

    def test_plugged_battery_hides_the_runtime_estimate(self):
        status = system_tools.BatteryStatus(percent=100, plugged=True, seconds_left=None)
        self.assertIn("charging", status.describe())
        self.assertEqual(system_tools.format_seconds_left(None, True), "")

    def test_open_media_rejects_a_missing_path(self):
        ok, message = system_tools.open_media("/definitely/not/here.mp3")
        self.assertFalse(ok)
        self.assertIn("could not find", message.lower())

    def test_power_argv_is_defined_per_platform(self):
        self.assertEqual(system_tools.power_argv("restart", "Windows"),
                         ["shutdown", "/r", "/t", "5"])
        self.assertEqual(system_tools.power_argv("nonsense", "Windows"), [])


class PowerSafetyTests(unittest.TestCase):
    """Power controls must never fire without opt-in *and* confirmation."""

    def test_power_is_refused_while_disabled(self):
        calls: list[list[str]] = []
        config = AssistantConfig(allow_power_commands=False)
        ok, message = system_tools.run_power_command(
            "shutdown", config, confirm=lambda action: True, runner=calls.append
        )
        self.assertFalse(ok)
        self.assertEqual(calls, [])
        self.assertIn("disabled", message)

    def test_power_is_refused_when_confirmation_is_declined(self):
        calls: list[list[str]] = []
        config = AssistantConfig(allow_power_commands=True)
        ok, message = system_tools.run_power_command(
            "restart", config, confirm=lambda action: False, runner=calls.append
        )
        self.assertFalse(ok)
        self.assertEqual(calls, [])
        self.assertIn("Cancelled", message)

    def test_power_runs_only_after_opt_in_and_confirmation(self):
        calls: list[list[str]] = []
        config = AssistantConfig(allow_power_commands=True)
        ok, message = system_tools.run_power_command(
            "logout", config, confirm=lambda action: True, runner=calls.append
        )
        self.assertTrue(ok)
        self.assertEqual(len(calls), 1)
        self.assertIn("issued", message)

    def test_unknown_power_action_is_rejected(self):
        ok, message = system_tools.run_power_command("explode", AssistantConfig())
        self.assertFalse(ok)
        self.assertIn("not a supported", message)

    def test_shutdown_intent_is_blocked_by_default(self):
        assistant, _, _ = build_assistant()
        self.assertIn("disabled", assistant.handle("shutdown").text)


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self._saved = dict(os.environ)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._saved)

    def test_defaults_target_jamshedpur(self):
        for key in ("ASSISTANT_CITY", "ASSISTANT_ALLOW_POWER", "ASSISTANT_HEADLINES"):
            os.environ.pop(key, None)
        config = load_config()
        self.assertEqual(config.city, "Jamshedpur")
        self.assertFalse(config.allow_power_commands)

    def test_environment_overrides_are_applied(self):
        os.environ["ASSISTANT_CITY"] = "Bengaluru"
        os.environ["ASSISTANT_HEADLINES"] = "3"
        os.environ["ASSISTANT_ALLOW_POWER"] = "true"
        config = load_config()
        self.assertEqual(config.city, "Bengaluru")
        self.assertEqual(config.max_headlines, 3)
        self.assertTrue(config.allow_power_commands)

    def test_malformed_numeric_values_fall_back_to_defaults(self):
        os.environ["ASSISTANT_HEADLINES"] = "many"
        self.assertEqual(load_config().max_headlines, 5)

    def test_screenshot_target_joins_the_configured_folder(self):
        config = AssistantConfig(screenshot_dir=Path("/tmp/shots"))
        self.assertEqual(config.screenshot_target("a.png"), Path("/tmp/shots/a.png"))


class CliTests(unittest.TestCase):
    def test_parser_reads_every_flag(self):
        from assistant.cli import build_parser

        args = build_parser().parse_args(
            ["--voice", "--no-tts", "--allow-power", "--city", "Pune", "--say", "battery"]
        )
        self.assertTrue(args.voice and args.no_tts and args.allow_power)
        self.assertEqual(args.city, "Pune")
        self.assertEqual(args.say, "battery")

    def test_defaults_are_conservative(self):
        from assistant.cli import build_parser

        args = build_parser().parse_args([])
        self.assertFalse(args.voice or args.no_tts or args.allow_power)


if __name__ == "__main__":
    unittest.main(verbosity=2)
