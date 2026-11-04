
import os
import subprocess
import urllib.parse
import time
import pyautogui

from window_detector import get_active_window


# ---------------- ACTIVE BROWSER DETECTION ----------------

def get_active_browser():

    window = get_active_window()

    if not window:
        return None

    process = window.get("process_name", "").lower()
    process = process.removesuffix(".exe")

    if process == "chrome":
        return "chrome"

    if process == "msedge":
        return "edge"

    return None


# ---------------- OPEN IN CHROME ----------------

def open_in_chrome(url):

    chrome_path = os.path.expandvars(
        r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"
    )

    if not os.path.isfile(chrome_path):
        print("Google Chrome executable not found.")
        return False

    try:
        subprocess.Popen([chrome_path, url])
        return True

    except Exception as error:
        print("Chrome launch failed:", error)
        return False


# ---------------- NAVIGATE CURRENT BROWSER ----------------

def navigate_current_browser(url, expected_text=None, timeout=20):

    browser = get_active_browser()

    if not browser:
        print("No supported browser is currently active.")
        return False

    try:
        # Capture the current window before navigation
        old_window = get_active_window()
        old_title = old_window.get("window_title", "") if old_window else ""

        pyautogui.hotkey("ctrl", "l")
        time.sleep(0.3)

        pyautogui.write(url, interval=0.005)
        pyautogui.press("enter")

        print("Navigation requested in:", browser)

        # Wait for the expected page title
        start_time = time.time()

        while time.time() - start_time < timeout:
            time.sleep(1)

            window = get_active_window()

            if not window:
                continue

            process = window.get("process_name", "").lower()
            process = process.removesuffix(".exe")
            title = window.get("window_title", "").lower()

            if process != browser:
                continue

            if not title:
                continue

            if expected_text:
                if expected_text.lower() in title:
                    print("PAGE LOAD VERIFIED:", title)
                    return True
            elif title != old_title.lower():
                print("PAGE LOAD VERIFIED:", title)
                return True

        print("Page load could not be verified.")
        return False

    except Exception as error:
        print("Navigation failed:", error)
        return False


# ---------------- OPEN WEBSITES ----------------

def open_google():
    return navigate_current_browser("https://www.google.com")


def open_youtube():
    return navigate_current_browser("https://www.youtube.com")


def open_github():
    return navigate_current_browser("https://github.com")


def open_amazon():
    return navigate_current_browser("https://www.amazon.in")


def open_wikipedia():
    return navigate_current_browser("https://www.wikipedia.org")


# ---------------- SEARCH ----------------

def google_search(query):

    if not isinstance(query, str) or not query.strip():
        return False

    query = query.strip()

    url = (
        "https://www.google.com/search?q="
        + urllib.parse.quote(query)
    )

    return navigate_current_browser(
        url,
        expected_text=query
    )
def youtube_search(query):

    if not isinstance(query, str) or not query.strip():
        return False

    url = (
        "https://www.youtube.com/results?search_query="
        + urllib.parse.quote(query.strip())
    )

    return navigate_current_browser(url)


def github_search(query):

    if not isinstance(query, str) or not query.strip():
        return False

    url = (
        "https://github.com/search?q="
        + urllib.parse.quote(query.strip())
    )

    return navigate_current_browser(url)


def amazon_search(query):

    if not isinstance(query, str) or not query.strip():
        return False

    url = (
        "https://www.amazon.in/s?k="
        + urllib.parse.quote(query.strip())
    )

    return navigate_current_browser(url)


def wikipedia_search(query):

    if not isinstance(query, str) or not query.strip():
        return False

    url = (
        "https://en.wikipedia.org/wiki/Special:Search?search="
        + urllib.parse.quote(query.strip())
    )

    return navigate_current_browser(url)


# ---------------- BROWSER TABS ----------------

def browser_shortcut(keys):

    if not get_active_browser():
        print("No supported browser is active.")
        return False

    try:
        pyautogui.hotkey(*keys)
        return True

    except Exception as error:
        print("Browser shortcut failed:", error)
        return False


def new_tab():
    return browser_shortcut(["ctrl", "t"])


def close_tab():
    return browser_shortcut(["ctrl", "w"])


def reopen_tab():
    return browser_shortcut(["ctrl", "shift", "t"])


def next_tab():
    return browser_shortcut(["ctrl", "tab"])


def previous_tab():
    return browser_shortcut(["ctrl", "shift", "tab"])


# ---------------- NAVIGATION ----------------

def refresh_page():
    return browser_shortcut(["ctrl", "r"])


def go_back():
    return browser_shortcut(["alt", "left"])


def go_forward():
    return browser_shortcut(["alt", "right"])


# ---------------- ZOOM ----------------

def zoom_in():
    return browser_shortcut(["ctrl", "+"])


def zoom_out():
    return browser_shortcut(["ctrl", "-"])


def reset_zoom():
    return browser_shortcut(["ctrl", "0"])
