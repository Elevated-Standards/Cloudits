import os
from datetime import datetime, timezone, timedelta
from calendar import monthrange
import json

# Constants
JC_API_KEY = os.getenv("JUMPCLOUD_API_KEY")
JC_URL = "https://console.jumpcloud.com/api/v2/"

def calculate_dynamic_start_time():
    """Calculate the dynamic start time, accounting for month-end and 30-day spans."""
    now = datetime.now(timezone.utc)
    last_month_days = monthrange(now.year, now.month - 1 if now.month > 1 else 12)[1]
    if now.day > last_month_days:
        return (now - timedelta(days=last_month_days)).isoformat() + "Z"
    return (now - timedelta(days=30)).isoformat() + "Z"

def get_headers():
    """Return headers for JumpCloud API requests."""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": JC_API_KEY
    }

def get_base_dir():
    """Return the base directory for evidence artifacts."""
    return os.path.join(os.getcwd(), "evidence-artifacts")

def get_current_date_info():
    """Return current date-related information."""
    now = datetime.now(timezone.utc)
    return {
        "year": now.year,
        "month": now.strftime('%B'),
        "day": now.day,
        "start_date": (now - timedelta(days=now.day)).strftime("%H:%M:%SZT%Y-%m-%d"),
        "end_date": now.strftime("%H:%M:%SZT%Y-%m-%d")
    }


def write_to_json(data, category, subcategory, system="Jumpcloud"):
    """
    Write data to a JSON file with standardized naming and directory structure.

    Args:
        data: Data to write
        category: Main category 
        subcategory: Subcategory folder name 
        system: System Name 
    """
    directory = f"{get_base_dir()}/{category}/{system}/{subcategory}/{datetime.now().year}/{datetime.now().strftime('%B')}/"
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f"{directory}{timestamp}_{subcategory}.json"
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data written to {file_name}")
