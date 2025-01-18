import requests
import json
from datetime import datetime
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_managed_devices():
    """Fetch a list of all managed devices from JumpCloud."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    response = requests.get(f"{JC_URL}/v2/systems", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch managed devices: {response.status_code} - {response.text}")
        return []

def write_managed_devices_to_json(devices):
    """Write managed devices list to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/managed-devices/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_Managed_Devices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(devices, file, indent=4)
    print(f"Managed devices list written to {file_name}")

if __name__ == "__main__":
    devices = fetch_managed_devices()
    if devices:
        managed_devices = []
        for device in devices:
            managed_devices.append({
                "id": device.get("id"),
                "hostname": device.get("hostname"),
                "os": device.get("os"),
                "status": device.get("system_connection_status"),
                "last_activity": device.get("last_contact")
            })
        write_managed_devices_to_json(managed_devices)
    else:
        print("No managed devices found or failed to fetch devices.")
