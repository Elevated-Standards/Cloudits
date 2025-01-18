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

def fetch_apps_for_group(group_id):
    """Fetch applications assigned to a specific group."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    response = requests.get(f"{JC_URL}/v2/groups/{group_id}/applications", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch applications for group {group_id}: {response.status_code} - {response.text}")
        return []

def write_groups_and_apps_to_json(groups_with_apps):
    """Write groups and their applications to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/groups-and-apps/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_Groups_And_Apps_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(groups_with_apps, file, indent=4)
    print(f"Groups and applications list written to {file_name}")

if __name__ == "__main__":
    groups = fetch_groups()
    if groups:
        groups_with_apps = []
        for group in groups:
            group_id = group.get("id")
            group_name = group.get("name", "UnknownGroup")
            print(f"Processing group: {group_name} (ID: {group_id})")
            
            apps = fetch_apps_for_group(group_id)
            group_data = {
                "group_id": group_id,
                "group_name": group_name,
                "applications": [
                    {"id": app.get("id"), "name": app.get("name")}
                    for app in apps
                ]
            }
            groups_with_apps.append(group_data)
        
        write_groups_and_apps_to_json(groups_with_apps)
    else:
        print("No groups found or failed to fetch groups.")
