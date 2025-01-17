import os
import subprocess
import datetime
import json
import sys
from credentials.aws import get_aws_credentials

# Ensure the 'src' directory is in the Python module search path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Define toggles to enable or disable environments
enable_environments = {
    'commercial': True,  # Set to False to disable 'commercial'
    'federal': False      # Set to False to disable 'federal'
}

YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
DAY = datetime.datetime.now().day
START_DATE = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=31)).isoformat()
END_DATE = datetime.datetime.now(datetime.timezone.utc).isoformat()

# Base directory for evidence artifacts
BASE_DIR = os.path.join(os.getcwd(), "evidence-artifacts")

# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            # Change '{BASE_DIR}' to '{BASE_DIR}' (relative path)
            'alarms': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_alarms.json",
            'metrics': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_metrics.json",
            'dashboards': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_dashboards.json",
            'log_groups': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_log_groups.json",
            'tags': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_tags.json",
            'trails': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_trails.json",
            'event_data_stores': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_event_data_stores.json",
            'insights': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_insights.json",
            'tags': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_tags.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            # Use relative paths
            'alarms': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{END_DATE}-cloudwatch_alarms.json",
            'metrics': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{END_DATE}-cloudwatch_metrics.json",
            'dashboards': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{END_DATE}-cloudwatch_dashboards.json",
            'log_groups': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{END_DATE}-cloudwatch_log_groups.json",
            'tags': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{END_DATE}-cloudwatch_tags.json",
            'trails': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{END_DATE}-cloudtrail_trails.json",
            'event_data_stores': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{END_DATE}-cloudtrail_event_data_stores.json",
            'insights': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{END_DATE}-cloudtrail_insights.json",
            'tags': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{END_DATE}-cloudtrail_tags.json"
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

# CloudWatch Evidence Collection Functions
def fetch_alarms(config, output_file):
    alarms_data = run_command(['aws', 'cloudwatch', 'describe-alarms', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(alarms_data, f, indent=4)

def fetch_metrics(config, output_file):
    metrics_data = run_command(['aws', 'cloudwatch', 'list-metrics', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(metrics_data, f, indent=4)

def fetch_dashboards(config, output_file):
    dashboards_data = run_command(['aws', 'cloudwatch', 'list-dashboards', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(dashboards_data, f, indent=4)

def fetch_log_groups(config, output_file):
    log_groups_data = run_command(['aws', 'logs', 'describe-log-groups', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(log_groups_data, f, indent=4)

def fetch_cloudwatch_tags(config, output_file):
    log_groups_data = run_command(['aws', 'logs', 'describe-log-groups', '--region', config['region'], '--output', 'json'])
    tags_data = []
    for log_group in log_groups_data.get('logGroups', []):
        log_group_name = log_group['logGroupName']
        tags = run_command(['aws', 'logs', 'list-tags-log-group', '--log-group-name', log_group_name, '--output', 'json'])
        tags_data.append({'LogGroupName': log_group_name, 'Tags': tags.get('tags', {})})
    with open(output_file, 'w') as f:
        json.dump(tags_data, f, indent=4)

# CloudTrail Evidence Collection Functions
def fetch_trails(config, output_file):
    trails_data = run_command(['aws', 'cloudtrail', 'list-trails', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(trails_data, f, indent=4)

def fetch_event_data_stores(config, output_file):
    event_data_stores_data = run_command(['aws', 'cloudtrail', 'list-event-data-stores', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(event_data_stores_data, f, indent=4)


def fetch_insights_selectors(config, output_file):
    """
    Fetch insight selectors for all trails in the specified region and save the data to a file.
    """
    try:
        # List all trails in the specified region
        trails_data = run_command(['aws', 'cloudtrail', 'list-trails', '--region', config['region'], '--output', 'json'])
        trails = trails_data.get('Trails', [])
        
        if not trails:
            print(f"No trails found in region {config['region']}.")
            return
        
        insights_data = []

        for trail in trails:
            trail_name = trail.get('Name')
            if not trail_name:
                print(f"Skipping trail with no name: {trail}")
                continue

            print(f"Processing trail: {trail_name}")

            try:
                # Fetch insight selectors for the current trail
                insights_selectors = run_command(['aws', 'cloudtrail', 'get-insight-selectors', '--trail-name', trail_name, '--output', 'json'])
                insights_data.append({
                    'TrailName': trail_name,
                    'InsightSelectors': insights_selectors.get('InsightSelectors', [])
                })
            except Exception as e:
                print(f"Failed to fetch insight selectors for trail '{trail_name}': {e}")

        # Save the insights data to a file
        with open(output_file, 'w') as f:
            json.dump(insights_data, f, indent=4)
        print(f"Insight selectors data saved to {output_file}.")

    except Exception as e:
        print(f"Error occurred while fetching insights: {e}")




def fetch_cloudtrail_tags(config, output_file):
    trails_data = run_command(['aws', 'cloudtrail', 'list-trails', '--region', config['region'], '--output', 'json'])
    tags_data = []
    for trail in trails_data['Trails']:
        trail_arn = trail['TrailARN']
        trail_tags = run_command(['aws', 'cloudtrail', 'list-tags', '--resource-id-list', trail_arn, '--output', 'json'])
        tags_data.append({
            'TrailARN': trail_arn,
            'Tags': trail_tags.get('ResourceTagList', [])
        })
    with open(output_file, 'w') as f:
        json.dump(tags_data, f, indent=4)

# Main function to execute each evidence collection task for enabled environments
def main():
    for env_name, config in environments.items():
        # Check if the environment is enabled
        if not enable_environments.get(env_name, False):
            print(f"Skipping environment '{env_name}' as it is disabled.")
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

        # Ensure directories exist for output files
        for file_path in config['output_files'].values():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Collect evidence for AWS CloudWatch configurations
        fetch_alarms(config, config['output_files']['alarms'])
        fetch_metrics(config, config['output_files']['metrics'])
        fetch_dashboards(config, config['output_files']['dashboards'])
        fetch_log_groups(config, config['output_files']['log_groups'])
        fetch_cloudwatch_tags(config, config['output_files']['tags'])

        # Collect evidence for AWS CloudTrail configurations
        fetch_trails(config, config['output_files']['trails'])
        fetch_event_data_stores(config, config['output_files']['event_data_stores'])
        fetch_insights_selectors(config, config['output_files']['insights'])
        fetch_cloudtrail_tags(config, config['output_files']['tags'])

        
        print(f"Completed evidence collection for environment '{env_name}'.")

    print("AWS CloudWatch and CloudTrail configuration evidence collection completed.")

# Execute main function
if __name__ == "__main__":
    main()
