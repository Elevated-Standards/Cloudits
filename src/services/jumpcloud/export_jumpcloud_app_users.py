import requests
import json
from datetime import datetime
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_applications():
    """Fetch all applications from JumpCloud."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    response = requests.get(f"{JC_URL}/v2/applications", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch applications: {response.status_code} - {response.text}")
        return []

def fetch_users_for_application(app_id):
    """Fetch users assigned to a specific application."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    response = requests.get(f"{JC_URL}/v2/applications/{app_id}/users", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch users for application {app_id}: {response.status_code} - {response.text}")
        return []

def write_app_users_to_json(app_name, user_data):
    """Write application user data to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/applications/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    sanitized_app_name = "".join(c if c.isalnum() else "_" for c in app_name)
    file_name = f"{directory}Jumpcloud_App_{sanitized_app_name}_Users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(user_data, file, indent=4)
    print(f"User list for application '{app_name}' written to {file_name}")

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
                write_app_users_to_json(app_name, enriched_users)
            else:
                print(f"No users found for application: {app_name}")
    else:
        print("No applications found or failed to fetch applications.")
