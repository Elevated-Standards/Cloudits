# Purpose: Provide Evidence for AWS Security Related Services.#
###############################################################
import os
import subprocess
import datetime, timezone, timedelta
import json
import sys
from utils.aws_utils import *
from output_environments.security import *
from utils.project import *


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

# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            # GuardDuty Files
            'detectors': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_detectors.json",
            'members': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_members.json",
            'ip_sets': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_ip_sets.json",
            'publishing_destinations': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_publishing_destinations.json",
            'coverage': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_coverage.json",
            'malware_scan_settings': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_malware_scan_settings.json",
            'organization_configuration': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_organization_configuration.json",
            'malware_scans': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_malware_scans.json",
            # IAM Files
            'users': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-iam_users.json",
            'roles': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-iam_roles.json",
            'policies': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-iam_policies.json",
            'permissions_boundaries': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-iam_permissions_boundaries.json",
            'mfa_devices': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-iam_mfa_devices.json",
            'access_keys': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-iam_access_keys.json",
            'tags': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-iam_tags.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            # GuardDuty Files
            'detectors': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_detectors.json",
            'members': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_members.json",
            'ip_sets': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_ip_sets.json",
            'publishing_destinations': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_publishing_destinations.json",
            'coverage': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_coverage.json",
            'malware_scan_settings': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_malware_scan_settings.json",
            'organization_configuration': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_organization_configuration.json",
            'malware_scans': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_malware_scans.json",
            # IAM Files
            'users': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-iam_users.json",
            'roles': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-iam_roles.json",
            'policies': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-iam_policies.json",
            'permissions_boundaries': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-iam_permissions_boundaries.json",
            'mfa_devices': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-iam_mfa_devices.json",
            'access_keys': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-iam_access_keys.json",
            'tags': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-iam_tags.json"
        }
    }
}

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(command)}\nError: {e}")
        return {}

# GuardDuty Evidence Collection Functions
def fetch_detectors(config, output_file):
    detectors_data = run_command(['aws', 'guardduty', 'list-detectors', '--region', config['region'], '--output', 'json'])
    detailed_detectors_data = []
    for detector_id in detectors_data['DetectorIds']:
        detector_details = run_command(['aws', 'guardduty', 'get-detector', '--detector-id', detector_id, '--output', 'json'])
        detailed_detectors_data.append(detector_details)
    with open(output_file, 'w') as f:
        json.dump(detailed_detectors_data, f, indent=4)

def fetch_guardduty_members(config, output_file):
    detectors_data = run_command(['aws', 'guardduty', 'list-detectors', '--region', config['region'], '--output', 'json'])
    members_data = []
    for detector_id in detectors_data['DetectorIds']:
        member_accounts = run_command(['aws', 'guardduty', 'list-members', '--detector-id', detector_id, '--output', 'json'])
        members_data.extend(member_accounts.get('Members', []))
    with open(output_file, 'w') as f:
        json.dump(members_data, f, indent=4)

def fetch_ip_sets(config, output_file):
    detectors_data = run_command(['aws', 'guardduty', 'list-detectors', '--region', config['region'], '--output', 'json'])
    ip_sets_data = []
    for detector_id in detectors_data['DetectorIds']:
        ip_sets = run_command(['aws', 'guardduty', 'list-ip-sets', '--detector-id', detector_id, '--output', 'json'])
        for ip_set_id in ip_sets['IpSetIds']:
            ip_set_details = run_command(['aws', 'guardduty', 'get-ip-set', '--detector-id', detector_id, '--ip-set-id', ip_set_id, '--output', 'json'])
            ip_sets_data.append(ip_set_details)
    with open(output_file, 'w') as f:
        json.dump(ip_sets_data, f, indent=4)

def fetch_guardduty_publishing_destinations(config, output_file):
    detectors_data = run_command(['aws', 'guardduty', 'list-detectors', '--region', config['region'], '--output', 'json'])
    publishing_destinations_data = []
    for detector_id in detectors_data['DetectorIds']:
        destinations = run_command(['aws', 'guardduty', 'list-publishing-destinations', '--detector-id', detector_id, '--output', 'json'])
        for destination in destinations['Destinations']:
            destination_details = run_command(['aws', 'guardduty', 'describe-publishing-destination', '--detector-id', detector_id, '--destination-id', destination['DestinationId'], '--output', 'json'])
            publishing_destinations_data.append(destination_details)
    with open(output_file, 'w') as f:
        json.dump(publishing_destinations_data, f, indent=4)

def fetch_guardduty_coverage(config, output_file):
    detectors_data = run_command(['aws', 'guardduty', 'list-detectors', '--region', config['region'], '--output', 'json'])
    coverage_data = []
    for detector_id in detectors_data['DetectorIds']:
        coverage_details = run_command(['aws', 'guardduty', 'list-coverage', '--detector-id', detector_id, '--output', 'json'])
        coverage_data.extend(coverage_details.get('CoveredResources', []))
    with open(output_file, 'w') as f:
        json.dump(coverage_data, f, indent=4)

def fetch_organization_configuration(config, output_file):
    detectors_data = run_command(['aws', 'guardduty', 'list-detectors', '--region', config['region'], '--output', 'json'])
    organization_config_data = []
    for detector_id in detectors_data['DetectorIds']:
        org_config = run_command(['aws', 'guardduty', 'describe-organization-configuration', '--detector-id', detector_id, '--output', 'json'])
        organization_config_data.append(org_config)
    with open(output_file, 'w') as f:
        json.dump(organization_config_data, f, indent=4)

# Fetch details of malware scans within the last 31 days
def fetch_malware_scans(config, output_file):
    detectors_data = run_command(['aws', 'guardduty', 'list-detectors', '--region', config['region'], '--output', 'json'])
    malware_scans_data = []
    for detector_id in detectors_data['DetectorIds']:
        malware_scans = run_command([
            'aws', 'guardduty', 'describe-malware-scans',
            '--detector-id', detector_id,
            '--start-time', START_DATE,
            '--end-time', END_DATE,
            '--output', 'json'
        ])
        malware_scans_data.extend(malware_scans.get('MalwareScans', []))
    with open(output_file, 'w') as f:
        json.dump(malware_scans_data, f, indent=4)

def fetch_malware_scan_settings(config, output_file):
    """
    Fetch malware scan settings for all GuardDuty detectors in the specified region and save them to a file.
    """
    detectors_data = run_command(['aws', 'guardduty', 'list-detectors', '--region', config['region'], '--output', 'json'])
    malware_scan_settings_data = []
    
    for detector_id in detectors_data.get('DetectorIds', []):
        try:
            settings = run_command(['aws', 'guardduty', 'get-malware-scan-settings', '--detector-id', detector_id, '--output', 'json'])
            malware_scan_settings_data.append({
                'DetectorId': detector_id,
                'MalwareScanSettings': settings
            })
        except subprocess.CalledProcessError as e:
            print(f"Failed to fetch malware scan settings for detector '{detector_id}': {e.stderr}")
    
    # Save the collected malware scan settings to the output file
    with open(output_file, 'w') as f:
        json.dump(malware_scan_settings_data, f, indent=4)
    
    print(f"Malware scan settings saved to {output_file}.")


# IAM Evidence Collection Functions
def fetch_iam_users(config, output_file):
    users_data = run_command(['aws', 'iam', 'list-users', '--region', config['region'], '--output', 'json'])
    detailed_users_data = []
    for user in users_data['Users']:
        user_name = user['UserName']
        user_details = run_command(['aws', 'iam', 'get-user', '--user-name', user_name, '--output', 'json'])
        detailed_users_data.append(user_details)
    with open(output_file, 'w') as f:
        json.dump(detailed_users_data, f, indent=4)

def fetch_roles(config, output_file):
    roles_data = run_command(['aws', 'iam', 'list-roles', '--region', config['region'], '--output', 'json'])
    detailed_roles_data = []
    for role in roles_data['Roles']:
        role_name = role['RoleName']
        role_details = run_command(['aws', 'iam', 'get-role', '--role-name', role_name, '--output', 'json'])
        detailed_roles_data.append(role_details)
    with open(output_file, 'w') as f:
        json.dump(detailed_roles_data, f, indent=4)

# Fetch detailed information for each IAM policy
def fetch_iam_policies(config, output_file):
    policies_data = run_command(['aws', 'iam', 'list-policies', '--scope', 'Local', '--region', config['region'], '--output', 'json'])
    detailed_policies_data = []
    for policy in policies_data['Policies']:
        policy_arn = policy['Arn']
        policy_details = run_command(['aws', 'iam', 'get-policy', '--policy-arn', policy_arn, '--output', 'json'])
        policy_version_id = policy_details['Policy']['DefaultVersionId']
        policy_version = run_command(['aws', 'iam', 'get-policy-version', '--policy-arn', policy_arn, '--version-id', policy_version_id, '--output', 'json'])
        policy_details['Policy']['PolicyVersion'] = policy_version
        detailed_policies_data.append(policy_details)
    with open(output_file, 'w') as f:
        json.dump(detailed_policies_data, f, indent=4)

# Fetch permissions boundaries for each IAM role and user
def fetch_permissions_boundaries(config, output_file):
    roles_data = run_command(['aws', 'iam', 'list-roles', '--output', 'json'])
    permissions_data = []
    for role in roles_data['Roles']:
        if 'PermissionsBoundary' in role:
            boundary = role['PermissionsBoundary']
            permissions_data.append({
                'RoleName': role['RoleName'],
                'PermissionsBoundary': boundary
            })
    users_data = run_command(['aws', 'iam', 'list-users', '--output', 'json'])
    for user in users_data['Users']:
        if 'PermissionsBoundary' in user:
            boundary = user['PermissionsBoundary']
            permissions_data.append({
                'UserName': user['UserName'],
                'PermissionsBoundary': boundary
            })
    with open(output_file, 'w') as f:
        json.dump(permissions_data, f, indent=4)

# Fetch MFA devices for each IAM user
def fetch_mfa_devices(config, output_file):
    users_data = run_command(['aws', 'iam', 'list-users', '--region', config['region'], '--output', 'json'])
    mfa_data = []
    for user in users_data['Users']:
        user_name = user['UserName']
        mfa_devices = run_command(['aws', 'iam', 'list-mfa-devices', '--user-name', user_name, '--output', 'json'])
        mfa_data.extend(mfa_devices['MFADevices'])
    with open(output_file, 'w') as f:
        json.dump(mfa_data, f, indent=4)

# Fetch access keys for each IAM user, including those created in the past 31 days
def fetch_access_keys(config, output_file):
    users_data = run_command(['aws', 'iam', 'list-users', '--region', config['region'], '--output', 'json'])
    access_keys_data = []
    for user in users_data['Users']:
        user_name = user['UserName']
        access_keys = run_command(['aws', 'iam', 'list-access-keys', '--user-name', user_name, '--output', 'json'])
        recent_keys = [key for key in access_keys['AccessKeyMetadata'] if key['CreateDate'] >= START_DATE]
        access_keys_data.append({
            'UserName': user_name,
            'AccessKeys': recent_keys
        })
    with open(output_file, 'w') as f:
        json.dump(access_keys_data, f, indent=4)

# Fetch tags for IAM resources (e.g., users and roles)
def fetch_iam_tags(config, output_file):
    resources = ['User', 'Role']
    tags_data = []
    for resource_type in resources:
        list_command = 'list-users' if resource_type == 'User' else 'list-roles'
        resources_data = run_command(['aws', 'iam', list_command, '--region', config['region'], '--output', 'json'])
        for resource in resources_data[resource_type + 's']:
            resource_name = resource['UserName'] if resource_type == 'User' else resource['RoleName']
            tags = run_command(['aws', 'iam', 'list-user-tags' if resource_type == 'User' else 'list-role-tags', '--' + resource_type.lower() + '-name', resource_name, '--output', 'json'])
            tags_data.append({
                resource_type + 'Name': resource_name,
                'Tags': tags['Tags']
            })
    with open(output_file, 'w') as f:
        json.dump(tags_data, f, indent=4)

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

        # Collect evidence for AWS GuardDuty configurations
        fetch_detectors(config, config['output_files']['detectors'])
        fetch_guardduty_members(config, config['output_files']['members'])
        fetch_ip_sets(config, config['output_files']['ip_sets'])
        fetch_guardduty_publishing_destinations(config, config['output_files']['publishing_destinations'])
        fetch_guardduty_coverage(config, config['output_files']['coverage'])
        fetch_malware_scan_settings(config, config['output_files']['malware_scan_settings'])  # Newly defined function
        fetch_organization_configuration(config, config['output_files']['organization_configuration'])
        fetch_malware_scans(config, config['output_files']['malware_scans'])  # Existing function

        # Collect evidence for AWS IAM configurations
        fetch_iam_users(config, config['output_files']['users'])
        fetch_roles(config, config['output_files']['roles'])
        fetch_iam_policies(config, config['output_files']['policies'])
        fetch_permissions_boundaries(config, config['output_files']['permissions_boundaries'])
        fetch_mfa_devices(config, config['output_files']['mfa_devices'])
        fetch_access_keys(config, config['output_files']['access_keys'])
        fetch_iam_tags(config, config['output_files']['tags'])

    print("AWS GuardDuty and IAM configuration evidence collection completed for all environments.")
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