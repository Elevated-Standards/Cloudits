import requests
import json
from datetime import datetime, timedelta
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_admin_actions():
    """Fetch logs of administrative actions in the past 30 days."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat() + "Z"
    query_params = {
        "startTime": thirty_days_ago,
        "eventType": [
            "user.created",  # User account created
            "user.deleted",  # User account deleted
            "policy.updated",  # Security policy updated
            "policy.created",  # Security policy created
            "policy.deleted",  # Security policy deleted
            "group.created",  # Group created
            "group.deleted",  # Group deleted
            "group.updated"   # Group updated
        ],
        "limit": 1000  # Adjust if necessary
    }

    response = requests.get(f"{JC_URL}/v2/systemevents", headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch admin actions: {response.status_code} - {response.text}")
        return []

def write_admin_actions_to_json(events):
    """Write administrative action logs to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/admin-actions/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_Admin_Actions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(events, file, indent=4)
    print(f"Administrative action logs written to {file_name}")

if __name__ == "__main__":
    admin_actions = fetch_admin_actions()
    if admin_actions:
        write_admin_actions_to_json(admin_actions)
    else:
        print("No administrative actions found in the past 30 days.")
