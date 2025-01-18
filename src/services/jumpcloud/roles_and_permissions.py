import requests
from datetime import datetime, timezone
from utils.jc_utils import (
    JC_URL,
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
def fetch_policies():
    """Fetch policies defining roles and permissions from JumpCloud."""
    headers = get_headers()
    response = requests.get(f"{JC_URL}policies", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch policies: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    policies = fetch_policies()
    if policies:
        # Use the generic `write_to_json` function
        write_to_json(policies, 'identity_and_access', 'policies')
    else:
        print("No policies found or failed to fetch policies.")