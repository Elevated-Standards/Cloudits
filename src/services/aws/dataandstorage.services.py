# Purpose: Provide Evidence for AWS Data & Storage Related Services.#
#####################################################################
import os
import subprocess
import datetime, timezone, timedelta
import json
import sys
from utils.aws_utils import *
from output_environments.dataandstorage import *
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
            'db_instances': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-db_instances.json',
            'db_snapshots': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-db_snapshots.json',
            'db_clusters': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-db_clusters.json',
            'db_security_groups': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-db_security_groups.json',
            'db_subnet_groups': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-db_subnet_groups.json',
            'db_log_files': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-db_log_files.json',
            'certificates': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-certificates.json',
            'ebs_volumes': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ebs_volumes.json',
            'ebs_snapshots': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ebs_snapshots.json',
            'ebs_lifecycle_policies': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ebs_lifecycle_policies.json',
            'efs_file_systems': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-efs_file_systems.json',
            'efs_lifecycle_policies': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-efs_lifecycle_policies.json',
            'efs_access_points': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-efs_access_points.json',
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            'db_instances': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-db_instances.json',
            'db_snapshots': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-db_snapshots.json',
            'db_clusters': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-db_clusters.json',
            'db_security_groups': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-db_security_groups.json',
            'db_subnet_groups': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-db_subnet_groups.json',
            'db_log_files': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-db_log_files.json',
            'certificates': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-certificates.json',
            'ebs_volumes': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ebs_volumes.json',
            'ebs_snapshots': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ebs_snapshots.json',
            'ebs_lifecycle_policies': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ebs_lifecycle_policies.json',
            'efs_file_systems': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-efs_file_systems.json',
            'efs_lifecycle_policies': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-efs_lifecycle_policies.json',
            'efs_access_points': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-efs_access_points.json',
        }
    }
}

# Helper function to run AWS CLI commands
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return json.loads(result.stdout)

# Function to fetch all DB instances and their details
def fetch_db_instances(config, output_file):
    #######################################
    # Framework(s): 
    #######################################
    list_data = run_command(['aws', 'rds', 'describe-db-instances', '--region', config['region'], '--output', 'json'])
    detailed_data = []
    for db_instance in list_data['DBInstances']:
        db_instance_id = db_instance['DBInstanceIdentifier']
        details = run_command(['aws', 'rds', 'describe-db-instances', '--db-instance-identifier', db_instance_id, '--output', 'json'])
        detailed_data.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_data, f, indent=4)

# Function to fetch all DB snapshots and their details
def fetch_db_snapshots(config, output_file):
    #######################################
    # Framework(s): 
    #######################################
    list_data = run_command(['aws', 'rds', 'describe-db-snapshots', '--region', config['region'], '--output', 'json'])
    detailed_data = []
    for snapshot in list_data['DBSnapshots']:
        snapshot_id = snapshot['DBSnapshotIdentifier']
        details = run_command(['aws', 'rds', 'describe-db-snapshots', '--db-snapshot-identifier', snapshot_id, '--output', 'json'])
        detailed_data.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_data, f, indent=4)

# Function to fetch all DB clusters and their details
def fetch_db_clusters(config, output_file):
    #######################################
    # Framework(s): 
    #######################################
    list_data = run_command(['aws', 'rds', 'describe-db-clusters', '--region', config['region'], '--output', 'json'])
    detailed_data = []
    for db_cluster in list_data.get('DBClusters', []):
        db_cluster_id = db_cluster['DBClusterIdentifier']
        details = run_command(['aws', 'rds', 'describe-db-clusters', '--db-cluster-identifier', db_cluster_id, '--output', 'json'])
        detailed_data.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_data, f, indent=4)

# Function to fetch all DB security groups and their details
def fetch_db_security_groups(config, output_file):
    #######################################
    # Framework(s): 
    #######################################
    list_data = run_command(['aws', 'rds', 'describe-db-security-groups', '--region', config['region'], '--output', 'json'])
    detailed_data = []
    for db_sg in list_data.get('DBSecurityGroups', []):
        db_sg_name = db_sg['DBSecurityGroupName']
        details = run_command(['aws', 'rds', 'describe-db-security-groups', '--db-security-group-name', db_sg_name, '--output', 'json'])
        detailed_data.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_data, f, indent=4)

# Function to fetch all DB subnet groups and their details
def fetch_db_subnet_groups(config, output_file):
    #######################################
    # Framework(s): 
    #######################################
    list_data = run_command(['aws', 'rds', 'describe-db-subnet-groups', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(list_data['DBSubnetGroups'], f, indent=4)

# Function to fetch DB log files for each DB instance
def fetch_db_log_files(config, output_file):
    #######################################
    # Framework(s): 
    #######################################
    db_instances = run_command(['aws', 'rds', 'describe-db-instances', '--region', config['region'], '--output', 'json'])
    log_files_data = {}
    for db_instance in db_instances['DBInstances']:
        db_instance_id = db_instance['DBInstanceIdentifier']
        logs = run_command(['aws', 'rds', 'describe-db-log-files', '--db-instance-identifier', db_instance_id, '--output', 'json'])
        log_files_data[db_instance_id] = logs.get('DescribeDBLogFiles', [])
    with open(output_file, 'w') as f:
        json.dump(log_files_data, f, indent=4)

# Function to fetch all certificates and their details
def fetch_certificates(config, output_file):
    #######################################
    # Framework(s): 
    #######################################
    list_data = run_command(['aws', 'rds', 'describe-certificates', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(list_data['Certificates'], f, indent=4)

# EBS Functions
def fetch_ebs_volumes(config, output_file):
    #######################################
    # Framework(s): 
    #######################################
    print("Fetching EBS volumes...")
    volumes = run_command(['aws', 'ec2', 'describe-volumes', '--region', config['region'], '--output', 'json'])
    detailed_volumes = []
    for volume in volumes.get('Volumes', []):
        volume_id = volume['VolumeId']
        details = run_command(['aws', 'ec2', 'describe-volumes', '--volume-ids', volume_id, '--region', config['region'], '--output', 'json'])
        detailed_volumes.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_volumes, f, indent=4)

def fetch_ebs_snapshots(config, output_file):
    #######################################
    # Framework(s): 
    #######################################
    print("Fetching EBS snapshots...")
    snapshots = run_command(['aws', 'ec2', 'describe-snapshots', '--owner-ids', 'self', '--region', config['region'], '--output', 'json'])
    detailed_snapshots = []
    for snapshot in snapshots.get('Snapshots', []):
        snapshot_id = snapshot['SnapshotId']
        details = run_command(['aws', 'ec2', 'describe-snapshots', '--snapshot-ids', snapshot_id, '--region', config['region'], '--output', 'json'])
        detailed_snapshots.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_snapshots, f, indent=4)

def fetch_ebs_lifecycle_policies(config, output_file):
    #######################################
    # Framework(s): 
    #######################################
    print("Fetching EBS lifecycle policies...")
    policies = run_command(['aws', 'dlm', 'get-lifecycle-policies', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(policies, f, indent=4)

# EFS Functions
def fetch_efs_file_systems(config, output_file):
    #######################################
    # Framework(s): 
    #######################################
    print("Fetching EFS file systems...")
    file_systems = run_command(['aws', 'efs', 'describe-file-systems', '--region', config['region'], '--output', 'json'])
    detailed_file_systems = []
    for fs in file_systems.get('FileSystems', []):
        fs_id = fs['FileSystemId']
        details = run_command(['aws', 'efs', 'describe-file-systems', '--file-system-id', fs_id, '--region', config['region'], '--output', 'json'])
        detailed_file_systems.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_file_systems, f, indent=4)

def fetch_efs_lifecycle_policies(config, output_file):
    #######################################
    # Framework(s): 
    #######################################
    print("Fetching EFS lifecycle policies...")
    file_systems = run_command(['aws', 'efs', 'describe-file-systems', '--region', config['region'], '--output', 'json'])
    lifecycle_policies = []
    for fs in file_systems.get('FileSystems', []):
        fs_id = fs['FileSystemId']
        policy = run_command(['aws', 'efs', 'describe-lifecycle-configuration', '--file-system-id', fs_id, '--region', config['region'], '--output', 'json'])
        lifecycle_policies.append({'FileSystemId': fs_id, 'LifecycleConfiguration': policy})
    with open(output_file, 'w') as f:
        json.dump(lifecycle_policies, f, indent=4)

def fetch_efs_access_points(config, output_file):
    #######################################
    # Framework(s): 
    #######################################
    print("Fetching EFS access points...")
    access_points = run_command(['aws', 'efs', 'describe-access-points', '--region', config['region'], '--output', 'json'])
    detailed_access_points = []
    for ap in access_points.get('AccessPoints', []):
        ap_id = ap['AccessPointId']
        details = run_command(['aws', 'efs', 'describe-access-points', '--access-point-id', ap_id, '--region', config['region'], '--output', 'json'])
        detailed_access_points.append(details)
    with open(output_file, 'w') as f:
        json.dump(detailed_access_points, f, indent=4)

# RDS Evidence Collection Functions
def fetch_rds_validation_logs(config, output_file):
    #######################################
    # Framework(s): 
    #######################################
    print("Fetching RDS validation logs...")
    db_instances = run_command(['aws', 'rds', 'describe-db-instances', '--region', config['region'], '--output', 'json'])
    log_files_data = {}
    for db_instance in db_instances['DBInstances']:
        db_instance_id = db_instance['DBInstanceIdentifier']
        logs = run_command(['aws', 'rds', 'describe-db-log-files', '--db-instance-identifier', db_instance_id, '--output', 'json'])
        for log_file in logs.get('DescribeDBLogFiles', []):
            log_name = log_file['LogFileName']
            log_content = run_command(['aws', 'rds', 'download-db-log-file-portion', '--db-instance-identifier', db_instance_id, '--log-file-name', log_name, '--output', 'text'])
            log_files_data[db_instance_id] = {log_name: log_content}
    with open(output_file, 'w') as f:
        json.dump(log_files_data, f, indent=4)

def fetch_rds_data(config, data_type, output_file):
    #######################################
    # Framework(s): 
    #######################################
    print(f"Fetching RDS {data_type}...")
    command = ['aws', 'rds', f'describe-{data_type}', '--region', config['region'], '--output', 'json']
    data = run_command(command)
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

# DynamoDB Evidence Collection Functions
def fetch_dynamodb_table_schema(config, output_file):
    #######################################
    # Framework(s): 
    #######################################
    print("Fetching DynamoDB table schema...")
    tables = run_command(['aws', 'dynamodb', 'list-tables', '--region', config['region'], '--output', 'json'])
    table_details = []
    for table_name in tables.get('TableNames', []):
        table_info = run_command(['aws', 'dynamodb', 'describe-table', '--table-name', table_name, '--region', config['region'], '--output', 'json'])
        table_details.append(table_info)
    with open(output_file, 'w') as f:
        json.dump(table_details, f, indent=4)


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

        # Collect evidence for each RDS configuration type
        fetch_db_instances(config, config['output_files']['db_instances'])
        fetch_db_snapshots(config, config['output_files']['db_snapshots'])
        fetch_db_clusters(config, config['output_files']['db_clusters'])
        fetch_db_security_groups(config, config['output_files']['db_security_groups'])
        fetch_db_subnet_groups(config, config['output_files']['db_subnet_groups'])
        fetch_db_log_files(config, config['output_files']['db_log_files'])
        fetch_certificates(config, config['output_files']['certificates'])
        fetch_rds_validation_logs(config, config['output_files']['db_log_files'])
        fetch_dynamodb_table_schema(config, config['output_files']['dynamodb_schema'])
        
        # Collect evidence for EBS configurations
        fetch_ebs_volumes(config, config['output_files']['ebs_volumes'])
        fetch_ebs_snapshots(config, config['output_files']['ebs_snapshots'])
        fetch_ebs_lifecycle_policies(config, config['output_files']['ebs_lifecycle_policies'])

        # Collect evidence for EFS configurations
        fetch_efs_file_systems(config, config['output_files']['efs_file_systems'])
        fetch_efs_lifecycle_policies(config, config['output_files']['efs_lifecycle_policies'])
        fetch_efs_access_points(config, config['output_files']['efs_access_points'])

    print("Evidence collection completed.")

# Execute main function
if __name__ == "__main__":
    main()
    
###############################################################
# Framework: 
# - SOC 2: CC2.1, PI1.2
# - ISO 27001: A.#.#
###############################################################
# Auditor 1 - A-Lign ID's: 
# - R-1039 - Evidence that edit checks are in place to prevent incomplete or incorrect data from being entered into the production system
# - 
###############################################################
# Auditor 2 - <Placeholder> ID's: 
# - 
###############################################################