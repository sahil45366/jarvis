import json
import os


FILE = "commands.json"


def load_commands():

    if os.path.exists(FILE):

        try:

            with open(FILE, "r") as f:
                return json.load(f)

        except:

            return {}


    return {}



def save_command(command, action):

    data = load_commands()


    command = command.lower().strip()
    action = action.lower().strip()


    data[command] = action


    with open(FILE,"w") as f:

        json.dump(
            data,
            f,
            indent=4
        )


    print("Command Saved:", command, "->", action)




def get_command(command):

    data = load_commands()


    command = command.lower().strip()


    # exact match

    if command in data:

        return data[command]



    # similar match

    for key, action in data.items():

        if key in command:

            print("Learned Match:", key)

            return action



    return None