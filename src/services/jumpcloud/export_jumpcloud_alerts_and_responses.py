import requests
import json
from datetime import datetime, timedelta
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_alerts_and_responses():
    """Fetch evidence of triggered alerts and responses in the past 30 days."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat() + "Z"
    query_params = {
        "startTime": thirty_days_ago,
        "eventType": [
            "alert.triggered",  # Alert triggered
            "alert.response"    # Alert response
        ],
        "limit": 1000  # Adjust if necessary
    }

    response = requests.get(f"{JC_URL}/v2/systemevents", headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch alerts and responses: {response.status_code} - {response.text}")
        return []

def write_alerts_and_responses_to_json(alerts):
    """Write alerts and responses to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/alerts-and-responses/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_Alerts_and_Responses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(alerts, file, indent=4)
    print(f"Alerts and responses log written to {file_name}")

if __name__ == "__main__":
    alerts = fetch_alerts_and_responses()
    if alerts:
        write_alerts_and_responses_to_json(alerts)
    else:
        print("No alerts or responses found in the past 30 days.")
