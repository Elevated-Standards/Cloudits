import requests
import json
import os
from datetime import datetime
import schedule
import time

# Replace with your SentinelOne API token and URL
from utils.s1_utils import S1_API_TOKEN, S1_URL

# Directory to save JSON files
OUTPUT_DIR = "device_list"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_device_list():
    """
    Fetches a list of all devices from SentinelOne.
    """
    headers = {
        "Authorization": f"APIToken {S1_API_TOKEN}",
        "Content-Type": "application/json"
    }

    devices_endpoint = f"{S1_URL}/web/api/v2.1/agents"

    response = requests.get(devices_endpoint, headers=headers)

    if response.status_code == 200:
        devices = response.json().get('data', [])
        return devices
    else:
        print("Failed to fetch device list, Status Code:", response.status_code)
        return []

def save_to_json(data):
    """
    Saves the device list data to a JSON file.
    """
    file_name = datetime.now().strftime('%Y-%m-%d') + "-device-list.json"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Device list saved to {file_path}")

def fetch_and_save_device_list():
    """
    Fetch and save a list of all devices.
    """
    print("Fetching device list...")
    devices = fetch_device_list()
    if devices:
        save_to_json(devices)
    else:
        print("No devices found.")

# Schedule the job to run daily (can adjust to monthly if needed)
schedule.every().day.do(fetch_and_save_device_list)

# Main loop to run the scheduled tasks
print("Device list scheduler started...")
try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute
except KeyboardInterrupt:
    print("Scheduler stopped manually.")
