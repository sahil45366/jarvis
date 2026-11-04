import os
import subprocess


# ---------- Helper ---------- #

def open_folder(folder_name):
    paths = [
        os.path.join(os.path.expanduser("~"), folder_name),
        os.path.join(os.path.expanduser("~"), "OneDrive", folder_name),
    ]

    for path in paths:
        if os.path.exists(path):
            os.startfile(path)
            return True

    print(f"{folder_name} folder not found")
    return False


# ---------- USER FOLDERS ---------- #

def open_desktop():
    open_folder("Desktop")


def open_documents():
    open_folder("Documents")


def open_downloads():
    open_folder("Downloads")


def open_pictures():
    open_folder("Pictures")


def open_music():
    open_folder("Music")


def open_videos():
    open_folder("Videos")


# ---------- WINDOWS LOCATIONS ---------- #

def open_this_pc():
    subprocess.Popen("explorer.exe shell:MyComputerFolder")


def open_recycle_bin():
    subprocess.Popen("explorer.exe shell:RecycleBinFolder")


def open_control_panel():
    os.system("control")


def open_task_manager():
    os.system("taskmgr")


def open_settings():
    os.system("start ms-settings:")


# ---------- COMMON FOLDERS ---------- #

def open_temp():
    os.system("start %temp%")


def open_run():
    os.system(
        'explorer.exe shell:::{2559a1f3-21d7-11d4-bdaf-00c04f60b9f0}'
    )