import webbrowser


websites = {

    "youtube": "https://www.youtube.com",
    
    "google": "https://www.google.com",
    "github": "https://github.com",
    "amazon": "https://www.amazon.in",
    "gmail": "https://mail.google.com",
    "facebook": "https://www.facebook.com",
    "wikipedia": "https://www.wikipedia.org",
    
    "twitter": "https://twitter.com",
}


def open_website(name):

    name = name.lower()

    if name in websites:

        webbrowser.open(websites[name])
        return True

    return False