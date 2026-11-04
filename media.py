import pyautogui
import time


# ---------------- VOLUME CONTROL ---------------- #

def volume_up():

    for i in range(5):   # 5 times = approx +10%
        pyautogui.press("volumeup")
        time.sleep(0.1)


def volume_down():

    for i in range(5):   # 5 times = approx -10%
        pyautogui.press("volumedown")
        time.sleep(0.1)


def mute():

    pyautogui.press("volumemute")



# ---------------- MEDIA CONTROL ---------------- #

def play_pause():
    pyautogui.press("playpause")


def next_song():
    pyautogui.press("nexttrack")


def previous_song():
    pyautogui.press("prevtrack")