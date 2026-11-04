import tkinter as tk
import pyautogui

from window_detector import get_active_window

from apps import open_app_and_focus
from browser import (
    get_active_browser,
    google_search,
    youtube_search
)
from observation_settings import is_observation_enabled
from screen_observer import capture_screen


ALLOWED_ACTIONS = {
    "open_app",
    "google_search",
    "youtube_search",
    "capture_screen",
    "type_text"
}

# Tracks the browser opened by JARVIS during this task.
active_task_browser = None
active_task_app = None 


def execute_step(step):

    global active_task_browser,active_task_app

    if not isinstance(step, dict):
        return {
            "success": False,
            "message": "Invalid step format."
        }

    action = step.get("action")
    target = step.get("target", "")

    if action not in ALLOWED_ACTIONS:
        return {
            "success": False,
            "message": "Action not allowed."
        }

    if not isinstance(target, str):
        return {
            "success": False,
            "message": "Invalid target."
        }

    target = target.strip()

    # OPEN APP + FOCUS + VERIFY
    if action == "open_app":
        
        if not target:
            return {
                "success": False,
                "message": "App name missing."
            }

        try:
            result = open_app_and_focus(target)

            if not isinstance(result, dict) or not result.get("success"):
                active_task_browser = None

                return {
                    "success": False,
                    "message": "App launch or focus verification failed.",
                    "details": result
                }

            process = result.get("process_name", "").lower()
            process = process.removesuffix(".exe")
            active_task_app = process

            if process == "chrome":
                active_task_browser = "chrome"
            elif process == "msedge":
                active_task_browser = "edge"
            else:
                active_task_browser = None

            return {
                "success": True,
                "message": "App launched and focused successfully.",
                "details": result
            }

        except Exception as error:
            active_task_browser = None

            return {
                "success": False,
                "message": f"App launch failed: {error}"
            }

    # VERIFY BROWSER BEFORE SEARCH
    elif action in {"google_search", "youtube_search"}:

        if not target:
            return {
                "success": False,
                "message": "Search query missing."
            }

        if active_task_browser not in {"chrome", "edge"}:
            return {
                "success": False,
                "message": "JARVIS has not opened a supported browser in this task."
            }

        try:
            current_browser = get_active_browser()

            if current_browser != active_task_browser:
                return {
                    "success": False,
                    "message": "Browser focus changed. Search cancelled for safety."
                }

            if action == "google_search":
              result = google_search(target)
              message = "Google search page load verified."

            else:
             result = youtube_search(target)
             message = "YouTube search page load verified."

            return {
        "success": bool(result),
         "message": message if result else "Browser search failed."
                 }
        except Exception as error:
            return {
                "success": False,
                "message": f"Browser search failed: {error}"
            }

        # TYPE TEXT 
    elif action == "type_text":

     if not target:
        return {
            "success": False,
            "message": "No text provided. Typing cancelled."
        }

    if active_task_app != "notepad":
        return {
            "success": False,
            "message": "Text entry blocked. Notepad was not opened in this task."
        }
    elif action == "type_text":

        if active_task_app != "notepad":
            return {
                "success": False,
                "message": "Text entry blocked. Notepad was not opened in this task."
            }

        try:
            window = get_active_window()

            if not window:
                return {
                    "success": False,
                    "message": "Unable to verify active window."
                }

            process = window.get("process_name", "").lower()
            process = process.removesuffix(".exe")

            if process != "notepad":
                return {
                    "success": False,
                    "message": "Typing cancelled. Notepad is not the active window."
                }

            # Copy Unicode text and paste it into Notepad.
            root = tk.Tk()
            root.withdraw()
            root.clipboard_clear()
            root.clipboard_append(target)
            root.update()
            root.destroy()

            pyautogui.hotkey("ctrl", "v")

            return {
                "success": True,
                "message": "Text pasted into verified Notepad.",
                "details": {
                    "app": "notepad",
                    "characters": len(target)
                }
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Text entry failed: {error}"
            }
    # SCREEN CAPTURE
    elif action == "capture_screen":

        if not is_observation_enabled():
            return {
                "success": False,
                "message": "Screen observation is OFF."
            }

        try:
            screenshot = capture_screen()

            return {
                "success": screenshot is not None,
                "message": (
                    "Screen captured."
                    if screenshot is not None
                    else "Capture failed."
                ),
                "screenshot": screenshot
            }

        except Exception as error:
            return {
                "success": False,
                "message": f"Screen capture failed: {error}"
            }

    return {
        "success": False,
        "message": "Unknown action."
    }


def execute_plan(plan):

    global active_task_browser, active_task_app

    active_task_browser = None
    active_task_app = None

    if not isinstance(plan, dict):
        return {
            "success": False,
            "results": []
        }

    steps = plan.get("steps")

    if not isinstance(steps, list) or not steps:
        return {
            "success": False,
            "results": []
        }

    results = []

    for step in steps:

        result = execute_step(step)
        results.append(result)

        if not result["success"]:
            break

    return {
        "success": all(item["success"] for item in results),
        "results": results
    }


if __name__ == "__main__":
    print("JARVIS Task Executor Loaded.")
