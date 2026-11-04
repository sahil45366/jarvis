import os
import datetime
import socket
import psutil
import webbrowser


# ---------------- TIME & DATE ---------------- #

def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")


def get_date():
    return datetime.datetime.now().strftime("%d %B %Y")


def get_day():
    return datetime.datetime.now().strftime("%A")


# ---------------- BATTERY ---------------- #

def battery_percentage():
    battery = psutil.sensors_battery()

    if battery:
        return battery.percent

    return None


def battery_charging():
    battery = psutil.sensors_battery()

    if battery:
        return battery.power_plugged

    return False


# ---------------- SYSTEM ---------------- #

def ram_usage():
    return psutil.virtual_memory().percent


def cpu_usage():
    return psutil.cpu_percent(interval=1)


def disk_usage():
    return psutil.disk_usage("/").percent


# ---------------- NETWORK ---------------- #

def ip_address():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Unknown"


# ---------------- WINDOWS ---------------- #

def open_calculator():
    os.system("calc")


def open_notepad():

    import subprocess

    subprocess.Popen(
        ["notepad.exe"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def open_cmd():
    os.system("start cmd")


def open_powershell():
    os.system("start powershell")


# ---------------- WEATHER ---------------- #

def open_weather():
    webbrowser.open("https://www.google.com/search?q=weather")


# ---------------- SHUTDOWN ---------------- #

def shutdown():
    os.system("shutdown /s /t 1")


def restart():
    os.system("shutdown /r /t 1")


def lock_pc():
    os.system("rundll32.exe user32.dll,LockWorkStation")