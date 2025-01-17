import os
import subprocess
import json

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

def ensure_directories_exist(file_paths):
    for file_path in file_paths:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)