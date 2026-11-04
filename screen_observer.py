import pyautogui
import time

from observation_settings import is_observation_enabled


def capture_screen():

    if not is_observation_enabled():
        print("Screen observation is OFF.")
        return None

    try:
        screenshot = pyautogui.screenshot()

        print("Screen captured successfully.")

        return screenshot

    except Exception as error:
        print("Screen Capture Error:", error)
        return None


def observe_screen():

    if not is_observation_enabled():
        print("Enable observation first.")
        return None

    screenshot = capture_screen()

    if screenshot is None:
        return None

    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "screenshot": screenshot
    }