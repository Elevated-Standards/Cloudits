import requests
import json
from datetime import datetime, timedelta
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_device_location_logs():
    """Fetch device location tracking logs for remote devices in the past 30 days."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat() + "Z"
    query_params = {
        "startTime": thirty_days_ago,
        "eventType": "device.location.updated",  # Event type for location tracking updates
        "limit": 1000  # Adjust if necessary
    }

    response = requests.get(f"{JC_URL}/v2/systemevents", headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch device location logs: {response.status_code} - {response.text}")
        return []

def write_device_location_logs_to_json(location_logs):
    """Write device location tracking logs to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/device-location-logs/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_Device_Location_Logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(location_logs, file, indent=4)
    print(f"Device location tracking logs written to {file_name}")

if __name__ == "__main__":
    location_logs = fetch_device_location_logs()
    if location_logs:
        write_device_location_logs_to_json(location_logs)
    else:
        print("No device location tracking logs found in the past 30 days.")
