import requests
import json
from datetime import datetime, timedelta
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_security_policy_changes():
    """Fetch evidence of modifications to security policies in the past 30 days."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat() + "Z"
    query_params = {
        "startTime": thirty_days_ago,
        "eventType": [
            "policy.updated",  # Captures updates to security policies
            "policy.created",  # Captures creation of new security policies
            "policy.deleted"   # Captures deletion of security policies
        ],
        "limit": 1000  # Adjust if necessary
    }

    response = requests.get(f"{JC_URL}/v2/systemevents", headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch security policy changes: {response.status_code} - {response.text}")
        return []

def write_security_policy_changes_to_json(events):
    """Write evidence of security policy modifications to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/security-policies/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_Security_Policy_Changes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(events, file, indent=4)
    print(f"Security policy change records written to {file_name}")

if __name__ == "__main__":
    policy_changes = fetch_security_policy_changes()
    if policy_changes:
        write_security_policy_changes_to_json(policy_changes)
    else:
        print("No modifications to security policies found in the past 30 days.")
