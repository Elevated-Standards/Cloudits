# Purpose: Collect evidence for monitoring privileged functions and auditing logs
###############################################################
# Framework: 
# - SOC 2: CC6.1, CC7.2, CC6.8, CC6.9
# - ISO 27001: A.8.15
###############################################################
# CloudTrail Monitoring: 
# - Privileged API Execution
# - Audit Logs for Sensitive Functions
###############################################################
# Operational Validation: 
# - Multi-environment coverage
###############################################################
import os
import subprocess
import datetime
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.aws_utils import get_aws_credentials, ensure_directories_exist

# Ensure the 'src' directory is in the Python module search path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Define toggles to enable or disable environments
enable_environments = {
    'commercial': True,  # Set to False to disable 'commercial'
    'federal': False      # Set to False to disable 'federal'
}

# Define current year, month, and day for directory paths
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
            'cloudtrail_events': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{DAY}-cloudtrail_events.json",
            'privileged_apis': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{DAY}-privileged_apis.json",
            'user_activity': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{DAY}-user_activity.json",
            'cloudtrail_status': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{DAY}-cloudtrail_status.json",
            'log_group_activity': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{DAY}-log_group_activity.json",
            'trail_event_selectors': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{DAY}-trail_event_selectors.json",
            'ssm_logs': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{DAY}-ssm_logs.json",
            'ec2_instances': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{DAY}-ec2_instances.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            'cloudtrail_events': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{DAY}-cloudtrail_events.json",
            'privileged_apis': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{DAY}-privileged_apis.json",
            'user_activity': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{DAY}-user_activity.json",
            'cloudtrail_status': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{DAY}-cloudtrail_status.json",
            'log_group_activity': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{DAY}-log_group_activity.json",
            'trail_event_selectors': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{DAY}-trail_event_selectors.json",
            'ssm_logs': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{DAY}-ssm_logs.json",
            'ec2_instances': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{DAY}-ec2_instances.json"
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

# Function 1: Fetch CloudTrail event logs
def fetch_cloudtrail_events(config, output_file):
    #######################################
    # Framework(s): SOC 2 CC6.8, ISO 27001 A.8.15
    #######################################
    events = run_command([
        'aws', 'cloudtrail', 'lookup-events',
        '--region', config['region'],
        '--start-time', START_DATE,
        '--end-time', END_DATE,
        '--output', 'json'
    ])
    save_to_file(events, output_file)

# Function 2: Fetch details of privileged API executions
def fetch_privileged_apis(config, output_file):
    #######################################
    # Framework(s): SOC 2 CC6.8, CC6.9
    #######################################
    privileged_events = []
    for api_name in ['CreateUser', 'DeleteUser', 'AttachRolePolicy']:
        events = run_command([
            'aws', 'cloudtrail', 'lookup-events',
            '--lookup-attributes', f"AttributeKey=EventName,AttributeValue={api_name}",
            '--region', config['region'],
            '--start-time', START_DATE,
            '--end-time', END_DATE,
            '--output', 'json'
        ])
        privileged_events.extend(events.get('Events', []))
    save_to_file(privileged_events, output_file)

# Function 3: Fetch user activity logs (dynamic username)
def fetch_user_activity(config, output_file, username):
    #######################################
    # Framework(s): SOC 2 CC6.8, ISO 27001 A.8.15
    #######################################
    users_activity = run_command([
        'aws', 'cloudtrail', 'lookup-events',
        '--lookup-attributes', f"AttributeKey=Username,AttributeValue={username}",
        '--region', config['region'],
        '--start-time', START_DATE,
        '--end-time', END_DATE,
        '--output', 'json'
    ])
    save_to_file(users_activity, output_file)

# Function 4: Fetch CloudTrail status
def fetch_cloudtrail_status(config, output_file):
    #######################################
    # Framework(s): ISO 27001 A.8.15
    #######################################
    trails = run_command(['aws', 'cloudtrail', 'describe-trails', '--region', config['region'], '--output', 'json'])
    statuses = []
    for trail in trails.get('trailList', []):
        status = run_command(['aws', 'cloudtrail', 'get-trail-status', '--name', trail['Name'], '--output', 'json'])
        statuses.append(status)
    save_to_file(statuses, output_file)

# Function 5: Fetch CloudWatch log group activity
def fetch_log_group_activity(config, output_file):
    #######################################
    # Framework(s): SOC 2 CC6.8
    #######################################
    log_groups = run_command(['aws', 'logs', 'describe-log-groups', '--region', config['region'], '--output', 'json'])
    activities = []
    for group in log_groups.get('logGroups', []):
        log_events = run_command([
            'aws', 'logs', 'get-log-events',
            '--log-group-name', group['logGroupName'],
            '--start-time', str(int(datetime.datetime.now().timestamp() - 31 * 86400) * 1000),
            '--end-time', str(int(datetime.datetime.now().timestamp()) * 1000),
            '--region', config['region'],
            '--output', 'json'
        ])
        activities.append(log_events)
    save_to_file(activities, output_file)

# Function 6: Fetch CloudTrail event selectors
def fetch_trail_event_selectors(config, output_file):
    #######################################
    # Framework(s): SOC 2 CC6.9, ISO 27001 A.8.15
    #######################################
    trails = run_command(['aws', 'cloudtrail', 'describe-trails', '--region', config['region'], '--output', 'json'])
    event_selectors = []
    for trail in trails.get('trailList', []):
        selectors = run_command(['aws', 'cloudtrail', 'get-event-selectors', '--trail-name', trail['Name'], '--output', 'json'])
        event_selectors.append(selectors)
    save_to_file(event_selectors, output_file)

# Function 7: Fetch logs from SSM-managed servers
def fetch_ssm_logs(config, output_file):
    #######################################
    # Framework(s): SOC 2 CC6.8, ISO 27001 A.8.15
    #######################################
    instances = run_command([
        'aws', 'ssm', 'describe-instance-information',
        '--filters', "Key=tag:Environment,Values=Production",
        '--region', config['region'],
        '--output', 'json'
    ])
    logs = []
    for instance in instances.get('InstanceInformationList', []):
        response = run_command([
            'aws', 'ssm', 'send-command',
            '--targets', f"Key=InstanceIds,Values={instance['InstanceId']}",
            '--document-name', 'AWS-RunShellScript',
            '--parameters', '{"commands":["cat /var/log/audit/audit.log | tail -n 100"]}',
            '--region', config['region'],
            '--output', 'json'
        ])
        logs.append(response)
    save_to_file(logs, output_file)

# Function 8: Fetch EC2 instance details
def fetch_ec2_instances(config, output_file):
    #######################################
    # Framework(s): ISO 27001 A.8.15
    #######################################
    instances = run_command([
        'aws', 'ec2', 'describe-instances',
        '--filters', "Name=tag:Environment,Values=Production",
        '--region', config['region'],
        '--output', 'json'
    ])
    save_to_file(instances, output_file)

# Utility function to save data to JSON file
def save_to_file(data, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

# Main function to execute tasks for each environment
def main():
    username = input("Enter the username to filter activity logs: ")  # Dynamically input username
    for env_name, config in environments.items():
        if not enable_environments.get(env_name, False):
            print(f"Environment '{env_name}' is disabled. Skipping...")
            continue

        aws_creds = get_aws_credentials(env_name)
        if not aws_creds:
            print(f"Skipping environment '{env_name}' due to credential issues.")
            continue

        os.environ['AWS_ACCESS_KEY_ID'] = aws_creds['access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_creds['secret_key']
        os.environ['AWS_DEFAULT_REGION'] = aws_creds['region']

        tasks = [
            (fetch_cloudtrail_events, config, config['output_files']['cloudtrail_events']),
            (fetch_privileged_apis, config, config['output_files']['privileged_apis']),
            (fetch_user_activity, config, config['output_files']['user_activity'], username),
            (fetch_cloudtrail_status, config, config['output_files']['cloudtrail_status']),
            (fetch_log_group_activity, config, config['output_files']['log_group_activity']),
            (fetch_trail_event_selectors, config, config['output_files']['trail_event_selectors']),
            (fetch_ssm_logs, config, config['output_files']['ssm_logs']),
            (fetch_ec2_instances, config, config['output_files']['ec2_instances']),
        ]

        print(f"Starting evidence collection for environment '{env_name}'...")

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(*task): task[0].__name__ for task in tasks}
            for future in as_completed(futures):
                task_name = futures[future]
                try:
                    future.result()
                    print(f"Task '{task_name}' completed successfully.")
                except Exception as e:
                    print(f"Task '{task_name}' failed: {e}")

        print(f"Evidence collection completed for environment '{env_name}'.")

if __name__ == "__main__":
    main()
