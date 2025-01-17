import os
import datetime
import json
import boto3
from botocore.exceptions import ClientError
from credentials.aws import get_aws_credentials

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
            'detectors': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-guardduty_detectors.json",
            'members': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-guardduty_members.json",
            'ip_sets': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-guardduty_ip_sets.json",
            'publishing_destinations': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-guardduty_publishing_destinations.json",
            'coverage': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-guardduty_coverage.json",
            'organization_configuration': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-guardduty_organization_configuration.json",
            'users': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-iam_users.json",
            'roles': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-iam_roles.json",
            'policies': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-iam_policies.json",
            'mfa_devices': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-iam_mfa_devices.json",
        }
    },
    'federal': {
        'region': 'us-west-2',
        'output_files': {
            'detectors': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-guardduty_detectors.json",
            'members': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-guardduty_members.json",
            'ip_sets': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-guardduty_ip_sets.json",
            'publishing_destinations': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-guardduty_publishing_destinations.json",
            'coverage': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-guardduty_coverage.json",
            'organization_configuration': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-guardduty_organization_configuration.json",
            'users': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-iam_users.json",
            'roles': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-iam_roles.json",
            'policies': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-iam_policies.json",
            'mfa_devices': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-iam_mfa_devices.json",
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

def fetch_and_save_data(client_method, output_file, **kwargs):
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

        guardduty_client = create_boto3_client('guardduty', config['region'], aws_creds)
        iam_client = create_boto3_client('iam', config['region'], aws_creds)

        # Create necessary directories
        for file_path in config['output_files'].values():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Fetch GuardDuty data
        fetch_and_save_data(guardduty_client.list_detectors, config['output_files']['detectors'])
        fetch_and_save_data(guardduty_client.list_members, config['output_files']['members'], DetectorId="detector-id-placeholder")
        fetch_and_save_data(guardduty_client.list_ip_sets, config['output_files']['ip_sets'], DetectorId="detector-id-placeholder")

        # Fetch IAM data
        fetch_and_save_data(iam_client.list_users, config['output_files']['users'])
        fetch_and_save_data(iam_client.list_roles, config['output_files']['roles'])
        fetch_and_save_data(iam_client.list_policies, config['output_files']['policies'], Scope='Local')

    print("Evidence collection for GuardDuty and IAM completed.")

if __name__ == "__main__":
    main()