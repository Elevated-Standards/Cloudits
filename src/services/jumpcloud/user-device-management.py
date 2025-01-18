import requests
from datetime import datetime, timezone, timedelta
from utils.jc_utils import (
    JC_URL,
    get_headers,
    get_base_dir,
    get_current_date_info,
    write_to_json,  # Imported from jc_utils.py    
)

# Fetch shared date information and base directory
date_info = get_current_date_info()
BASE_DIR = get_base_dir()
YEAR = date_info["year"]
MONTH = date_info["month"]
END_DATE = date_info["end_date"]

# Managed Devices Functions
def fetch_managed_devices():
    headers = get_headers()
    response = requests.get(f"{JC_URL}systems", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch managed devices: {response.status_code} - {response.text}")
        return []

# Compliant Devices Functions
def filter_compliant_devices(devices):
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

# Groups and Apps Functions
def fetch_groups():
    headers = get_headers()
    response = requests.get(f"{JC_URL}groups", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch groups: {response.status_code} - {response.text}")
        return []

def fetch_apps_for_group(group_id):
    headers = get_headers()
    response = requests.get(f"{JC_URL}groups/{group_id}/applications", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch applications for group {group_id}: {response.status_code} - {response.text}")
        return []

# Locked-Out Users Functions
def fetch_users():
    headers = get_headers()
    response = requests.get(f"{JC_URL}systemusers", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch users: {response.status_code} - {response.text}")
        return []

def filter_locked_out_users(users):
    locked_out_users = []
    today = datetime.now(timezone.utc)
    one_month_ago = today - timedelta(days=31)

    for user in users:
        lockout_date_str = user.get("lockedOutUntil")
        if lockout_date_str:
            lockout_date = datetime.strptime(lockout_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            if one_month_ago <= lockout_date <= today:
                locked_out_users.append({
                    "id": user.get("id"),
                    "email": user.get("email"),
                    "username": user.get("username"),
                    "locked_out_until": lockout_date_str
                })
    return locked_out_users

if __name__ == "__main__":
    print("Fetching and writing managed devices...")
    devices = fetch_managed_devices()
    if devices:
        write_to_json(devices, 'identity_and_access', 'managed-devices')

        print("Filtering and writing compliant devices...")
        compliant_devices = filter_compliant_devices(devices)
        if compliant_devices:
            write_to_json(compliant_devices, 'identity_and_access', 'compliant-devices')

    print("Fetching and writing groups and apps...")
    groups = fetch_groups()
    if groups:
        groups_with_apps = []
        for group in groups:
            group_id = group.get("id")
            group_name = group.get("name", "UnknownGroup")
            apps = fetch_apps_for_group(group_id)
            groups_with_apps.append({
                "group_id": group_id,
                "group_name": group_name,
                "applications": [
                    {"id": app.get("id"), "name": app.get("name")}
                    for app in apps
                ]
            })
        write_to_json(groups_with_apps, 'identity_and_access', 'groups-and-apps')

    print("Fetching and writing locked-out users...")
    users = fetch_users()
    if users:
        locked_out_users = filter_locked_out_users(users)
        if locked_out_users:
            write_to_json(locked_out_users, 'identity_and_access', 'locked-out-users')

    print("Data collection completed.")