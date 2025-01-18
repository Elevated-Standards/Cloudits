import requests
from datetime import datetime, timezone
from utils.jc_utils import (
    JC_URL,
    get_base_dir,
    get_current_date_info,
    get_headers,
    calculate_dynamic_start_time,
    write_to_json  # Import the generic write function
)

# Fetch shared date information and base directory
date_info = get_current_date_info()
BASE_DIR = get_base_dir()
YEAR = date_info["year"]
MONTH = date_info["month"]
END_DATE = date_info["end_date"]
def fetch_change_events():
    """Fetch records of changes to directory configurations, device settings, or security policies in the past dynamic time range."""
    headers = get_headers()
    dynamic_start_time = calculate_dynamic_start_time()
    query_params = {
        "startTime": dynamic_start_time,
        "eventType": [
            "directory.config.updated",
            "device.settings.updated",
            "policy.updated"
        ],
        "limit": 1000  # Adjust if necessary
    }

    response = requests.get(f"{JC_URL}systemevents", headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch change events: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    change_events = fetch_change_events()
    if change_events:
        # Use the generic `write_to_json` function
        write_to_json(change_events, 'identity_and_access', 'change-events')
    else:
        print("No changes to directory configurations, device settings, or security policies found in the past dynamic range.")
