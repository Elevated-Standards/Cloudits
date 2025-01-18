import requests
import json
from datetime import datetime
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_devices():
    """Fetch all managed devices from JumpCloud."""
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

def filter_compliant_devices(devices):
    """Filter devices that meet security posture requirements."""
    compliant_devices = []
    for device in devices:
        if (device.get("disk_encryption_status") == "Enabled" and
            device.get("antivirus_installed") == "Yes" and
            device.get("screen_lock") == "Yes"):
            compliant_devices.append({
                "id": device.get("id"),
                "hostname": device.get("hostname"),
                "os": device.get("os"),
                "status": device.get("system_connection_status"),
                "last_activity": device.get("last_contact"),
                "disk_encryption": device.get("disk_encryption_status"),
                "antivirus_installed": device.get("antivirus_installed"),
                "screen_lock": device.get("screen_lock")
            })
    return compliant_devices

def write_compliant_devices_to_json(compliant_devices):
    """Write the list of compliant devices to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/compliant-devices/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_Compliant_Devices_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(compliant_devices, file, indent=4)
    print(f"Compliant devices list written to {file_name}")

if __name__ == "__main__":
    devices = fetch_devices()
    if devices:
        compliant_devices = filter_compliant_devices(devices)
        if compliant_devices:
            write_compliant_devices_to_json(compliant_devices)
        else:
            print("No devices meet the security posture requirements.")
    else:
        print("No devices found or failed to fetch devices.")
