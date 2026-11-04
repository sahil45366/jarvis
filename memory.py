import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, dict) else {}

    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as error:
        print("Memory Load Error:", error)
        return {}


def save_memory(data):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True

    except (TypeError, OSError) as error:
        print("Memory Save Error:", error)
        return False


def remember(key, value):
    data = load_memory()
    data[key] = value
    return save_memory(data)


def recall(key):
    data = load_memory()
    return data.get(key)