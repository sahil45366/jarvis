import re


# ---------------- SEARCH QUERY ---------------- #

def extract_query(command):

    command = command.lower()

    words = [
        "search",
        "youtube",
        "par",
        "pe",
        "main",
        "karo",
        "karo na"
    ]


    query = command

    for word in words:
        query = query.replace(word, "")

    return query.strip()



# ---------------- VOLUME NUMBER ---------------- #

def extract_volume(command):

    command = command.lower()

    numbers = re.findall(r'\d+', command)

    if numbers:
        return int(numbers[0])

    return None



# ---------------- APP NAME ---------------- #

def extract_app(command):

    apps = [
        "chrome",
        "youtube",
        "google",
        "notepad",
        "calculator",
        "vs code"
        "instagram"
    ]

    for app in apps:

        if app in command:
            return app

    return None



# ---------------- FILE NAME ---------------- #

def extract_folder(command):

    folders = {

        "downloads": [
            "downloads",
            "download"
        ],

        "desktop": [
            "desktop"
        ],

        "documents": [
            "documents",
            "document"
        ],

        "pictures": [
            "pictures",
            "photos"
        ],

        "music": [
            "music",
            "songs"
        ],

        "videos": [
            "videos"
        ]
    }


    for folder, words in folders.items():

        for word in words:

            if word in command:
                return folder


    return None