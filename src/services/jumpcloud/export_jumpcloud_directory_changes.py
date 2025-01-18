import requests
import json
from datetime import datetime, timedelta
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_change_events():
    """Fetch records of changes to directory configurations, device settings, or security policies in the past 30 days."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat() + "Z"
    query_params = {
        "startTime": thirty_days_ago,
        "eventType": [
            "directory.config.updated",
            "device.settings.updated",
            "policy.updated"
        ],
        "limit": 1000  # Adjust if necessary
    }

    response = requests.get(f"{JC_URL}/v2/systemevents", headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch change events: {response.status_code} - {response.text}")
        return []

def write_change_events_to_json(events):
    """Write change event records to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/change-events/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_Change_Records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(events, file, indent=4)
    print(f"Change records written to {file_name}")

if __name__ == "__main__":
    change_events = fetch_change_events()
    if change_events:
        write_change_events_to_json(change_events)
    else:
        print("No changes to directory configurations, device settings, or security policies found in the past 30 days.")
