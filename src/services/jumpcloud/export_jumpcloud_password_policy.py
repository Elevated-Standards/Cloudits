import requests
import json
from datetime import datetime
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_password_policy():
    """Fetch the password policy from JumpCloud."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    response = requests.get(f"{JC_URL}/v2/systeminsights/settings/policies/password", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch password policy: {response.status_code} - {response.text}")
        return {}

def write_password_policy_to_json(policy_data):
    """Write the password policy to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/policies/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_Password_Policy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(policy_data, file, indent=4)
    print(f"Password policy written to {file_name}")

if __name__ == "__main__":
    policy = fetch_password_policy()
    if policy:
        write_password_policy_to_json(policy)
    else:
        print("No password policy found or failed to fetch policy.")
