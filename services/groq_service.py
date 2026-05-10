from datetime import datetime

def generate_description(data):
    
    action = data.get("action_type", "UNKNOWN")
    username = data.get("username", "Unknown User")
    module = data.get("module", "Unknown Module")
    status = data.get("status", "UNKNOWN")

    risk_level = "LOW"

    if "FAILED" in status.upper():
        risk_level = "MEDIUM"

    if "MULTIPLE LOGIN ATTEMPTS" in action.upper():
        risk_level = "HIGH"

    description = (
        f"User {username} performed {action} action "
        f"in the {module} module with status {status}."
    )

    return {
        "description": description,
        "risk_level": risk_level,
        "generated_at": datetime.now().isoformat()
    }