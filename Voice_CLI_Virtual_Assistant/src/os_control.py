"""
OS-Level Control Hooks for Voice & CLI Virtual Assistant.
Provides media/file execution via subprocess and administrative power control protocols (logout, restart, shutdown).
"""

import os
import platform
import subprocess
import sys


def open_media(target_path: str) -> str:
    """
    Triggers execution or launch of a media file, document, or application.

    Args:
        target_path (str): File path, document, or app name to launch.

    Returns:
        str: Result status message.
    """
    if not target_path or not target_path.strip():
        return "Please specify a valid file path or application name to open."

    clean_target = target_path.strip()
    system_os = platform.system().lower()

    try:
        if system_os == "windows":
            os.startfile(clean_target)
        elif system_os == "darwin":  # macOS
            subprocess.Popen(["open", clean_target])
        else:  # Linux/Unix
            subprocess.Popen(["xdg-open", clean_target])
        return f"🚀 Successfully launched target: '{clean_target}'"
    except Exception as e:
        return f"⚠️ Failed to launch target '{clean_target}': {e}"


def power_command(action: str, confirm: bool = False) -> str:
    """
    Executes administrative power commands (logout, restart, shutdown).
    Requires explicit confirm=True parameter to prevent unintended execution during tests.

    Args:
        action (str): Power action ('logout', 'restart', 'shutdown').
        confirm (bool): Safety confirmation flag. Must be True to trigger power action.

    Returns:
        str: Execution status or safety warning.
    """
    act = action.strip().lower()
    valid_actions = ["logout", "restart", "shutdown"]

    if act not in valid_actions:
        return f"⚠️ Invalid power command '{action}'. Supported actions: {', '.join(valid_actions)}"

    if not confirm:
        return (
            f"🔒 [Power Command Guard] Requested action: '{act.upper()}'.\n"
            f"Execution halted for safety. To proceed with system {act}, re-run with confirmation flag '--confirm'."
        )

    system_os = platform.system().lower()

    try:
        if act == "shutdown":
            if system_os == "windows":
                cmd = ["shutdown", "/s", "/t", "10"]
            else:
                cmd = ["shutdown", "-h", "now"]
            subprocess.run(cmd, check=True)
            return f"⚡ System shutdown initiated..."

        elif act == "restart":
            if system_os == "windows":
                cmd = ["shutdown", "/r", "/t", "10"]
            else:
                cmd = ["shutdown", "-r", "now"]
            subprocess.run(cmd, check=True)
            return f"🔄 System restart initiated..."

        elif act == "logout":
            if system_os == "windows":
                cmd = ["shutdown", "/l"]
            else:
                cmd = ["pkill", "-u", os.getlogin()]
            subprocess.run(cmd, check=True)
            return f"🔒 Logging out user..."

    except Exception as e:
        return f"⚠️ Administrative power command '{act}' failed: {e}"
