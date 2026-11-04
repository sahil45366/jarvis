
import json
import re


# Must match task_executor.py
ALLOWED_ACTIONS = {
    "open_app",
    "google_search",
    "youtube_search",
    "capture_screen",
    "type_text"
}


def extract_json(text):

    if not isinstance(text, str):
        return None

    # Remove Markdown JSON code fences if present
    text = re.sub(
        r"```(?:json)?",
        "",
        text,
        flags=re.IGNORECASE
    ).replace("```", "").strip()

    # Extract JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        return None

    try:
        return json.loads(match.group())

    except json.JSONDecodeError as error:
        print("JSON Parsing Error:", error)
        return None


def validate_plan(plan):

    if not isinstance(plan, dict):
        return False

    steps = plan.get("steps")

    if not isinstance(steps, list) or not steps:
        return False

    for step in steps:

        if not isinstance(step, dict):
            return False

        if step.get("action") not in ALLOWED_ACTIONS:
            return False

        target = step.get("target")

        if not isinstance(target, str) or not target.strip():
            return False

    if not isinstance(plan.get("requires_confirmation"), bool):
        return False
    # Typing always requires user confirmation.
    if any(
        step.get("action") == "type_text"
        for step in steps
    ):
        plan["requires_confirmation"] = True
    return True


def create_task_plan(command, screen_context=""):

    prompt = f"""
You are JARVIS Task Planner.

Convert the user's command into a sequence of executable actions.

IMPORTANT RULES:

1. Return valid JSON only.
2. Never execute actions yourself.
3. Use only the allowed actions.
4. Never invent screen information.
5. If the user asks to open an app and then search,
   open the app FIRST and search SECOND.
6. Do not generate a search action before opening the requested browser.
7. Ask for clarification if the requested task is unclear.
8. Set requires_confirmation to true for consequential actions.
9. Do not claim that an action has already been completed.
10. For writing text, use the type_text action.
11. Always open Notepad before using type_text.
12. Use type_text only for text explicitly provided by the user.
13. Never use type_text in a browser or an unknown application.
14. Do not create, edit, or overwrite files.

Allowed actions:
{sorted(ALLOWED_ACTIONS)}

Screen context:
{screen_context}

User command:
{command}

Required JSON format:

{{
    "goal": "short task description",
    "steps": [
        {{"action": "open_app", "target": "chrome"}},
        {{"action": "google_search", "target": "Python tutorials"}}
    ],
    "requires_confirmation": false,
    "clarification": null
}}
"""

    try:

        from ollama_brain import ask_ollama

        response = ask_ollama(prompt)

        if not response:
            print("Empty response from Ollama.")
            return None

        plan = extract_json(response)

        if not validate_plan(plan):
            print("Invalid task plan.")
            print("Ollama response:", response)
            return None

        return plan

    except Exception as error:

        print("Task Planner Error:", error)
        return None


if __name__ == "__main__":

    plan = create_task_plan(
    "Open Notepad and write Python, NumPy and Pandas"
)

    print("\nJARVIS TASK PLAN:")
    print(json.dumps(plan, indent=4))
