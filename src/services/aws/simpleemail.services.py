import os
import subprocess
import datetime, timezone, timedelta
import json
import sys
from utils.aws_utils import get_aws_credentials, run_command, ensure_directories_exist

# Ensure the 'src' directory is in the Python module search path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Define toggles to enable or disable environments
enable_environments = {
    'commercial': True,  # Set to False to disable 'commercial'
    'federal': False      # Set to False to disable 'federal'
}

YEAR = datetime.now().year  # Current year
MONTH = datetime.now().strftime('%B')  # Current month name
DAY = datetime.now().day  # Current day of the month
START_DATE = (datetime.now(timezone.utc) - timedelta(days=DAY)).isoformat()  # Start date: first day of the month
END_DATE = datetime.now(timezone.utc).strftime("%H:%M:%SZT%Y-%m-%d")  # End date: current date in UTC

# Base directory for evidence artifacts
BASE_DIR = os.path.join(os.getcwd(), "evidence-artifacts")

# Replace with actual configuration set name and resource ARN
config_set_name = 'YOUR_CONFIG_SET_NAME'
resource_arn = 'YOUR_RESOURCE_ARN'


# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            'identities': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-sesv2_email_identities.json",
            'configuration_sets': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-sesv2_configuration_sets.json",
            'dedicated_ips': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-sesv2_dedicated_ips.json",
            'event_destinations': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-sesv2_event_destinations.json",
            'tags': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-sesv2_tags.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            'identities': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-sesv2_email_identities.json",
            'configuration_sets': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-sesv2_configuration_sets.json",
            'dedicated_ips': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-sesv2_dedicated_ips.json",
            'event_destinations': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-sesv2_event_destinations.json",
            'tags': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-sesv2_tags.json"
        }
    }
}

# Helper function to run AWS CLI commands
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return json.loads(result.stdout)

# Fetch all SES email identities
def fetch_email_identities(config, output_file):
    identities_data = run_command(['aws', 'sesv2', 'list-email-identities', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(identities_data, f, indent=4)

# Fetch configuration sets
def fetch_configuration_sets(config, output_file):
    config_sets_data = run_command(['aws', 'sesv2', 'list-configuration-sets', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(config_sets_data, f, indent=4)

# Fetch dedicated IPs
def fetch_dedicated_ips(config, output_file):
    dedicated_ips_data = run_command(['aws', 'sesv2', 'list-dedicated-ips', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(dedicated_ips_data, f, indent=4)

# Fetch event destinations for a configuration set
def fetch_event_destinations(config, output_file, config_set_name):
    event_destinations_data = run_command([
        'aws', 'sesv2', 'list-event-destinations',
        '--configuration-set-name', config_set_name,
        '--region', config['region'],
        '--output', 'json'
    ])
    with open(output_file, 'w') as f:
        json.dump(event_destinations_data, f, indent=4)

# Fetch tags for a specific SES resource
def fetch_sesv2_tags(config, output_file, resource_arn):
    tags_data = run_command(['aws', 'sesv2', 'list-tags-for-resource', '--resource-arn', resource_arn, '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(tags_data, f, indent=4)

# Main function to execute each evidence collection task
def main():
    for env_name, config in environments.items():
        # Check if the environment is enabled
        if not enable_environments.get(env_name, False):
            print(f"Environment '{env_name}' is disabled. Skipping...")
            continue

        # Fetch AWS credentials for the current environment
        aws_creds = get_aws_credentials(env_name)
        if not aws_creds:
            print(f"Skipping environment '{env_name}' due to credential issues.")
            continue
        
        # Set AWS environment variables for subprocess commands
        os.environ['AWS_ACCESS_KEY_ID'] = aws_creds['access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_creds['secret_key']
        os.environ['AWS_DEFAULT_REGION'] = aws_creds['region']

        ensure_directories_exist(config['output_files'].values())

        # Collect evidence for AWS SES v2 configurations
        fetch_email_identities(config, config['output_files']['identities'])
        fetch_configuration_sets(config, config['output_files']['configuration_sets'])
        fetch_dedicated_ips(config, config['output_files']['dedicated_ips'])
        fetch_event_destinations(config, config['output_files']['event_destinations'], config_set_name)
        fetch_sesv2_tags(config, config['output_files']['tags'], resource_arn)

    print("AWS SES v2 configuration evidence collection completed.")

# Execute main function
if __name__ == "__main__":
    main()
