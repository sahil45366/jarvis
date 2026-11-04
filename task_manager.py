from task_planner import create_task_plan
from task_executor import execute_plan
from task_verifier import verify_execution
from task_confirmation import request_task_confirmation
from task_safety import check_task_safety
from context_builder import build_screen_context


def process_task(command, screen_context=""):

    # 1. Get active application context
    if not screen_context:
        screen_context = build_screen_context()

    # 2. Create task plan
    plan = create_task_plan(command, screen_context)

    if not plan:
        return {
            "status": "PLANNING_FAILED",
            "message": "Could not create a valid task plan."
        }

    # 3. Safety check
    safety = check_task_safety(plan)

    if not safety.get("safe", False):
        return {
            "status": "BLOCKED",
            "message": safety.get("reason", "Safety check failed."),
            "plan": plan
        }

    # 4. Approval only when required
    if safety.get("requires_confirmation", True):

        approved = request_task_confirmation(plan)

        if not approved:
            return {
                "status": "CANCELLED",
                "message": "User did not approve the task."
            }

    else:
        print("Low-risk task. Automatic execution approved.")

    # 5. Execute task
    execution_report = execute_plan(plan)

    # 6. Verify execution
    verification = verify_execution(execution_report)

    return {
        "status": verification["status"],
        "plan": plan,
        "execution": execution_report,
        "verification": verification
    }