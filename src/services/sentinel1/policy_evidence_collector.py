import requests
import json
import os
from datetime import datetime, timezone, timedelta
import schedule
import time

# Replace with your SentinelOne API token and URL
from utils.s1_utils import S1_API_TOKEN, S1_URL

# Directory to save JSON files
OUTPUT_DIR = "policy_evidence"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_policy_evidence():
    """
    Fetches evidence of applied policies, such as whitelisting, blacklisting, behavioral rules, and alert thresholds.
    """
    headers = {
        "Authorization": f"APIToken {S1_API_TOKEN}",
        "Content-Type": "application/json"
    }

    policies_endpoint = f"{S1_URL}/web/api/v2.1/policies"

    response = requests.get(policies_endpoint, headers=headers)

    if response.status_code == 200:
        policies = response.json().get('data', [])
        return policies
    else:
        print("Failed to fetch policy evidence, Status Code:", response.status_code)
        return []

def save_to_json(data):
    """
    Saves the policy evidence data to a JSON file.
    """
    file_name = datetime.now().strftime('%Y-%m-%d') + "-policy-evidence.json"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Policy evidence saved to {file_path}")

def fetch_and_save_policy_evidence():
    """
    Fetch and save evidence of applied policies.
    """
    print("Fetching policy evidence...")
    policies = fetch_policy_evidence()
    if policies:
        save_to_json(policies)
    else:
        print("No policy evidence found.")

# Schedule the job to run daily (can adjust to monthly if needed)
schedule.every().day.do(fetch_and_save_policy_evidence)

# Main loop to run the scheduled tasks
print("Policy evidence scheduler started...")
try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute
except KeyboardInterrupt:
    print("Scheduler stopped manually.")
