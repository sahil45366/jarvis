import math
import re


def calculate(command):

    command = command.lower()


    try:

        # Hindi + speech correction

        command = command.replace("ka", "")
        command = command.replace("x", "*")
        command = command.replace("×", "*")

        command = command.replace("plus", "+")
        command = command.replace("add", "+")

        command = command.replace("minus", "-")
        command = command.replace("subtract", "-")

        command = command.replace("multiply", "*")
        command = command.replace("times", "*")

        command = command.replace("divide", "/")
        command = command.replace("by", "")


        # Square

        if "square" in command:

            number = re.findall(
                r'\d+',
                command
            )

            if number:

                return int(number[0]) ** 2



        # Remove words

        command = command.replace(
            "calculate",
            ""
        )


        result = eval(command)


        return result



    except Exception as e:

        print(
            "Calculator Error:",
            e
        )

        return None