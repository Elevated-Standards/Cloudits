import requests
import json
from datetime import datetime, timedelta
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_failed_login_attempts():
    """Fetch failed login events from JumpCloud in the past 30 days."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat() + "Z"
    query_params = {
        "startTime": thirty_days_ago,
        "eventType": "login.failed",
        "limit": 1000  # Adjust if necessary
    }

    response = requests.get(f"{JC_URL}/v2/systemevents", headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch login events: {response.status_code} - {response.text}")
        return []

def write_failed_login_attempts_to_json(events):
    """Write failed login events to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/login-events/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_Failed_Login_Attempts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(events, file, indent=4)
    print(f"Failed login events written to {file_name}")

if __name__ == "__main__":
    failed_login_events = fetch_failed_login_attempts()
    if failed_login_events:
        write_failed_login_attempts_to_json(failed_login_events)
    else:
        print("No failed login events found in the past 30 days.")
