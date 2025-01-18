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
def fetch_failed_login_attempts():
    """Fetch failed login events from JumpCloud in the past dynamic time range."""
    headers = get_headers()
    dynamic_start_time = calculate_dynamic_start_time()
    query_params = {
        "startTime": dynamic_start_time,
        "eventType": "login.failed",
        "limit": 1000  # Adjust if necessary
    }

    response = requests.get(f"{JC_URL}systemevents", headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch login events: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    failed_login_events = fetch_failed_login_attempts()
    if failed_login_events:
        # Use the generic `write_to_json` function
        write_to_json(failed_login_events, 'identity_and_access', 'login-events')
    else:
        print("No failed login events found in the past dynamic range.")