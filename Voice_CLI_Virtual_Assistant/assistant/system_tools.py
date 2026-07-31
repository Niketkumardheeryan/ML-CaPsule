"""System automation: clipboard, screenshots, battery telemetry, power control.

Every helper degrades gracefully. Optional third-party packages (``pyautogui``,
``psutil``, ``pyperclip``) are imported inside the functions that need them, so
importing this module never fails on a head-less machine.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

POWER_ACTIONS = ("shutdown", "restart", "logout")

# Per-platform argv for each power action. Nothing here runs unless the user
# both enables power commands and confirms the prompt.
_POWER_COMMANDS: dict[str, dict[str, list[str]]] = {
    "Windows": {
        "shutdown": ["shutdown", "/s", "/t", "5"],
        "restart": ["shutdown", "/r", "/t", "5"],
        "logout": ["shutdown", "/l"],
    },
    "Darwin": {
        "shutdown": ["osascript", "-e", 'tell app "System Events" to shut down'],
        "restart": ["osascript", "-e", 'tell app "System Events" to restart'],
        "logout": ["osascript", "-e", 'tell app "System Events" to log out'],
    },
    "Linux": {
        "shutdown": ["systemctl", "poweroff"],
        "restart": ["systemctl", "reboot"],
        "logout": ["loginctl", "terminate-user", os.environ.get("USER", "")],
    },
}


def _default_runner(argv: list[str]) -> None:
    """Run ``argv`` without raising on a non-zero exit status."""
    subprocess.run(argv, check=False)


def current_platform() -> str:
    """Return the platform key used by the power command table."""
    return platform.system()


def power_argv(action: str, system: str | None = None) -> list[str]:
    """Return the argv for ``action`` on ``system``; empty when unsupported."""
    table = _POWER_COMMANDS.get(system or current_platform(), {})
    return list(table.get(action, []))


# --------------------------------------------------------------- clipboard
def read_clipboard() -> str:
    """Return the current clipboard text, or an explanatory message."""
    try:
        import pyperclip

        text = pyperclip.paste()
        if text:
            return text
    except Exception:
        pass  # fall back to the platform utility below

    system = current_platform()
    commands = {
        "Darwin": ["pbpaste"],
        "Linux": ["xclip", "-selection", "clipboard", "-o"],
        "Windows": ["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
    }
    argv = commands.get(system)
    if argv and (shutil.which(argv[0]) or system == "Windows"):
        try:
            completed = subprocess.run(argv, capture_output=True, text=True, timeout=10)
            if completed.returncode == 0 and completed.stdout.strip():
                return completed.stdout.strip()
        except Exception:
            pass

    return "The clipboard is empty or unreadable on this system."


# -------------------------------------------------------------- screenshot
def screenshot_filename(moment: datetime | None = None) -> str:
    """Return a timestamped screenshot file name."""
    return (moment or datetime.now()).strftime("screenshot_%Y%m%d_%H%M%S.png")


def capture_screenshot(config, moment: datetime | None = None) -> tuple[bool, str]:
    """Capture the desktop and return ``(success, message)``."""
    target = config.screenshot_target(screenshot_filename(moment))
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return False, f"Could not create the screenshot folder: {exc}"

    try:
        import pyautogui

        pyautogui.screenshot().save(target)
        return True, f"Screenshot saved to {target}"
    except Exception:
        pass  # try a native utility before giving up

    natives = {
        "Darwin": ["screencapture", "-x", str(target)],
        "Linux": ["gnome-screenshot", "-f", str(target)],
    }
    argv = natives.get(current_platform())
    if argv and shutil.which(argv[0]):
        try:
            completed = subprocess.run(argv, capture_output=True, timeout=20)
            if completed.returncode == 0 and target.exists():
                return True, f"Screenshot saved to {target}"
        except Exception:
            pass

    return False, (
        "Screen capture is unavailable. Install pyautogui, and on macOS grant your "
        "terminal Screen Recording permission in System Settings > Privacy & Security."
    )


# ----------------------------------------------------------------- battery
@dataclass
class BatteryStatus:
    """Battery telemetry snapshot."""

    percent: float
    plugged: bool
    seconds_left: int | None = None

    def describe(self) -> str:
        """Render the snapshot as a single spoken sentence."""
        state = "charging" if self.plugged else "on battery"
        sentence = f"The battery is at {self.percent:.0f} percent and {state}."
        remaining = format_seconds_left(self.seconds_left, self.plugged)
        return f"{sentence} {remaining}".strip()


def format_seconds_left(seconds: int | None, plugged: bool) -> str:
    """Describe the remaining battery runtime in hours and minutes."""
    if plugged or seconds is None or seconds < 0:
        return ""
    hours, minutes = divmod(seconds // 60, 60)
    if hours and minutes:
        return f"About {hours} hours and {minutes} minutes remaining."
    if hours:
        return f"About {hours} hours remaining."
    return f"About {minutes} minutes remaining."


def battery_status() -> BatteryStatus | None:
    """Return the current battery status, or ``None`` when unavailable."""
    try:
        import psutil

        battery = psutil.sensors_battery()
    except Exception:
        return None
    if battery is None:
        return None

    seconds = battery.secsleft
    unlimited = getattr(psutil, "POWER_TIME_UNLIMITED", -2)
    unknown = getattr(psutil, "POWER_TIME_UNKNOWN", -1)
    if seconds in (unlimited, unknown):
        seconds = None
    return BatteryStatus(
        percent=float(battery.percent),
        plugged=bool(battery.power_plugged),
        seconds_left=seconds,
    )


# ------------------------------------------------------------------- media
def open_media(path: str, runner=None) -> tuple[bool, str]:
    """Play ``path`` with the operating system's default media player."""
    media = Path(path).expanduser()
    if not media.exists():
        return False, f"I could not find any file at {media}."

    system = current_platform()
    if system == "Windows":
        try:
            os.startfile(str(media))  # type: ignore[attr-defined]  # Windows only
            return True, f"Playing {media.name}."
        except Exception as exc:
            return False, f"Could not play {media.name}: {exc}"

    argv = ["open", str(media)] if system == "Darwin" else ["xdg-open", str(media)]
    try:
        (runner or subprocess.Popen)(argv)
        return True, f"Playing {media.name}."
    except Exception as exc:
        return False, f"Could not play {media.name}: {exc}"


# ------------------------------------------------------------------- power
def run_power_command(action: str, config, confirm=None, runner=None) -> tuple[bool, str]:
    """Run a shutdown / restart / logout command behind two safety gates.

    The command only runs when power controls are enabled (``ASSISTANT_ALLOW_POWER``
    or ``--allow-power``) *and* ``confirm`` returns ``True``. Otherwise the exact
    command that would have run is reported instead.
    """
    action = action.lower().strip()
    if action not in POWER_ACTIONS:
        return False, f"'{action}' is not a supported power command."

    argv = power_argv(action)
    if not argv:
        return False, f"{action.capitalize()} is not supported on {current_platform()}."

    if not config.allow_power_commands:
        return False, (
            f"Power commands are disabled. Restart me with --allow-power to enable "
            f"'{action}' (it would run: {' '.join(argv)})."
        )

    if confirm is not None and not confirm(action):
        return False, f"Cancelled the {action} request."

    try:
        (runner or _default_runner)(argv)
        return True, f"{action.capitalize()} command issued."
    except Exception as exc:
        return False, f"Could not issue the {action} command: {exc}"


def system_summary() -> str:
    """Return a short description of the host machine."""
    return (
        f"{platform.system()} {platform.release()} on {platform.machine()}, "
        f"running Python {sys.version_info.major}.{sys.version_info.minor}."
    )
