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

# Replace with actual configuration set name and resource ARN
config_set_name = 'YOUR_CONFIG_SET_NAME'
resource_arn = 'YOUR_RESOURCE_ARN'

# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            'identities': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-sesv2_email_identities.json",
            'configuration_sets': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-sesv2_configuration_sets.json",
            'dedicated_ips': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-sesv2_dedicated_ips.json",
            'event_destinations': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-sesv2_event_destinations.json",
            'tags': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-sesv2_tags.json"
        }
    },
    'federal': {
        'region': 'us-west-2',
        'output_files': {
            'identities': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-sesv2_email_identities.json",
            'configuration_sets': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-sesv2_configuration_sets.json",
            'dedicated_ips': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-sesv2_dedicated_ips.json",
            'event_destinations': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-sesv2_event_destinations.json",
            'tags': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-sesv2_tags.json"
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

        sesv2_client = create_boto3_client('sesv2', config['region'], aws_creds)

        # Create necessary directories
        for file_path in config['output_files'].values():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Fetch SESv2 data
        fetch_and_save_data(sesv2_client.list_email_identities, config['output_files']['identities'])
        fetch_and_save_data(sesv2_client.list_configuration_sets, config['output_files']['configuration_sets'])
        fetch_and_save_data(sesv2_client.list_dedicated_ips, config['output_files']['dedicated_ips'])
        fetch_and_save_data(
            sesv2_client.list_event_destinations,
            config['output_files']['event_destinations'],
            ConfigurationSetName=config_set_name
        )
        fetch_and_save_data(
            sesv2_client.list_tags_for_resource,
            config['output_files']['tags'],
            ResourceArn=resource_arn
        )

    print("AWS SES v2 configuration evidence collection completed.")

if __name__ == "__main__":
    main()
