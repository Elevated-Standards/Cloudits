import requests
import json
import os
from datetime import datetime
import schedule
import time

# Replace with your SentinelOne API token and URL
from utils.s1_utils import S1_API_TOKEN, S1_URL

# Directory to save JSON files
OUTPUT_DIR = "quarantine_evidence"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_quarantine_events():
    """
    Fetches quarantined files or applications from SentinelOne.
    """
    headers = {
        "Authorization": f"APIToken {S1_API_TOKEN}",
        "Content-Type": "application/json"
    }

    quarantine_endpoint = f"{S1_URL}/web/api/v2.1/threats"
    params = {
        "quarantined": True  # Filter for quarantined threats
    }

    response = requests.get(quarantine_endpoint, headers=headers, params=params)

    if response.status_code == 200:
        threats = response.json().get('data', [])
        return threats
    else:
        print("Failed to fetch quarantine events, Status Code:", response.status_code)
        return []

def save_to_json(data):
    """
    Saves the quarantined evidence data to a JSON file.
    """
    file_name = datetime.now().strftime('%Y-%m-%d') + "-quarantine-evidence.json"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Quarantine evidence saved to {file_path}")

def fetch_and_save_quarantine_evidence():
    """
    Fetch and save quarantined files or applications.
    """
    print("Fetching quarantined threats...")
    quarantined_threats = fetch_quarantine_events()
    if quarantined_threats:
        save_to_json(quarantined_threats)
    else:
        print("No quarantined threats found.")

# Schedule the job to run daily (can adjust to monthly if needed)
schedule.every().day.do(fetch_and_save_quarantine_evidence)

# Main loop to run the scheduled tasks
print("Quarantine evidence scheduler started...")
try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute
except KeyboardInterrupt:
    print("Scheduler stopped manually.")
