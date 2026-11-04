
def request_task_confirmation(plan):
    if not isinstance(plan, dict):
        print("Invalid task plan.")
        return False

    steps = plan.get("steps", [])

    if not isinstance(steps, list) or not steps:
        print("No valid steps found.")
        return False

    print("\n========== JARVIS TASK APPROVAL ==========")
    print("Goal:", plan.get("goal", "Unknown"))

    print("\nPlanned actions:")

    for index, step in enumerate(steps, start=1):
        action = step.get("action", "Unknown")
        target = step.get("target", "")
        print(f"{index}. {action} -> {target}")

    print("\nDo you want JARVIS to execute this plan?")
    answer = input("Type YES to approve: ").strip().upper()

    if answer == "YES":
        print("Task approved.")
        return True

    print("Task cancelled. No actions executed.")
    return False


if __name__ == "__main__":
    sample_plan = {
        "goal": "Open Chrome and search for Python tutorials",
        "steps": [
            {"action": "open_app", "target": "chrome"},
            {"action": "google_search", "target": "Python tutorials"}
        ]
    }

    approved = request_task_confirmation(sample_plan)
    print("Approval:", approved)
