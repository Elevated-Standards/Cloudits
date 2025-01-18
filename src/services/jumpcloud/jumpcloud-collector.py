import requests
import csv
import datetime
import os
from utils.jc_utils import (
    JC_URL,
    get_base_dir,
    get_current_date_info,
    get_headers
)

# Fetch shared date information and base directory
date_info = get_current_date_info()
BASE_DIR = get_base_dir()
YEAR = date_info["year"]
MONTH = date_info["month"]
END_DATE = date_info["end_date"]


def ensure_directory_exists(path):
    if not os.path.exists(path):
        print(f"Creating directory: {path}")
        os.makedirs(path)


def save_csv(data, file_path):
    ensure_directory_exists(os.path.dirname(file_path))
    try:
        print(f"Saving data to CSV file: {file_path}")
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    except (OSError, IOError) as e:
        print(f"Error writing to file {file_path}: {e}")
        raise


def fetch_data(endpoint):
    headers = get_headers()
    url = endpoint
    results = []
    while url:
        print(f"Fetching data from URL: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            raise
        data = response.json()
        if 'results' not in data:
            print(f"Malformed response from {url}: 'results' key not found.")
            raise Exception(f"Malformed response from {url}: 'results' key not found.")
        results.extend(data.get('results', []))
        url = data.get('links', {}).get('next')
    print(f"Fetched {len(results)} items from endpoint {endpoint}")
    return results


def collect_users():
    print("Collecting users...")
    users = fetch_data(f"{JC_URL}/systemusers")
    file_path = os.path.join(BASE_DIR, f"identity_and_access/{YEAR}/{MONTH}/{END_DATE}-users.csv")
    save_csv(users, file_path)


def collect_groups():
    print("Collecting groups...")
    groups = fetch_data(f"{JC_URL}/usergroups")
    file_path = os.path.join(BASE_DIR, f"identity_and_access/{YEAR}/{MONTH}/{END_DATE}-groups.csv")
    save_csv(groups, file_path)


def collect_systems():
    print("Collecting systems...")
    systems = fetch_data(f"{JC_URL}/systems")
    file_path = os.path.join(BASE_DIR, f"identity_and_access/{YEAR}/{MONTH}/{END_DATE}-systems.csv")
    save_csv(systems, file_path)


def collect_group_members():
    print("Collecting group members...")
    groups = fetch_data(f"{JC_URL}/usergroups")
    group_members = []
    for group in groups:
        group_id = group['id']
        print(f"Fetching members for group ID: {group_id}")
        members = fetch_data(f"{JC_URL}/usergroups/{group_id}/members")
        group_members.extend(members)
    file_path = os.path.join(BASE_DIR, f"identity_and_access/{YEAR}/{MONTH}/{END_DATE}-group_members.csv")
    save_csv(group_members, file_path)


def collect_user_system_mapping():
    print("Collecting user-system mappings...")
    users = fetch_data(f"{JC_URL}/systemusers")
    user_system_mapping = []
    for user in users:
        user_id = user['id']
        print(f"Fetching systems for user ID: {user_id}")
        systems = fetch_data(f"{JC_URL}/systemusers/{user_id}/systems")
        user_system_mapping.extend(systems)
    file_path = os.path.join(BASE_DIR, f"identity_and_access/{YEAR}/{MONTH}/{END_DATE}-user_system_mapping.csv")
    save_csv(user_system_mapping, file_path)


if __name__ == "__main__":
    print("Starting data collection...")
    collect_users()
    collect_groups()
    collect_systems()
    collect_group_members()
    collect_user_system_mapping()
    print("Data collection completed.")
