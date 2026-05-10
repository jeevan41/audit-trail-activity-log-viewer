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

def generate_recommendations(data):

    action = data.get("action_type", "").upper()
    status = data.get("status", "").upper()

    recommendations = []

    if "LOGIN" in action and "FAILED" in status:
        recommendations.append({
            "action_type": "ACCOUNT_REVIEW",
            "description": "Review failed login attempts for suspicious activity.",
            "priority": "HIGH"
        })

    recommendations.append({
        "action_type": "MONITOR_ACTIVITY",
        "description": "Continue monitoring user activity logs regularly.",
        "priority": "MEDIUM"
    })

    recommendations.append({
        "action_type": "SECURITY_AUDIT",
        "description": "Perform periodic security audits for sensitive modules.",
        "priority": "LOW"
    })

    return {
        "recommendations": recommendations
    }