import requests
from datetime import datetime, timezone
from utils.jc_utils import (
    JC_URL,
    calculate_dynamic_start_time,
    get_base_dir,
    get_current_date_info,
    get_headers,
    write_to_json  # Import the generic write function
)

# Fetch shared date information and base directory
date_info = get_current_date_info()
BASE_DIR = get_base_dir()
YEAR = date_info["year"]
MONTH = date_info["month"]
END_DATE = date_info["end_date"]

def fetch_api_interactions():
    """Fetch API interactions for system integrations in the past dynamic time range."""
    headers = get_headers()
    dynamic_start_time = calculate_dynamic_start_time()
    query_params = {
        "startTime": dynamic_start_time,
        "eventType": [
            "api.request.success",  # Successful API requests
            "api.request.error"     # Failed API requests
        ],
        "limit": 1000  # Adjust if necessary
    }

    response = requests.get(f"{JC_URL}systemevents", headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch API interactions: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    api_events = fetch_api_interactions()
    if api_events:
        # Use the generic `write_to_json` function
        write_to_json(api_events, 'identity_and_access', 'api-interactions')
    else:
        print("No API interactions found for system integrations in the past dynamic range.")