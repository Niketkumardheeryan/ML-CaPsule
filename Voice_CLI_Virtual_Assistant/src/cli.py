"""
Command-Line Interface Handler for Voice & CLI Virtual Assistant.
"""

import argparse
import sys
from .assistant import VirtualAssistant
from .speech_engine import safe_print


def run_cli():
    """CLI entry point handling options and execution loop."""
    parser = argparse.ArgumentParser(
        description="Voice & CLI-Driven System Virtual Assistant",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["cli", "voice", "interactive"],
        default="cli",
        help="Input mode: CLI text commands, Voice microphone listening, or interactive selector.",
    )
    parser.add_argument(
        "--cmd",
        type=str,
        default=None,
        help="Execute a single command directly and exit.",
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Mute Text-to-Speech audio output.",
    )
    parser.add_argument(
        "--city",
        type=str,
        default="Jamshedpur",
        help="Default city for weather indexing.",
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Confirm permission to execute OS power commands (shutdown/restart/logout).",
    )

    args = parser.parse_args()

    assistant = VirtualAssistant(silent=args.silent, default_city=args.city)

    # Handle single shot command execution
    if args.cmd:
        assistant.greet_user()
        response, _ = assistant.process_command(args.cmd, confirm_power=args.confirm)
        return

    # Interactive Loop
    assistant.greet_user()
    safe_print(assistant.get_help_menu())

    mode = args.mode

    try:
        while assistant.running:
            if mode == "voice":
                command = assistant.speech_rec.listen()
            else:
                try:
                    safe_print("\n👤 You (CLI Input): ", end="")
                    command = input().strip()
                except (EOFError, KeyboardInterrupt):
                    safe_print("\nExiting Assistant...")
                    break

            if not command:
                continue

            response, keep_running = assistant.process_command(command, confirm_power=args.confirm)
            if not keep_running:
                break
    except KeyboardInterrupt:
        safe_print("\nSession ended by user.")


if __name__ == "__main__":
    run_cli()
