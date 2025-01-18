import requests
import json
import os
from datetime import datetime, timezone, timedelta
import schedule
import time

# Replace with your SentinelOne API token and URL
from utils.s1_utils import S1_API_TOKEN, S1_URL

# Directory to save JSON files
OUTPUT_DIR = "incident_records"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_all_incidents():
    """
    Fetches all incidents from SentinelOne, including detection timestamps, severity levels, and affected endpoints.
    """
    headers = {
        "Authorization": f"APIToken {S1_API_TOKEN}",
        "Content-Type": "application/json"
    }

    incidents_endpoint = f"{S1_URL}/web/api/v2.1/incidents"

    response = requests.get(incidents_endpoint, headers=headers)

    if response.status_code == 200:
        incidents = response.json().get('data', [])
        return incidents
    else:
        print("Failed to fetch incidents, Status Code:", response.status_code)
        return []

def save_to_json(data):
    """
    Saves the incident data to a JSON file.
    """
    file_name = datetime.now().strftime('%Y-%m-%d') + "-incident-records.json"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Incident records saved to {file_path}")

def fetch_and_save_incident_records():
    """
    Fetch and save all incidents including timestamps, severity levels, and affected endpoints.
    """
    print("Fetching incident records...")
    incidents = fetch_all_incidents()
    if incidents:
        save_to_json(incidents)
    else:
        print("No incidents found.")

# Schedule the job to run daily (can adjust to monthly if needed)
schedule.every().day.do(fetch_and_save_incident_records)

# Main loop to run the scheduled tasks
print("Incident record scheduler started...")
try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute
except KeyboardInterrupt:
    print("Scheduler stopped manually.")
