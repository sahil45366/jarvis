ALLOWED_ACTIONS = {
    "open_app",
    "google_search",
    "youtube_search",
    "capture_screen",
    "type_text"
}

ALLOWED_APPS = {
    "chrome",
    "google chrome",
    "edge",
    "microsoft edge",
    "notepad",
    "calculator"
}

# Only these actions can run without approval.
LOW_RISK_ACTIONS = {
    "open_app",
    "google_search",
    "youtube_search"
}


def check_task_safety(plan):

    if not isinstance(plan, dict):
        return {
            "safe": False,
            "requires_confirmation": True,
            "reason": "Invalid task plan."
        }

    steps = plan.get("steps")

    if not isinstance(steps, list) or not steps:
        return {
            "safe": False,
            "requires_confirmation": True,
            "reason": "Task has no valid steps."
        }

    if len(steps) > 10:
        return {
            "safe": False,
            "requires_confirmation": True,
            "reason": "Too many steps in one task."
        }

    requires_confirmation = False
    notepad_opened = False

    for step in steps:

        if not isinstance(step, dict):
            return {
                "safe": False,
                "requires_confirmation": True,
                "reason": "Invalid step format."
            }

        action = step.get("action")
        target = step.get("target")

        if action not in ALLOWED_ACTIONS:
            return {
                "safe": False,
                "requires_confirmation": True,
                "reason": f"Action not allowed: {action}"
            }

        if not isinstance(target, str) or not target.strip():
            return {
                "safe": False,
                "requires_confirmation": True,
                "reason": "Missing or invalid target."
            }

        target = target.strip()

        if len(target) > 2000:
            return {
                "safe": False,
                "requires_confirmation": True,
                "reason": "Target exceeds the 2000-character limit."
            }

        if action == "open_app":

            app_name = target.lower()

            if app_name not in ALLOWED_APPS:
                return {
                    "safe": False,
                    "requires_confirmation": True,
                    "reason": f"App not approved: {target}"
                }

            notepad_opened = app_name == "notepad"

        elif action == "type_text":

            # Typing is permitted only after Notepad is opened.
            if notepad_opened is not True:
                return {
                    "safe": False,
                    "requires_confirmation": True,
                    "reason": "Text entry is allowed only after opening Notepad."
                }

            requires_confirmation = True

        if action not in LOW_RISK_ACTIONS:
            requires_confirmation = True

        if action == "capture_screen":

            from observation_settings import is_observation_enabled

            if not is_observation_enabled():
                return {
                    "safe": False,
                    "requires_confirmation": True,
                    "reason": "Screen observation is OFF."
                }

    return {
        "safe": True,
        "requires_confirmation": requires_confirmation,
        "reason": "All task steps passed safety checks."
    }


if __name__ == "__main__":

    sample_plan = {
        "goal": "Open Notepad and write Python topics",
        "steps": [
            {"action": "open_app", "target": "notepad"},
            {"action": "type_text", "target": "Python, NumPy and Pandas"}
        ]
    }

    print(check_task_safety(sample_plan))