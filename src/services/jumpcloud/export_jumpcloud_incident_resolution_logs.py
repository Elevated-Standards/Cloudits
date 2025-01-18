import requests
import json
from datetime import datetime, timedelta
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_incident_resolution_logs():
    """Fetch logs of actions taken to resolve detected incidents in the past 30 days."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat() + "Z"
    query_params = {
        "startTime": thirty_days_ago,
        "eventType": [
            "incident.response",  # General incident response
            "alert.response",     # Response to triggered alerts
            "policy.updated",     # Policy updates to resolve issues
            "user.updated"        # Actions on user accounts as part of resolution
        ],
        "limit": 1000  # Adjust if necessary
    }

    response = requests.get(f"{JC_URL}/v2/systemevents", headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch incident resolution logs: {response.status_code} - {response.text}")
        return []

def write_incident_resolution_logs_to_json(logs):
    """Write incident resolution logs to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/incident-resolution/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_Incident_Resolution_Logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(logs, file, indent=4)
    print(f"Incident resolution logs written to {file_name}")

if __name__ == "__main__":
    resolution_logs = fetch_incident_resolution_logs()
    if resolution_logs:
        write_incident_resolution_logs_to_json(resolution_logs)
    else:
        print("No incident resolution logs found in the past 30 days.")
