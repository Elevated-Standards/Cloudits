import requests
import json
from datetime import datetime
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_groups():
    """Fetch all groups from JumpCloud."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    response = requests.get(f"{JC_URL}/v2/groups", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch groups: {response.status_code} - {response.text}")
        return []

def fetch_users_for_group(group_id):
    """Fetch users for a specific group by its ID."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    response = requests.get(f"{JC_URL}/v2/groups/{group_id}/members", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch users for group {group_id}: {response.status_code} - {response.text}")
        return []

def write_users_to_json(group_name, users_data):
    """Write user data to a JSON file with timestamp for a specific group."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/groups/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    sanitized_group_name = "".join(c if c.isalnum() else "_" for c in group_name)
    file_name = f"{directory}Jumpcloud_Group_{sanitized_group_name}_Users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(users_data, file, indent=4)
    print(f"User list for group '{group_name}' written to {file_name}")

if __name__ == "__main__":
    groups = fetch_groups()
    if groups:
        for group in groups:
            group_id = group.get("id")
            group_name = group.get("name", "UnknownGroup")
            print(f"Processing group: {group_name} (ID: {group_id})")
            users = fetch_users_for_group(group_id)
            if users:
                write_users_to_json(group_name, users)
            else:
                print(f"No users found for group: {group_name}")
    else:
        print("No groups found or failed to fetch groups.")
