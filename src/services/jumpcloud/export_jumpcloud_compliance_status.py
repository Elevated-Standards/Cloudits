import requests
import json
from datetime import datetime
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_device_compliance():
    """Fetch compliance status of managed devices."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    response = requests.get(f"{JC_URL}/v2/systems", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch devices: {response.status_code} - {response.text}")
        return []

def process_compliance_data(devices):
    """Process compliance data for devices."""
    compliance_data = []
    for device in devices:
        compliance_data.append({
            "id": device.get("id"),
            "hostname": device.get("hostname"),
            "os": device.get("os"),
            "disk_encryption": device.get("disk_encryption_status", "Unknown"),
            "antivirus_installed": device.get("antivirus_installed", "Unknown"),
            "screen_lock_enabled": device.get("screen_lock", "Unknown"),
            "status": device.get("system_connection_status"),
            "last_activity": device.get("last_contact")
        })
    return compliance_data

def write_compliance_data_to_json(compliance_data):
    """Write compliance data to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/compliance-status/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_Compliance_Status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(compliance_data, file, indent=4)
    print(f"Compliance data written to {file_name}")

if __name__ == "__main__":
    devices = fetch_device_compliance()
    if devices:
        compliance_data = process_compliance_data(devices)
        write_compliance_data_to_json(compliance_data)
    else:
        print("No managed devices found or failed to fetch devices.")
