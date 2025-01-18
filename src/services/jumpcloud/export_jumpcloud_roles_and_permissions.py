import requests
import json
from datetime import datetime
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_policies():
    """Fetch policies defining roles and permissions from JumpCloud."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    response = requests.get(f"{JC_URL}/v2/policies", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch policies: {response.status_code} - {response.text}")
        return []

def write_policies_to_json(policies):
    """Write policies to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/policies/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_Roles_and_Permissions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(policies, file, indent=4)
    print(f"Policies defining roles and permissions written to {file_name}")

if __name__ == "__main__":
    policies = fetch_policies()
    if policies:
        write_policies_to_json(policies)
    else:
        print("No policies found or failed to fetch policies.")
