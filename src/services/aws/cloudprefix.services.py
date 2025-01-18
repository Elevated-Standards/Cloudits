####################################
# Auditor - A-lign ID's: 
#    1. P-13 - List of all infrastructure changes (e.g. changes to the configurations of the firewall/security groups, router, adding and removing servers, and other production network security controls)
# Auditor - 
# Auditor - 
####################################
import os
import subprocess
import datetime, timezone, timedelta
import json
import sys
from utils.aws_utils import *
from output_environments.cloudprefix import *


# Ensure the 'src' directory is in the Python module search path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Toggle environment enablement
ENABLE_ENVIRONMENTS = {
    'commercial': True,  # Enable/disable 'commercial' environment
    'federal': False     # Enable/disable 'federal' environment
}

# Date constants
CURRENT_DATETIME = datetime.datetime.now(datetime.timezone.utc)
YEAR = CURRENT_DATETIME.year
MONTH = CURRENT_DATETIME.strftime('%B')
DAY = CURRENT_DATETIME.day
START_DATE = (CURRENT_DATETIME - datetime.timedelta(days=31)).isoformat()
END_DATE = CURRENT_DATETIME.isoformat()

# Base directory for evidence storage
BASE_DIR = os.path.join(os.getcwd(), "evidence-artifacts")

# AWS environment configurations
ENVIRONMENTS = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            'alarms': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_alarms.json",
            'metrics': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_metrics.json",
            'dashboards': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_dashboards.json",
            'log_groups': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_log_groups.json",
            'tags': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_tags.json",
            'trails': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_trails.json",
            'event_data_stores': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_event_data_stores.json",
            'insights': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_insights.json",
            'config_changes': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-config_changes.json",
            'cloudtrail_events': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_events.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            'alarms': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_alarms.json",
            'metrics': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_metrics.json",
            'dashboards': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_dashboards.json",
            'log_groups': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_log_groups.json",
            'tags': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_tags.json",
            'trails': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_trails.json",
            'event_data_stores': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_event_data_stores.json",
            'insights': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_insights.json",
            'config_changes': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-config_changes.json",
            'cloudtrail_events': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_events.json"
        }
    }
}

# Helper function to save data to file
def save_data_to_file(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Fetch CloudTrail events
def fetch_cloudtrail_events(config, output_file):
    try:
        events = run_command([
            'aws', 'cloudtrail', 'lookup-events',
            '--lookup-attributes', 'AttributeKey=EventSource,AttributeValue=ec2.amazonaws.com',
            '--region', config['region'], '--output', 'json'
        ])
        save_data_to_file(events, output_file)
        print(f"CloudTrail events saved to {output_file}")
    except Exception as e:
        print(f"Error fetching CloudTrail events: {e}")

# Enable CloudTrail Insights
def enable_cloudtrail_insights(config, output_file):
    try:
        trails = run_command(['aws', 'cloudtrail', 'list-trails', '--region', config['region'], '--output', 'json'])
        insights_status = []
        for trail in trails.get('Trails', []):
            trail_name = trail['Name']
            try:
                run_command([
                    'aws', 'cloudtrail', 'put-insight-selectors',
                    '--trail-name', trail_name,
                    '--insight-selectors', '[{"InsightType":"ApiCallRateInsight"}]',
                    '--region', config['region']
                ])
                insights_status.append({trail_name: "Enabled"})
            except Exception as e:
                print(f"Failed to enable insights for trail {trail_name}: {e}")
        save_data_to_file(insights_status, output_file)
    except Exception as e:
        print(f"Error enabling CloudTrail Insights: {e}")

# Fetch AWS Config changes
def fetch_config_changes(config, output_file):
    try:
        resource_types = ['AWS::EC2::Instance', 'AWS::EC2::SecurityGroup', 'AWS::EC2::VPC']
        changes = []
        for resource_type in resource_types:
            resource_changes = run_command([
                'aws', 'configservice', 'get-resource-config-history',
                '--resource-type', resource_type, '--region', config['region'], '--output', 'json'
            ])
            changes.append({resource_type: resource_changes})
        save_data_to_file(changes, output_file)
        print(f"AWS Config changes saved to {output_file}")
    except Exception as e:
        print(f"Error fetching AWS Config changes: {e}")

# Main function
def main():
    for env_name, config in ENVIRONMENTS.items():
        if not ENABLE_ENVIRONMENTS.get(env_name, False):
            print(f"Skipping disabled environment: {env_name}")
            continue

        aws_creds = get_aws_credentials(env_name)
        if not aws_creds:
            print(f"Skipping {env_name}: Unable to retrieve credentials.")
            continue

        os.environ.update({
            'AWS_ACCESS_KEY_ID': aws_creds['access_key'],
            'AWS_SECRET_ACCESS_KEY': aws_creds['secret_key'],
            'AWS_DEFAULT_REGION': config['region']
        })

        print(f"Collecting evidence for environment: {env_name}")
        # Fetch CloudTrail and Config evidence
        fetch_cloudtrail_events(config, config['output_files']['cloudtrail_events'])
        enable_cloudtrail_insights(config, config['output_files']['insights'])
        fetch_config_changes(config, config['output_files']['config_changes'])
        print(f"Completed evidence collection for: {env_name}")

if __name__ == "__main__":
    main()
