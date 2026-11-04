import pyautogui
import datetime
import os


# ---------------- SCREENSHOT ---------------- #

def take_screenshot():
    try:
        folder = "Screenshots"

        if not os.path.exists(folder):
            os.makedirs(folder)

        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
        path = os.path.join(folder, filename)

        image = pyautogui.screenshot()
        image.save(path)

        print(f"Screenshot saved: {path}")

    except Exception as e:
        print("Screenshot Error:", e)


# ---------------- CLIPBOARD ---------------- #

def copy():
    pyautogui.hotkey("ctrl", "c")


def paste():
    pyautogui.hotkey("ctrl", "v")


def cut():
    pyautogui.hotkey("ctrl", "x")


def undo():
    pyautogui.hotkey("ctrl", "z")


def redo():
    pyautogui.hotkey("ctrl", "y")


def select_all():
    pyautogui.hotkey("ctrl", "a")


# ---------------- WINDOWS SHORTCUTS ---------------- #

def save():
    pyautogui.hotkey("ctrl", "s")


def find():
    pyautogui.hotkey("ctrl", "f")


def print_file():
    pyautogui.hotkey("ctrl", "p")