sample_logs = [
    {
        "username": "admin",
        "action_type": "LOGIN",
        "module": "Authentication",
        "timestamp": "2026-05-10 10:30:00",
        "ip_address": "192.168.1.10",
        "status": "SUCCESS"
    },
    {
        "username": "john",
        "action_type": "DELETE",
        "module": "User Management",
        "timestamp": "2026-05-10 11:00:00",
        "ip_address": "192.168.1.22",
        "status": "FAILED"
    },
    {
        "username": "unknown_user",
        "action_type": "MULTIPLE LOGIN ATTEMPTS",
        "module": "Authentication",
        "timestamp": "2026-05-10 11:15:00",
        "ip_address": "10.0.0.1",
        "status": "FAILED"
    },
    {
        "username": "manager",
        "action_type": "EXPORT",
        "module": "Reports",
        "timestamp": "2026-05-10 12:00:00",
        "ip_address": "172.16.0.5",
        "status": "SUCCESS"
    },
    {
        "username": "employee1",
        "action_type": "UPDATE",
        "module": "Payroll",
        "timestamp": "2026-05-10 01:20:00",
        "ip_address": "192.168.1.45",
        "status": "SUCCESS"
    }
]

for log in sample_logs:
    print("\nAudit Log:")
    print(log)