import requests
from datetime import datetime, timezone
from utils.jc_utils import (
    JC_URL,
    get_base_dir,
    get_current_date_info,
    get_headers,
    write_to_json  # Import the generic write function
)

date_info = get_current_date_info()
BASE_DIR = get_base_dir()
YEAR = date_info["year"]
MONTH = date_info["month"]
END_DATE = date_info["end_date"]
def fetch_device_compliance():
    """Fetch compliance status of managed devices."""
    headers = get_headers()
    response = requests.get(f"{JC_URL}systems", headers=headers)
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

if __name__ == "__main__":
    devices = fetch_device_compliance()
    if devices:
        compliance_data = process_compliance_data(devices)
        # Use the generic `write_to_json` function
        write_to_json(compliance_data, 'identity_and_access', 'compliance-status')
    else:
        print("No managed devices found or failed to fetch devices.")