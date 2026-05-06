import json
import requests

BASE_URL = "http://127.0.0.1:5000"

record = {
    "log_entry": "2026-05-06 15:00:00 - Suspicious login detected from IP 203.0.113.77 for user 'admin'"
}


def describe_record():
    response = requests.post(f"{BASE_URL}/describe", json=record, timeout=30)
    print("\n=== /describe Response ===")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except ValueError:
        print(response.text)


def recommend_record():
    response = requests.post(f"{BASE_URL}/recommend", json=record, timeout=30)
    print("\n=== /recommend Response ===")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except ValueError:
        print(response.text)


if __name__ == '__main__':
    print("Live Demo: sending one record to the AI service")
    describe_record()
    recommend_record()
