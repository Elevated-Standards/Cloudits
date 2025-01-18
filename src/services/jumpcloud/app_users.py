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
def fetch_applications():
    """Fetch all applications from JumpCloud."""
    headers = get_headers()
    response = requests.get(f"{JC_URL}applications", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch applications: {response.status_code} - {response.text}")
        return []

def fetch_users_for_application(app_id):
    """Fetch users assigned to a specific application."""
    headers = get_headers()
    response = requests.get(f"{JC_URL}applications/{app_id}/users", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch users for application {app_id}: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    applications = fetch_applications()
    if applications:
        for app in applications:
            app_id = app.get("id")
            app_name = app.get("name", "UnknownApp")
            print(f"Processing application: {app_name} (ID: {app_id})")

            users = fetch_users_for_application(app_id)
            if users:
                # Extract last sign-on details, if available
                enriched_users = []
                for user in users:
                    enriched_users.append({
                        "id": user.get("id"),
                        "email": user.get("email"),
                        "username": user.get("username"),
                        "last_sign_on": user.get("last_sign_on", "Never")
                    })

                # Use the generic `write_to_json` function
                sanitized_app_name = "".join(c if c.isalnum() else "_" for c in app_name)
                write_to_json(
                    enriched_users, 
                    'identity_and_access', 
                    f'applications/{sanitized_app_name}_users'
                )
            else:
                print(f"No users found for application: {app_name}")
    else:
        print("No applications found or failed to fetch applications.")
