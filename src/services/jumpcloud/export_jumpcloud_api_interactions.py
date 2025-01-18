import requests
import json
from datetime import datetime, timedelta
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_api_interactions():
    """Fetch API interactions for system integrations in the past 30 days."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat() + "Z"
    query_params = {
        "startTime": thirty_days_ago,
        "eventType": [
            "api.request.success",  # Successful API requests
            "api.request.error"     # Failed API requests
        ],
        "limit": 1000  # Adjust if necessary
    }

    response = requests.get(f"{JC_URL}/v2/systemevents", headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch API interactions: {response.status_code} - {response.text}")
        return []

def write_api_interactions_to_json(events):
    """Write API interactions to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/api-interactions/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_API_Interactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(events, file, indent=4)
    print(f"API interactions log written to {file_name}")

if __name__ == "__main__":
    api_events = fetch_api_interactions()
    if api_events:
        write_api_interactions_to_json(api_events)
    else:
        print("No API interactions found for system integrations in the past 30 days.")
