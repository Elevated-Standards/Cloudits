import os
import subprocess
import json
from datetime import datetime, timezone, timedelta
from calendar import monthrange
from utils.utils import *
def get_aws_credentials(environment):
    regions = {
        'commercial': 'us-east-1',
        'federal': 'us-east-1',
    }

    if environment not in regions:
        print(f"Error: Invalid environment '{environment}' specified.")
        return None

    credentials = {
        'access_key': os.getenv('AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'region': regions[environment],
    }

    if not credentials['access_key'] or not credentials['secret_key']:
        print(f"Error: Missing AWS credentials for the '{environment}' environment.")
        return None

    return credentials

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(command)}\nError: {e}")
        return {}

def write_to_json(data, category, subcategory, system="aws"):
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
    