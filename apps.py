
import subprocess
import ctypes
import time
import psutil
from ctypes import wintypes

from app_finder import find_app, find_process


# ---------------- OPEN APP ----------------

def open_app(app):

    app = app.lower().strip()

    app_id = find_app(app)

    if not app_id:
        print("App not found:", app)
        return False

    print("FOUND APP:", app_id)

    try:

        powershell_command = (
            f'Start-Process "shell:AppsFolder\\{app_id}"'
        )

        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                powershell_command
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("Launching:", app)
            return True

        print("Launch failed!")
        print("PowerShell Error:", result.stderr)
        return False

    except Exception as e:

        print("Launch Error:", e)
        return False
    # ---------------- FIND APP WINDOW ----------------

def find_app_window(process_name):

    user32 = ctypes.WinDLL("user32", use_last_error=True)

    EnumWindows = user32.EnumWindows
    GetWindowThreadProcessId = user32.GetWindowThreadProcessId
    IsWindowVisible = user32.IsWindowVisible
    GetWindowTextW = user32.GetWindowTextW

    WNDENUMPROC = ctypes.WINFUNCTYPE(
        wintypes.BOOL,
        wintypes.HWND,
        wintypes.LPARAM
    )

    found_windows = []

    def callback(hwnd, lparam):

        if not IsWindowVisible(hwnd):
            return True

        pid = wintypes.DWORD()

        GetWindowThreadProcessId(
            hwnd,
            ctypes.byref(pid)
        )

        try:
            current_process = psutil.Process(pid.value)
            current_name = current_process.name().lower().removesuffix(".exe")
            expected_name = process_name.lower().removesuffix(".exe")

            if current_name != expected_name:
                return True

            buffer = ctypes.create_unicode_buffer(512)

            GetWindowTextW(hwnd, buffer, 512)

            title = buffer.value.strip()

            if title:
                found_windows.append({
                    "hwnd": hwnd,
                    "pid": pid.value,
                    "process_name": current_name,
                    "window_title": title
                })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

        return True

    enum_callback = WNDENUMPROC(callback)
    EnumWindows(enum_callback, 0)

    return found_windows[0] if found_windows else None


# ---------------- FOCUS APP WINDOW ----------------

def focus_app_window(hwnd):

    user32 = ctypes.WinDLL("user32", use_last_error=True)

    ShowWindow = user32.ShowWindow
    SetForegroundWindow = user32.SetForegroundWindow
    GetForegroundWindow = user32.GetForegroundWindow

    SW_RESTORE = 9

    ShowWindow(hwnd, SW_RESTORE)

    time.sleep(0.3)

    SetForegroundWindow(hwnd)

    time.sleep(0.5)

    return GetForegroundWindow() == hwnd


# ---------------- OPEN + FOCUS + VERIFY ----------------

def open_app_and_focus(app, timeout=20):

    app = app.lower().strip()

    print("Opening app:", app)

    if not open_app(app):
        return {
            "success": False,
            "message": "App launch failed."
        }

    process_name = find_process(app)

    if not process_name:
        return {
            "success": False,
            "message": "App process not detected."
        }

    start_time = time.time()

    while time.time() - start_time < timeout:

        window = find_app_window(process_name)

        if window:

            focused = focus_app_window(window["hwnd"])

            if focused:

                print("APP FOCUSED:", window["process_name"])
                print("ACTIVE WINDOW:", window["window_title"])

                return {
                    "success": True,
                    "process_name": window["process_name"],
                    "process_id": window["pid"],
                    "window_title": window["window_title"]
                }

        time.sleep(0.5)

    return {
        "success": False,
        "message": "App window was not detected or focused."
    }


# ---------------- CLOSE WINDOWS STORE APPS ----------------

def close_store_app(app):

    app = app.lower().strip()

    # Window titles for Store applications
    window_titles = {
        "calculator": ["Calculator"],
        "instagram": ["Instagram"],
        "store": ["Microsoft Store"]
    }

    target_titles = None

    for key, titles in window_titles.items():

        if key in app:
            target_titles = titles
            break

    if not target_titles:
        return False

    try:

        user32 = ctypes.WinDLL("user32", use_last_error=True)

        EnumWindows = user32.EnumWindows
        EnumWindows.argtypes = [
            ctypes.WINFUNCTYPE(
                wintypes.BOOL,
                wintypes.HWND,
                wintypes.LPARAM
            ),
            wintypes.LPARAM
        ]

        EnumWindows.restype = wintypes.BOOL

        GetWindowTextW = user32.GetWindowTextW
        GetWindowTextW.argtypes = [
            wintypes.HWND,
            wintypes.LPWSTR,
            ctypes.c_int
        ]

        GetWindowTextLengthW = user32.GetWindowTextLengthW
        GetWindowTextLengthW.argtypes = [wintypes.HWND]
        GetWindowTextLengthW.restype = ctypes.c_int

        IsWindowVisible = user32.IsWindowVisible
        IsWindowVisible.argtypes = [wintypes.HWND]
        IsWindowVisible.restype = wintypes.BOOL

        PostMessageW = user32.PostMessageW
        PostMessageW.argtypes = [
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            wintypes.LPARAM
        ]
        PostMessageW.restype = wintypes.BOOL

        WM_CLOSE = 0x0010

        closed = []

        WNDENUMPROC = ctypes.WINFUNCTYPE(
            wintypes.BOOL,
            wintypes.HWND,
            wintypes.LPARAM
        )

        def callback(hwnd, lparam):

            if not IsWindowVisible(hwnd):
                return True

            length = GetWindowTextLengthW(hwnd)

            if length == 0:
                return True

            buffer = ctypes.create_unicode_buffer(length + 1)

            GetWindowTextW(
                hwnd,
                buffer,
                length + 1
            )

            title = buffer.value.strip()

            for target in target_titles:

                if title.lower() == target.lower():

                    if PostMessageW(
                        hwnd,
                        WM_CLOSE,
                        0,
                        0
                    ):
                        closed.append(title)
                        print("Close message sent:", title)

                    return True

            return True

        enum_callback = WNDENUMPROC(callback)

        EnumWindows(enum_callback, 0)

        if closed:
            print(app, "close request successful")
            return True

        print("Window not found:", app)
        return False

    except Exception as e:

        print("Close Store Error:", e)
        return False


# ---------------- CLOSE NORMAL APPS ----------------

def close_app(app):

    app = app.lower().strip()

    print("Close request:", app)

    # Microsoft Store applications
    if (
        "instagram" in app
        or "calculator" in app
        or "store" in app
    ):

        return close_store_app(app)

    # Normal desktop applications
    process = find_process(app)

    if process:

        result = subprocess.run(
            [
                "taskkill",
                "/F",
                "/IM",
                process + ".exe"
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            print("Closed:", process)
            return True

        print("Close failed:", result.stderr)
        return False

    print("Process not found:", app)
    return False
