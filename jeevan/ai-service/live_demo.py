import json
import requests

BASE_URL = "http://127.0.0.1:5000"

record = {
    "log_entry": "2026-05-06 15:00:00 - Suspicious login detected from IP 203.0.113.77 for user 'admin'"
}


def explain_step(step_name, explanation):
    print(f"\n--- {step_name} ---")
    print(explanation)


def describe_record():
    explain_step(
        "/describe",
        "The AI reads the log entry and generates a human-friendly description of the event. "
        "If the Groq API is unavailable, fallback text is returned while preserving the same response shape."
    )
    response = requests.post(f"{BASE_URL}/describe", json=record, timeout=30)
    print("\nResponse:")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except ValueError:
        print(response.text)


def recommend_record():
    explain_step(
        "/recommend",
        "The AI examines the same log entry and returns exactly three recommendations. "
        "Each recommendation includes an action type, a description, and a priority level."
    )
    response = requests.post(f"{BASE_URL}/recommend", json=record, timeout=30)
    print("\nResponse:")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except ValueError:
        print(response.text)


def generate_report():
    explain_step(
        "/generate-report",
        "The AI takes the log entry list and generates a structured audit report. "
        "This report includes a title, summary, overview, key findings, and recommendations."
    )
    payload = {"logs": [record['log_entry']]}
    response = requests.post(f"{BASE_URL}/generate-report", json=payload, timeout=60)
    print("\nResponse:")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except ValueError:
        print(response.text)


if __name__ == '__main__':
    print("Live Demo: sending one record through Describe, Recommend, and Generate Report")
    describe_record()
    recommend_record()
    generate_report()
