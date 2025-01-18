import os
import datetime, timezone, timedelta
import json
import boto3
from botocore.exceptions import ClientError
from utils.aws_utils import *

# Define current year and month for directory paths
YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
START_DATE = (datetime.datetime.utcnow() - datetime.timedelta(days=31)).isoformat()
END_DATE = datetime.datetime.utcnow().isoformat()

# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            'backup_vaults': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}-backup_vaults.json",
            'backup_plans': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}-backup_plans.json",
            'recovery_points': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}-recovery_points.json",
            'tags': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}-backup_tags.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            'backup_vaults': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-backup_vaults.json",
            'backup_plans': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-backup_plans.json",
            'recovery_points': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-recovery_points.json",
            'tags': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-backup_tags.json"
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

def fetch_backup_vaults(client, output_file):
    try:
        vaults = client.list_backup_vaults()['BackupVaultList']
        detailed_vaults = [
            client.describe_backup_vault(BackupVaultName=vault['BackupVaultName']) for vault in vaults
        ]
        with open(output_file, 'w') as f:
            json.dump(detailed_vaults, f, indent=4)
    except ClientError as e:
        print(f"Error fetching backup vaults: {str(e)}")

def fetch_backup_plans(client, output_file):
    try:
        plans = client.list_backup_plans()['BackupPlansList']
        detailed_plans = []
        for plan in plans:
            plan_id = plan['BackupPlanId']
            plan_details = client.get_backup_plan(BackupPlanId=plan_id)
            plan_versions = client.list_backup_plan_versions(BackupPlanId=plan_id)['BackupPlanVersionsList']
            plan_details['BackupPlan']['Versions'] = plan_versions
            detailed_plans.append(plan_details)
        with open(output_file, 'w') as f:
            json.dump(detailed_plans, f, indent=4)
    except ClientError as e:
        print(f"Error fetching backup plans: {str(e)}")

def fetch_recovery_points(client, output_file):
    try:
        vaults = client.list_backup_vaults()['BackupVaultList']
        recovery_points = []
        for vault in vaults:
            points = client.list_recovery_points_by_backup_vault(
                BackupVaultName=vault['BackupVaultName'],
                ByCreatedAfter=START_DATE,
                ByCreatedBefore=END_DATE
            )['RecoveryPoints']
            for point in points:
                details = client.describe_recovery_point(
                    BackupVaultName=vault['BackupVaultName'],
                    RecoveryPointArn=point['RecoveryPointArn']
                )
                recovery_points.append(details)
        with open(output_file, 'w') as f:
            json.dump(recovery_points, f, indent=4)
    except ClientError as e:
        print(f"Error fetching recovery points: {str(e)}")

def fetch_backup_tags(client, output_file):
    try:
        vaults = client.list_backup_vaults()['BackupVaultList']
        tags = []
        for vault in vaults:
            vault_tags = client.list_tags(
                ResourceArn=vault['BackupVaultArn']
            )['Tags']
            tags.append({'BackupVaultArn': vault['BackupVaultArn'], 'Tags': vault_tags})
        with open(output_file, 'w') as f:
            json.dump(tags, f, indent=4)
    except ClientError as e:
        print(f"Error fetching backup tags: {str(e)}")

def main():
    for env_name, config in environments.items():
        aws_creds = get_aws_credentials(env_name)
        if not aws_creds:
            print(f"Skipping environment '{env_name}' due to credential issues.")
            continue

        backup_client = create_boto3_client('backup', config['region'], aws_creds)

        for file_path in config['output_files'].values():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        fetch_backup_vaults(backup_client, config['output_files']['backup_vaults'])
        fetch_backup_plans(backup_client, config['output_files']['backup_plans'])
        fetch_recovery_points(backup_client, config['output_files']['recovery_points'])
        fetch_backup_tags(backup_client, config['output_files']['tags'])

    print("AWS Backup configuration evidence collection completed.")

if __name__ == "__main__":
    main()
