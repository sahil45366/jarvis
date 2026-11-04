def split_commands(command):

    command = command.strip()

    task_phrases = [
        "perform this task",
        "do this task",
        "complete this task",
        "execute this task",
        "perform these steps",
        "do these steps",
        "task karo",
        "ye task karo",
        "ye kaam karo"
    ]

    normalized = command.lower()

    # Keep task requests together
    if any(phrase in normalized for phrase in task_phrases):
        return [command]

    separators = [
        " and ",
        " aur ",
        " then ",
        " phir "
    ]

    commands = [command]

    for sep in separators:
        new_commands = []

        for cmd in commands:
            new_commands.extend(cmd.split(sep))

        commands = new_commands

    return [
        cmd.strip()
        for cmd in commands
        if cmd.strip()
    ]