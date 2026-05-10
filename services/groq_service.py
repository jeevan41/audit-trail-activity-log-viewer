from datetime import datetime

from datetime import datetime

def generate_description(data):

    try:

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
            "generated_at": datetime.now().isoformat(),
            "is_fallback": False
        }

    except Exception as e:

        print("AI generation error:", str(e))

        return {
            "description": "Unable to generate audit description currently.",
            "risk_level": "UNKNOWN",
            "generated_at": datetime.now().isoformat(),
            "is_fallback": True
        }
    
def generate_recommendations(data):

    try:

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
            "recommendations": recommendations,
            "is_fallback": False
        }

    except Exception as e:

        print("Recommendation error:", str(e))

        return {
            "recommendations": [],
            "is_fallback": True
        }
    

def generate_report(data):

    try:

        system_name = data.get("system_name", "Unknown System")
        total_events = data.get("total_events", 0)
        failed_logins = data.get("failed_logins", 0)
        suspicious_activities = data.get("suspicious_activities", 0)

        return {
            "title": "Audit Activity Report",

            "summary": (
                f"The {system_name} recorded {total_events} audit events. "
                f"{failed_logins} failed login attempts and "
                f"{suspicious_activities} suspicious activities were detected."
            ),

            "overview": (
                "This report provides an overview of system audit activities "
                "and highlights security-related events."
            ),

            "key_items": [
                f"Total Events: {total_events}",
                f"Failed Logins: {failed_logins}",
                f"Suspicious Activities: {suspicious_activities}"
            ],

            "recommendations": [
                "Monitor failed login trends regularly.",
                "Investigate suspicious activities immediately.",
                "Enable stricter authentication policies."
            ],

            "generated_at": datetime.now().isoformat(),
            "is_fallback": False
        }

    except Exception as e:

        print("Generate report error:", str(e))

        return {
            "title": "Fallback Audit Report",
            "summary": "Unable to generate report currently.",
            "overview": "Fallback response generated.",
            "key_items": [],
            "recommendations": [],
            "generated_at": datetime.now().isoformat(),
            "is_fallback": True
        }