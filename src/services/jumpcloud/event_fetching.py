import requests
import json
from datetime import datetime
import os
from utils.jc_utils import (
    JC_URL,
    calculate_dynamic_start_time,
    get_headers,
    get_base_dir,
    get_current_date_info
)

# Fetch shared date information and base directory
date_info = get_current_date_info()
BASE_DIR = get_base_dir()
YEAR = date_info["year"]
MONTH = date_info["month"]
END_DATE = date_info["end_date"]

# Fetch admin actions
def fetch_admin_actions():
    headers = get_headers()
    dynamic_start_time = calculate_dynamic_start_time()
    query_params = {
        "startTime": dynamic_start_time,
        "eventType": [
            "user.created", "user.deleted", "policy.updated",
            "policy.created", "policy.deleted", "group.created",
            "group.deleted", "group.updated"
        ],
        "limit": 1000
    }
    response = requests.get(f"{JC_URL}systemevents", headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch admin actions: {response.status_code} - {response.text}")
        return []

def write_admin_actions_to_json(events):
    directory = f"{BASE_DIR}/identity_and_access/jumpcloud/admin-actions/{YEAR}/{MONTH}/"
    os.makedirs(directory, exist_ok=True)
    file_name = f"{directory}{END_DATE}-Jumpcloud_Admin_Actions.json"
    with open(file_name, 'w') as file:
        json.dump(events, file, indent=4)
    print(f"Administrative action logs written to {file_name}")

# Fetch alerts and responses
def fetch_alerts_and_responses():
    headers = get_headers()
    dynamic_start_time = calculate_dynamic_start_time()
    query_params = {
        "startTime": dynamic_start_time,
        "eventType": ["alert.triggered", "alert.response"],
        "limit": 1000
    }
    response = requests.get(f"{JC_URL}systemevents", headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch alerts and responses: {response.status_code} - {response.text}")
        return []

def write_alerts_and_responses_to_json(alerts):
    directory = f"{BASE_DIR}/identity_and_access/jumpcloud/alerts-and-responses/{YEAR}/{MONTH}/"
    os.makedirs(directory, exist_ok=True)
    file_name = f"{directory}Jumpcloud_Alerts_and_Responses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(alerts, file, indent=4)
    print(f"Alerts and responses log written to {file_name}")

# Fetch incident resolution logs
def fetch_incident_resolution_logs():
    headers = get_headers()
    dynamic_start_time = calculate_dynamic_start_time()
    query_params = {
        "startTime": dynamic_start_time,
        "eventType": [
            "incident.response", "alert.response", "policy.updated", "user.updated"
        ],
        "limit": 1000
    }
    response = requests.get(f"{JC_URL}systemevents", headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch incident resolution logs: {response.status_code} - {response.text}")
        return []

def write_incident_resolution_logs_to_json(logs):
    directory = f"{BASE_DIR}/identity_and_access/jumpcloud/incident-resolution/{YEAR}/{MONTH}/"
    os.makedirs(directory, exist_ok=True)
    file_name = f"{directory}Jumpcloud_Incident_Resolution_Logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(logs, file, indent=4)
    print(f"Incident resolution logs written to {file_name}")

# Fetch security policy changes
def fetch_security_policy_changes():
    headers = get_headers()
    dynamic_start_time = calculate_dynamic_start_time()
    query_params = {
        "startTime": dynamic_start_time,
        "eventType": ["policy.updated", "policy.created", "policy.deleted"],
        "limit": 1000
    }
    response = requests.get(f"{JC_URL}systemevents", headers=headers, params=query_params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch security policy changes: {response.status_code} - {response.text}")
        return []

def write_security_policy_changes_to_json(events):
    directory = f"{BASE_DIR}/identity_and_access/jumpcloud/security-policies/{YEAR}/{MONTH}/"
    os.makedirs(directory, exist_ok=True)
    file_name = f"{directory}Jumpcloud_Security_Policy_Changes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(events, file, indent=4)
    print(f"Security policy change records written to {file_name}")

if __name__ == "__main__":
    print("Fetching and writing admin actions...")
    admin_actions = fetch_admin_actions()
    if admin_actions:
        write_admin_actions_to_json(admin_actions)

    print("Fetching and writing alerts and responses...")
    alerts = fetch_alerts_and_responses()
    if alerts:
        write_alerts_and_responses_to_json(alerts)

    print("Fetching and writing incident resolution logs...")
    resolution_logs = fetch_incident_resolution_logs()
    if resolution_logs:
        write_incident_resolution_logs_to_json(resolution_logs)

    print("Fetching and writing security policy changes...")
    policy_changes = fetch_security_policy_changes()
    if policy_changes:
        write_security_policy_changes_to_json(policy_changes)

    print("Data collection completed.")
