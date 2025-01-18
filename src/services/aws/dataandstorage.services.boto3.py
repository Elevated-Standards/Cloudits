import os
import datetime, timezone, timedelta
import json
import boto3
from botocore.exceptions import ClientError
from utils.aws_utils import *

# Define current year, month, and day for directory paths
YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
DAY = datetime.datetime.now().day
START_DATE = (datetime.datetime.utcnow() - datetime.timedelta(days=31)).isoformat()
END_DATE = datetime.datetime.utcnow().isoformat()

# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            'db_instances': f'{BASE_DIR}/commercial/systems//aws/{YEAR}/{END_DATE}-db_instances.json',
            'db_snapshots': f'{BASE_DIR}/commercial/systems//aws/{YEAR}/{END_DATE}-db_snapshots.json',
            'db_clusters': f'{BASE_DIR}/commercial/systems//aws/{YEAR}/{END_DATE}-db_clusters.json',
            'db_security_groups': f'{BASE_DIR}/commercial/systems//aws/{YEAR}/{END_DATE}-db_security_groups.json',
            'db_subnet_groups': f'{BASE_DIR}/commercial/systems//aws/{YEAR}/{END_DATE}-db_subnet_groups.json',
            'db_log_files': f'{BASE_DIR}/commercial/systems//aws/{YEAR}/{END_DATE}-db_log_files.json',
            'certificates': f'{BASE_DIR}/commercial/systems//aws/{YEAR}/{END_DATE}-certificates.json',
            'ebs_volumes': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{END_DATE}-ebs_volumes.json',
            'ebs_snapshots': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{END_DATE}-ebs_snapshots.json',
            'ebs_lifecycle_policies': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{END_DATE}-ebs_lifecycle_policies.json',
            'efs_file_systems': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{END_DATE}-efs_file_systems.json',
            'efs_lifecycle_policies': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{END_DATE}-efs_lifecycle_policies.json',
            'efs_access_points': f'{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{END_DATE}-efs_access_points.json',
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            'db_instances': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-db_instances.json',
            'db_snapshots': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-db_snapshots.json',
            'db_clusters': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-db_clusters.json',
            'db_security_groups': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-db_security_groups.json',
            'db_subnet_groups': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-db_subnet_groups.json',
            'db_log_files': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-db_log_files.json',
            'certificates': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-certificates.json',
            'ebs_volumes': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-ebs_volumes.json',
            'ebs_snapshots': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-ebs_snapshots.json',
            'ebs_lifecycle_policies': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-ebs_lifecycle_policies.json',
            'efs_file_systems': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-efs_file_systems.json',
            'efs_lifecycle_policies': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-efs_lifecycle_policies.json',
            'efs_access_points': f'{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-efs_access_points.json',
        }
    }
}

def create_boto3_client(service, region, aws_creds):
    return boto3.client(
        service,
        region_name=region,
        aws_access_key_id=aws_creds['access_key'],
        aws_secret_access_key=aws_creds['secret_key']
    )

def fetch_data(client_method, output_file, **kwargs):
    try:
        response = client_method(**kwargs)
        with open(output_file, 'w') as f:
            json.dump(response, f, indent=4)
        return response
    except ClientError as e:
        print(f"Error fetching data: {str(e)}")
        return {}

def main():
    for env_name, config in environments.items():
        aws_creds = get_aws_credentials(env_name)
        if not aws_creds:
            print(f"Skipping environment '{env_name}' due to credential issues.")
            continue

        rds_client = create_boto3_client('rds', config['region'], aws_creds)
        ec2_client = create_boto3_client('ec2', config['region'], aws_creds)
        efs_client = create_boto3_client('efs', config['region'], aws_creds)
        dlm_client = create_boto3_client('dlm', config['region'], aws_creds)

        for file_path in config['output_files'].values():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        fetch_data(rds_client.describe_db_instances, config['output_files']['db_instances'])
        fetch_data(rds_client.describe_db_snapshots, config['output_files']['db_snapshots'])
        fetch_data(rds_client.describe_db_clusters, config['output_files']['db_clusters'])
        fetch_data(rds_client.describe_db_security_groups, config['output_files']['db_security_groups'])
        fetch_data(rds_client.describe_db_subnet_groups, config['output_files']['db_subnet_groups'])
        fetch_data(rds_client.describe_certificates, config['output_files']['certificates'])
        fetch_data(ec2_client.describe_volumes, config['output_files']['ebs_volumes'])
        fetch_data(ec2_client.describe_snapshots, config['output_files']['ebs_snapshots'], OwnerIds=['self'])
        fetch_data(dlm_client.get_lifecycle_policies, config['output_files']['ebs_lifecycle_policies'])
        fetch_data(efs_client.describe_file_systems, config['output_files']['efs_file_systems'])
        fetch_data(efs_client.describe_lifecycle_configuration, config['output_files']['efs_lifecycle_policies'])
        fetch_data(efs_client.describe_access_points, config['output_files']['efs_access_points'])

    print("AWS Data & Storage configuration evidence collection completed.")

if __name__ == "__main__":
    main()
