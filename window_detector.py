import ctypes
import psutil
from ctypes import wintypes


user32 = ctypes.WinDLL("user32", use_last_error=True)

user32.GetForegroundWindow.argtypes = []
user32.GetForegroundWindow.restype = wintypes.HWND

user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
user32.GetWindowTextLengthW.restype = ctypes.c_int

user32.GetWindowTextW.argtypes = [
    wintypes.HWND,
    wintypes.LPWSTR,
    ctypes.c_int
]
user32.GetWindowTextW.restype = ctypes.c_int

user32.GetWindowThreadProcessId.argtypes = [
    wintypes.HWND,
    ctypes.POINTER(wintypes.DWORD)
]
user32.GetWindowThreadProcessId.restype = wintypes.DWORD


def get_active_window():
    """Detect foreground window metadata without capturing its screen."""

    try:
        hwnd = user32.GetForegroundWindow()

        if not hwnd:
            return None

        length = user32.GetWindowTextLengthW(hwnd)
        buffer = ctypes.create_unicode_buffer(length + 1)

        user32.GetWindowTextW(
            hwnd,
            buffer,
            length + 1
        )

        window_title = buffer.value.strip()

        process_id = wintypes.DWORD()

        user32.GetWindowThreadProcessId(
            hwnd,
            ctypes.byref(process_id)
        )

        try:
            process = psutil.Process(process_id.value)
            process_name = process.name()

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            process_name = "Unknown"

        return {
            "window_title": window_title,
            "process_name": process_name,
            "process_id": process_id.value
        }

    except Exception as error:
        print("Window Detection Error:", error)
        return None


if __name__ == "__main__":
    print(get_active_window())