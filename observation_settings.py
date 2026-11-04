import json
import os

CONFIG_FILE = "observation_config.json"

DEFAULT_SETTINGS = {
    "observation_enabled": False,
    "capture_interval": 3,
    "save_screenshots": False
}


def load_settings():
    if not os.path.exists(CONFIG_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)

        return {**DEFAULT_SETTINGS, **settings}

    except (json.JSONDecodeError, OSError) as error:
        print("Settings Error:", error)
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def enable_observation():
    settings = load_settings()
    settings["observation_enabled"] = True
    save_settings(settings)
    print("Screen Observation Enabled")
    return True


def disable_observation():
    settings = load_settings()
    settings["observation_enabled"] = False
    save_settings(settings)
    print("Screen Observation Disabled")
    return True


def is_observation_enabled():
    return load_settings()["observation_enabled"]