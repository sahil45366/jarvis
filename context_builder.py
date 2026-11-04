from window_detector import get_active_window


def build_screen_context(window_info=None, screen_analysis=None):

    # Automatically detect active application
    if window_info is None:
        window_info = get_active_window()

    if not window_info and not screen_analysis:
        return ""

    context = []

    context.append("CURRENT SCREEN CONTEXT:")

    if window_info:
        context.append(
            f"Active Application: {window_info.get('process_name', 'Unknown')}"
        )

        context.append(
            f"Window Title: {window_info.get('window_title', 'Unknown')}"
        )

        context.append(
            f"Process ID: {window_info.get('process_id', 'Unknown')}"
        )

    if screen_analysis:
        context.append(
            f"Screen Description: {screen_analysis}"
        )

    return "\n".join(context)


def build_ai_prompt(user_command, screen_context=""):

    prompt = f"""
USER COMMAND:
{user_command}
"""

    if screen_context:
        prompt += f"""

{screen_context}

Use this screen information only as context.
Do not assume an action has been completed.
Prefer the currently active application when planning
application-specific actions.
"""

    return prompt