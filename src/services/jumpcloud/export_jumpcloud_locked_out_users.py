import requests
import json
from datetime import datetime, timedelta
import os
from utils.jc_utils import JC_API_KEY, JC_URL

def fetch_users():
    """Fetch all users from JumpCloud."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }
    response = requests.get(f"{JC_URL}/v2/systemusers", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch users: {response.status_code} - {response.text}")
        return []

def filter_locked_out_users(users):
    """Filter users who have been locked out in the past month."""
    locked_out_users = []
    today = datetime.now()
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

def write_locked_out_users_to_json(locked_out_users):
    """Write the locked-out user data to a JSON file."""
    current_year = datetime.now().year
    directory = f"/evidence-artifacts/{current_year}/commercial/jumpcloud/locked-out-users/"
    os.makedirs(directory, exist_ok=True)  # Ensure directory exists
    file_name = f"{directory}Jumpcloud_Locked_Out_Users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, 'w') as file:
        json.dump(locked_out_users, file, indent=4)
    print(f"Locked-out user list written to {file_name}")

if __name__ == "__main__":
    users = fetch_users()
    if users:
        locked_out_users = filter_locked_out_users(users)
        if locked_out_users:
            write_locked_out_users_to_json(locked_out_users)
        else:
            print("No users were locked out in the past month.")
    else:
        print("No users found or failed to fetch users.")
