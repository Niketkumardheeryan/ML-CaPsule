"""Command line entry point.

Examples
--------
    python main.py                      # interactive text session
    python main.py --voice              # interactive voice session
    python main.py --say "weather"      # one-shot command, useful in scripts
    python main.py --list-commands      # print the supported command surface
"""

from __future__ import annotations

import argparse
import sys

from .config import load_config
from .core import VirtualAssistant
from .speech import SpeechEngine


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the assistant."""
    parser = argparse.ArgumentParser(
        prog="virtual-assistant",
        description="Voice and CLI driven system virtual assistant.",
    )
    parser.add_argument("--voice", action="store_true",
                        help="listen on the microphone instead of the keyboard")
    parser.add_argument("--say", metavar="COMMAND",
                        help="run a single command and exit")
    parser.add_argument("--city", metavar="CITY",
                        help="override the default city used for weather")
    parser.add_argument("--no-tts", action="store_true",
                        help="disable spoken output and print responses only")
    parser.add_argument("--allow-power", action="store_true",
                        help="enable shutdown/restart/logout (still asks for confirmation)")
    parser.add_argument("--list-commands", action="store_true",
                        help="print every supported command and exit")
    return parser


def build_assistant(args) -> VirtualAssistant:
    """Create a :class:`VirtualAssistant` configured from parsed ``args``."""
    config = load_config()
    if args.city:
        config.city = args.city
    if args.allow_power:
        config.allow_power_commands = True

    speech = SpeechEngine(
        config,
        enable_tts=not args.no_tts,
        enable_stt=bool(args.voice),
    )
    return VirtualAssistant(config=config, speech=speech)


def main(argv: list[str] | None = None) -> int:
    """Run the assistant and return a process exit code."""
    args = build_parser().parse_args(argv)
    assistant = build_assistant(args)

    if args.list_commands:
        print(assistant.router.help_text())
        return 0

    if args.say:
        response = assistant.respond(args.say)
        return 0 if response.handled else 1

    return assistant.run(voice=bool(args.voice))


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
