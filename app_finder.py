
import json
import subprocess


# -------- APP ALIASES -------- #

APP_ALIASES = {
    "whatsapp": "whatsapp",
    "spotify": "spotify",
    "instagram": "instagram",
    "capcut": "capcut",
    "edge": "microsoft edge",
    "chrome": "google chrome",
    "powerpoint": "powerpoint",
    "word": "word",
    "excel": "excel",
    "microsoft store": "microsoft store"
}


PROCESS_ALIASES = {
    "chrome": "chrome",
    "google chrome": "chrome",
    "edge": "msedge",
    "microsoft edge": "msedge",
    "powerpoint": "powerpnt",
    "word": "winword",
    "excel": "excel",
    "spotify": "spotify",
    "whatsapp": "whatsapp",
    "instagram": "instagram",
    "capcut": "capcut",
    "microsoft store": "WinStore.App"
}


# -------- FIND WINDOWS APP -------- #

def find_app(app_name):

    app_name = app_name.lower().strip()
    search = APP_ALIASES.get(app_name, app_name)

    try:
        result = subprocess.check_output(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-StartApps | Select-Object Name, AppID | ConvertTo-Json -Compress"
            ],
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        apps = json.loads(result)

        if isinstance(apps, dict):
            apps = [apps]

        # Exact match first
        for item in apps:
            name = item.get("Name", "").strip()

            if name.lower() == search:
                print("FOUND APP:", name)
                print("APP ID:", item.get("AppID"))
                return item.get("AppID")

        # Partial match only as fallback
        matches = [
            item for item in apps
            if search in item.get("Name", "").lower()
        ]

        if len(matches) == 1:
            print("FOUND APP:", matches[0]["Name"])
            return matches[0].get("AppID")

        if len(matches) > 1:
            print("Multiple matching apps found:")
            for item in matches:
                print("-", item.get("Name"))

    except Exception as e:
        print("Find App Error:", e)

    return None


# -------- FIND RUNNING PROCESS -------- #

def find_process(app):

    app = app.lower().strip()
    search = PROCESS_ALIASES.get(app, app).lower()

    try:
        result = subprocess.check_output(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-Process | Select-Object -ExpandProperty ProcessName"
            ],
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        for line in result.splitlines():

            process = line.strip()

            if process.lower() == search:
                print("FOUND PROCESS:", process)
                return process

    except Exception as e:
        print("Process Error:", e)

    return None
