# Purpose: 
###############################################################
import os
import subprocess
import datetime, timezone, timedelta
import json
import sys
from utils.aws_utils import *
from output_environments.certificatesandkey import *
from utils.project import *
from concurrent.futures import *

# Ensure the 'src' directory is in the Python module search path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Define toggles to enable or disable environments
enable_environments = {
    'commercial': True,  # Set to False to disable 'commercial'
    'federal': False      # Set to False to disable 'federal'
}

# Define current year and month for directory paths
YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
DAY = datetime.datetime.now().day
START_DATE = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=31)).isoformat()  # 31 days ago
END_DATE = datetime.datetime.now(datetime.timezone.utc).isoformat() 


# Base directory for evidence artifacts
BASE_DIR = os.path.join(os.getcwd(), "evidence-artifacts")

# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            '<Function1>': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}.{DAY}-<Function1>.json",
            '<Function2>': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}.{DAY}-<Function2>.json",
            '<Function3>': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}.{DAY}-<Function3>.json",
            '<Function4>': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}.{DAY}-<Function4>.json",
            '<Function5>': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}.{DAY}-<Function5>.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            '<Function1>': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}.{DAY}-<Function1>.json",
            '<Function2>': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}.{DAY}-<Function2>.json",
            '<Function3>': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}.{DAY}-<Function3>.json",
            '<Function4>': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}.{DAY}-<Function4>.json",
            '<Function5>': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}.{DAY}-<Function5>.json"
        }
    }
}

# Helper function to run AWS CLI commands
def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(command)}\nError: {e}")
        return {}

# Placeholder functions for each evidence collection task with item iteration
def fetch_function1(config, output_file):
    data = run_command(['aws', '<service>', '<list_command>', '--region', config['region'], '--output', 'json'])
    items = []
    for item in data.get('<ItemsKey>', []):
        item_details = run_command(['aws', '<service>', '<get_command>', '--item-id', item['<IDKey>'], '--region', config['region'], '--output', 'json'])
        items.append(item_details)
    save_to_file(items, output_file)

def fetch_function2(config, output_file):
    data = run_command(['aws', '<service>', '<list_command>', '--region', config['region'], '--output', 'json'])
    items = []
    for item in data.get('<ItemsKey>', []):
        item_details = run_command(['aws', '<service>', '<get_command>', '--item-id', item['<IDKey>'], '--region', config['region'], '--output', 'json'])
        items.append(item_details)
    save_to_file(items, output_file)

def fetch_function3(config, output_file):
    data = run_command(['aws', '<service>', '<list_command>', '--region', config['region'], '--output', 'json'])
    items = []
    for item in data.get('<ItemsKey>', []):
        item_details = run_command(['aws', '<service>', '<get_command>', '--item-id', item['<IDKey>'], '--region', config['region'], '--output', 'json'])
        items.append(item_details)
    save_to_file(items, output_file)

def fetch_function4(config, output_file):
    data = run_command(['aws', '<service>', '<list_command>', '--region', config['region'], '--output', 'json'])
    items = []
    for item in data.get('<ItemsKey>', []):
        item_details = run_command(['aws', '<service>', '<get_command>', '--item-id', item['<IDKey>'], '--region', config['region'], '--output', 'json'])
        items.append(item_details)
    save_to_file(items, output_file)

def fetch_function5(config, output_file):
    data = run_command(['aws', '<service>', '<list_command>', '--region', config['region'], '--output', 'json'])
    items = []
    for item in data.get('<ItemsKey>', []):
        item_details = run_command(['aws', '<service>', '<get_command>', '--item-id', item['<IDKey>'], '--region', config['region'], '--output', 'json'])
        items.append(item_details)
    save_to_file(items, output_file)

# Utility function to save data to JSON file
def save_to_file(data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

# Main function with multithreading
def main():
    for env_name, config in environments.items():
        # Fetch AWS credentials for the current environment
        aws_creds = get_aws_credentials(env_name)
        if not aws_creds:
            print(f"Skipping environment '{env_name}' due to credential issues.")
            continue

        # Set AWS environment variables for subprocess commands
        os.environ['AWS_ACCESS_KEY_ID'] = aws_creds['access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_creds['secret_key']
        os.environ['AWS_DEFAULT_REGION'] = aws_creds['region']

        # Define tasks for evidence collection
        tasks = [
            (fetch_function1, config, config['output_files']['function1']),
            (fetch_function2, config, config['output_files']['function2']),
            (fetch_function3, config, config['output_files']['function3']),
            (fetch_function4, config, config['output_files']['function4']),
            (fetch_function5, config, config['output_files']['function5']),
        ]

        print(f"Starting evidence collection for environment '{env_name}'...")

        # Execute tasks concurrently
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(task[0], *task[1:]): task[0].__name__ for task in tasks}

            for future in as_completed(futures):
                task_name = futures[future]
                try:
                    future.result()
                    print(f"Task '{task_name}' completed successfully.")
                except Exception as e:
                    print(f"Task '{task_name}' failed with error: {e}")

        print(f"Evidence collection completed for environment '{env_name}'.")

if __name__ == "__main__":
    main()


###############################################################
# Framework: 
# - SOC 2: CC#.#, CC#.#
# - ISO 27001: A.#.#
###############################################################
# Auditor 1 - <Placeholder> ID's: 
# - R-### - 
# - 
###############################################################
# Auditor 2 - <Placeholder> ID's: 
# - 
###############################################################