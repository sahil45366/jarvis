current_context = {
    "website": None
}


def set_context(key, value):
    current_context[key] = value


def get_context(key):
    return current_context.get(key)


def clear_context():

    global current_context

    current_context = {
        "website": None
    }
    