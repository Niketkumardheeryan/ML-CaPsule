"""
System Automation Engine for Voice & CLI Virtual Assistant.
Provides clipboard text reading, timestamped desktop screen capturing, and live battery telemetry monitoring.
"""

from datetime import datetime
import os
import sys


def read_clipboard() -> str:
    """
    Reads text content from the system clipboard.

    Returns:
        str: Text content or status message.
    """
    try:
        import pyperclip
        text = pyperclip.paste()
        if text and text.strip():
            return f"📋 Clipboard Content:\n\"{text.strip()}\""
        return "📋 Clipboard is currently empty or contains non-text data."
    except Exception as e:
        # Tkinter fallback
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            text = root.clipboard_get()
            root.destroy()
            if text and text.strip():
                return f"📋 Clipboard Content:\n\"{text.strip()}\""
            return "📋 Clipboard is currently empty."
        except Exception:
            return f"⚠️ Could not read clipboard content: {e}"


def take_screenshot(output_dir: str = "screenshots") -> str:
    """
    Captures a timestamped desktop screenshot and saves it to output_dir.

    Args:
        output_dir (str): Directory where screenshot images are stored.

    Returns:
        str: Status message with absolute filepath.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.abspath(os.path.join(output_dir, filename))

        # Try pyautogui first, fallback to PIL.ImageGrab
        captured = False
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            captured = True
        except Exception:
            try:
                from PIL import ImageGrab
                screenshot = ImageGrab.grab()
                screenshot.save(filepath)
                captured = True
            except Exception as e:
                return f"⚠️ Screenshot capture failed: {e}"

        if captured:
            return f"📸 Desktop screenshot saved successfully:\nPath: {filepath}"
        return "⚠️ Screenshot capture could not be saved."
    except Exception as e:
        return f"⚠️ Error taking screenshot: {e}"


def get_battery_telemetry() -> str:
    """
    Retrieves live battery telemetry including percentage, plug status, and time remaining.

    Returns:
        str: Battery telemetry status report.
    """
    try:
        import psutil
        battery = psutil.sensors_battery()

        if battery is None:
            return "🔋 Battery Telemetry: No battery detected (Desktop system or battery status unavailable)."

        percent = round(battery.percent, 1)
        power_plugged = battery.power_plugged
        plug_status = "Plugged In (AC Power)" if power_plugged else "Discharging (On Battery)"

        if battery.secsleft == psutil.POWER_TIME_UNLIMITED:
            time_left_str = "Fully Charged / Continuous Power"
        elif battery.secsleft == psutil.POWER_TIME_UNKNOWN or battery.secsleft < 0:
            time_left_str = "Calculating time remaining..."
        else:
            hours = battery.secsleft // 3600
            minutes = (battery.secsleft % 3600) // 60
            time_left_str = f"{hours}h {minutes}m remaining"

        return (
            f"🔋 Battery Telemetry Status:\n"
            f"• Level: {percent}%\n"
            f"• Power State: {plug_status}\n"
            f"• Time Remaining: {time_left_str}"
        )
    except Exception as e:
        return f"⚠️ Could not retrieve battery telemetry: {e}"
