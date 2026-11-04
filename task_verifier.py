def verify_execution(execution_report):

    if not isinstance(execution_report, dict):
        return {
            "status": "INVALID",
            "message": "Execution report is invalid."
        }

    results = execution_report.get("results", [])

    if not isinstance(results, list) or not results:
        return {
            "status": "NO_RESULTS",
            "message": "No execution results were provided."
        }

    verified = []
    failed = []
    needs_check = []

    verified_messages = {
        "App launched and focused successfully.",
        "Google search page load verified.",
        "YouTube search page load verified.",
        "Screen captured."
    }

    for item in results:

        if not isinstance(item, dict):
            failed.append("Invalid result entry.")
            continue

        message = item.get(
            "message",
            "No details provided."
        )

        if not item.get("success", False):
            failed.append(message)

        elif message in verified_messages:
            verified.append(message)

        else:
            needs_check.append(message)

    if failed:
        status = "PARTIAL_OR_FAILED"

    elif needs_check:
        status = "NEEDS_VERIFICATION"

    else:
        status = "VERIFIED"

    return {
        "status": status,
        "verified": verified,
        "failed": failed,
        "needs_check": needs_check
    }


if __name__ == "__main__":

    sample_report = {
        "success": True,
        "results": [
            {
                "success": True,
                "message": "App launched and focused successfully."
            },
            {
                "success": True,
                "message": "Google search page load verified."
            }
        ]
    }

    print("JARVIS VERIFICATION:")
    print(verify_execution(sample_report))