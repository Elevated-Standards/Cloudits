import requests
import json
import os
from datetime import datetime, timezone, timedelta
import schedule
import time

# Replace with your SentinelOne API token and URL
from utils.s1_utils import S1_API_TOKEN, S1_URL

# Directory to save JSON files
OUTPUT_DIR = "integration_evidence"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_integration_evidence():
    """
    Fetches evidence of SentinelOne integrations with patch management systems or tools.
    """
    headers = {
        "Authorization": f"APIToken {S1_API_TOKEN}",
        "Content-Type": "application/json"
    }

    integrations_endpoint = f"{S1_URL}/web/api/v2.1/integrations"

    response = requests.get(integrations_endpoint, headers=headers)

    if response.status_code == 200:
        integrations = response.json().get('data', [])
        return integrations
    else:
        print("Failed to fetch integration evidence, Status Code:", response.status_code)
        return []

def save_to_json(data):
    """
    Saves the integration evidence data to a JSON file.
    """
    file_name = datetime.now().strftime('%Y-%m-%d') + "-integration-evidence.json"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Integration evidence saved to {file_path}")

def fetch_and_save_integration_evidence():
    """
    Fetch and save evidence of integrations with patch management systems.
    """
    print("Fetching integration evidence...")
    integrations = fetch_integration_evidence()
    if integrations:
        save_to_json(integrations)
    else:
        print("No integration evidence found.")

# Schedule the job to run daily (can adjust to monthly if needed)
schedule.every().day.do(fetch_and_save_integration_evidence)

# Main loop to run the scheduled tasks
print("Integration evidence scheduler started...")
try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute
except KeyboardInterrupt:
    print("Scheduler stopped manually.")
