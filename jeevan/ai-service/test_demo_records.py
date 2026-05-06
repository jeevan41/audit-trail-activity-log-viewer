import requests
import json
import time

# Demo audit log entries
demo_logs = [
    "2024-01-15 10:30:45 - User 'john.doe' successfully logged in from IP 192.168.1.100",
    "2024-01-15 10:31:22 - User 'admin' accessed file '/etc/passwd' with read permissions",
    "2024-01-15 10:32:10 - Failed login attempt for user 'root' from IP 10.0.0.5",
    "2024-01-15 10:33:05 - User 'alice' modified configuration file '/app/config.json'",
    "2024-01-15 10:34:18 - Database query executed: SELECT * FROM users WHERE role='admin'",
    "2024-01-15 10:35:30 - User 'bob' attempted to access restricted directory '/secure/data'",
    "2024-01-15 10:36:45 - System backup completed successfully, 2.3GB transferred",
    "2024-01-15 10:37:12 - User 'charlie' changed password for account 'service_account'",
    "2024-01-15 10:38:25 - Multiple failed login attempts detected from IP 203.0.113.1",
    "2024-01-15 10:39:40 - User 'diana' exported 1500 records from customer database",
    "2024-01-15 10:40:55 - Privilege escalation attempt blocked for user 'eve'",
    "2024-01-15 10:41:18 - SSL certificate renewed for domain 'api.company.com'",
    "2024-01-15 10:42:30 - User 'frank' accessed API endpoint '/admin/users' 50 times in 1 minute",
    "2024-01-15 10:43:45 - Firewall rule added: block traffic from 192.168.1.0/24 to port 22",
    "2024-01-15 10:44:12 - User 'grace' deleted temporary files older than 30 days",
    "2024-01-15 10:45:25 - Unusual network traffic detected: 500MB outbound to unknown IP",
    "2024-01-15 10:46:40 - User 'henry' granted admin privileges to user 'ivy'",
    "2024-01-15 10:47:55 - Database connection pool exhausted, 100 active connections",
    "2024-01-15 10:48:18 - User 'jack' attempted SQL injection: ' OR 1=1 --",
    "2024-01-15 10:49:30 - System memory usage spiked to 95% for 5 minutes",
    "2024-01-15 10:50:45 - User 'kate' accessed sensitive HR records for 20 employees",
    "2024-01-15 10:51:12 - VPN connection established from IP 198.51.100.1",
    "2024-01-15 10:52:25 - User 'liam' modified system cron jobs",
    "2024-01-15 10:53:40 - Failed authentication attempts: 25 in last 10 minutes from same IP",
    "2024-01-15 10:54:55 - User 'mia' downloaded entire product catalog (5GB)",
    "2024-01-15 10:55:18 - Security patch applied to all servers in cluster",
    "2024-01-15 10:56:30 - User 'noah' queried logs for 'password' keyword 10 times",
    "2024-01-15 10:57:45 - Unusual login time: user 'olivia' logged in at 3:00 AM",
    "2024-01-15 10:58:12 - User 'peter' attempted to mount external USB device",
    "2024-01-15 10:59:25 - System integrity check passed for all critical files"
]

BASE_URL = "http://127.0.0.1:5000"

def test_describe_endpoint():
    print("Testing /describe endpoint with 30 demo records...")
    results = []
    
    for i, log in enumerate(demo_logs, 1):
        try:
            response = requests.post(f"{BASE_URL}/describe", 
                                   json={"log_entry": log}, 
                                   timeout=30)
            if response.status_code == 200:
                result = response.json()
                results.append({
                    "record_id": i,
                    "log_entry": log,
                    "description": result.get("description", ""),
                    "generated_at": result.get("generated_at", ""),
                    "is_fallback": result.get("is_fallback", False)
                })
                print(f"✓ Record {i}: {result.get('description', '')[:50]}...")
            else:
                print(f"✗ Record {i}: HTTP {response.status_code}")
                results.append({
                    "record_id": i,
                    "log_entry": log,
                    "error": f"HTTP {response.status_code}",
                    "response": response.text
                })
        except Exception as e:
            print(f"✗ Record {i}: Exception - {str(e)}")
            results.append({
                "record_id": i,
                "log_entry": log,
                "error": str(e)
            })
        time.sleep(0.5)  # Rate limiting
    
    return results

def test_recommend_endpoint():
    print("Testing /recommend endpoint with 30 demo records...")
    results = []
    
    for i, log in enumerate(demo_logs, 1):
        try:
            response = requests.post(f"{BASE_URL}/recommend", 
                                   json={"log_entry": log}, 
                                   timeout=30)
            if response.status_code == 200:
                result = response.json()
                results.append({
                    "record_id": i,
                    "log_entry": log,
                    "recommendations": result.get("recommendations", []),
                    "generated_at": result.get("generated_at", ""),
                    "is_fallback": result.get("is_fallback", False)
                })
                print(f"✓ Record {i}: {len(result.get('recommendations', []))} recommendations")
            else:
                print(f"✗ Record {i}: HTTP {response.status_code}")
                results.append({
                    "record_id": i,
                    "log_entry": log,
                    "error": f"HTTP {response.status_code}",
                    "response": response.text
                })
        except Exception as e:
            print(f"✗ Record {i}: Exception - {str(e)}")
            results.append({
                "record_id": i,
                "log_entry": log,
                "error": str(e)
            })
        time.sleep(0.5)  # Rate limiting
    
    return results

def test_generate_report_endpoint():
    print("Testing /generate-report endpoint with all 30 demo records...")
    
    try:
        response = requests.post(f"{BASE_URL}/generate-report", 
                               json={"logs": demo_logs}, 
                               timeout=60)
        if response.status_code == 200:
            result = response.json()
            print("✓ Report generated successfully")
            return {
                "title": result.get("title", ""),
                "summary": result.get("summary", ""),
                "overview": result.get("overview", ""),
                "key_items": result.get("key_items", []),
                "recommendations": result.get("recommendations", []),
                "generated_at": result.get("generated_at", ""),
                "is_fallback": result.get("is_fallback", False)
            }
        else:
            print(f"✗ Report generation failed: HTTP {response.status_code}")
            return {
                "error": f"HTTP {response.status_code}",
                "response": response.text
            }
    except Exception as e:
        print(f"✗ Report generation exception: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    print("Starting comprehensive AI service testing with 30 demo records...")
    print("=" * 60)
    
    # Test all endpoints
    describe_results = test_describe_endpoint()
    print("\n" + "=" * 60)
    
    recommend_results = test_recommend_endpoint()
    print("\n" + "=" * 60)
    
    report_result = test_generate_report_endpoint()
    print("\n" + "=" * 60)
    
    # Save results to file
    output = {
        "describe_results": describe_results,
        "recommend_results": recommend_results,
        "report_result": report_result,
        "total_records_tested": len(demo_logs),
        "endpoints_tested": ["describe", "recommend", "generate-report"]
    }
    
    with open("demo_test_results.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("Demo testing completed! Results saved to demo_test_results.json")
    print(f"Total records tested: {len(demo_logs)}")
    print(f"Describe endpoint: {len([r for r in describe_results if 'error' not in r])} successful")
    print(f"Recommend endpoint: {len([r for r in recommend_results if 'error' not in r])} successful")
    print(f"Report endpoint: {'successful' if 'error' not in report_result else 'failed'}")