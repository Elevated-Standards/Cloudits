import os
import subprocess
import json
from datetime import datetime, timezone, timedelta
from calendar import monthrange

def ensure_directories_exist(file_paths):
    for file_path in file_paths:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

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

def get_base_dir():
    """Return the base directory for evidence artifacts."""
    return os.path.join(os.getcwd(), "evidence-artifacts")