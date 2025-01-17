import os
import datetime
import json
import boto3
from botocore.exceptions import ClientError
from credentials.aws import get_aws_credentials

# Define current year and month for directory paths
YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
DAY = datetime.datetime.now().day
START_DATE = (datetime.datetime.utcnow() - datetime.timedelta(days=31)).isoformat()  # 31 days ago
END_DATE = datetime.datetime.utcnow().isoformat()  # current time

# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            'certificates': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-acm_certificates.json",
            'certificate_details': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-acm_certificate_details.json",
            'tags': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-acm_tags.json",
            'renewal_status': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-acm_renewal_status.json",
            'keys': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-kms_keys.json",
            'key_policies': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-kms_key_policies.json",
            'grants': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-kms_grants.json",
            'kms_tags': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-kms_tags.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            'certificates': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-acm_certificates.json",
            'certificate_details': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-acm_certificate_details.json",
            'tags': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-acm_tags.json",
            'renewal_status': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-acm_renewal_status.json",
            'keys': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-kms_keys.json",
            'key_policies': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-kms_key_policies.json",
            'grants': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-kms_grants.json",
            'kms_tags': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-kms_tags.json"
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

def fetch_certificates(client, output_file):
    paginator = client.get_paginator('list_certificates')
    certificates = []
    for page in paginator.paginate():
        certificates.extend(page['CertificateSummaryList'])
    with open(output_file, 'w') as f:
        json.dump(certificates, f, indent=4)
    return certificates

def fetch_certificate_details(client, certificates, output_file):
    details = []
    for cert in certificates:
        try:
            details.append(client.describe_certificate(CertificateArn=cert['CertificateArn']))
        except ClientError as e:
            details.append({'CertificateArn': cert['CertificateArn'], 'Error': str(e)})
    with open(output_file, 'w') as f:
        json.dump(details, f, indent=4)

def fetch_acm_tags(client, certificates, output_file):
    tags = []
    for cert in certificates:
        try:
            tags.append({
                'CertificateArn': cert['CertificateArn'],
                'Tags': client.list_tags_for_certificate(CertificateArn=cert['CertificateArn']).get('Tags', [])
            })
        except ClientError as e:
            tags.append({'CertificateArn': cert['CertificateArn'], 'Error': str(e)})
    with open(output_file, 'w') as f:
        json.dump(tags, f, indent=4)

def fetch_renewal_status(client, certificates, output_file):
    renewal_status = []
    for cert in certificates:
        try:
            renewal_status.append({
                'CertificateArn': cert['CertificateArn'],
                'RenewalSummary': client.describe_certificate(CertificateArn=cert['CertificateArn']).get('RenewalSummary', {})
            })
        except ClientError as e:
            renewal_status.append({'CertificateArn': cert['CertificateArn'], 'Error': str(e)})
    with open(output_file, 'w') as f:
        json.dump(renewal_status, f, indent=4)

def fetch_kms_keys(client, output_file):
    paginator = client.get_paginator('list_keys')
    keys = []
    for page in paginator.paginate():
        keys.extend(page['Keys'])
    with open(output_file, 'w') as f:
        json.dump(keys, f, indent=4)
    return keys

def fetch_kms_key_policies(client, keys, output_file):
    policies = []
    for key in keys:
        try:
            policies.append({
                'KeyId': key['KeyId'],
                'Policy': client.get_key_policy(KeyId=key['KeyId'], PolicyName='default')
            })
        except ClientError as e:
            policies.append({'KeyId': key['KeyId'], 'Error': str(e)})
    with open(output_file, 'w') as f:
        json.dump(policies, f, indent=4)

def fetch_kms_grants(client, keys, output_file):
    grants = []
    for key in keys:
        try:
            response = client.list_grants(KeyId=key['KeyId'])
            grants.extend(response.get('Grants', []))
        except ClientError as e:
            grants.append({'KeyId': key['KeyId'], 'Error': str(e)})
    with open(output_file, 'w') as f:
        json.dump(grants, f, indent=4)

def fetch_kms_tags(client, keys, output_file):
    tags = []
    for key in keys:
        try:
            tags.append({
                'KeyId': key['KeyId'],
                'Tags': client.list_resource_tags(KeyId=key['KeyId']).get('Tags', [])
            })
        except ClientError as e:
            tags.append({'KeyId': key['KeyId'], 'Error': str(e)})
    with open(output_file, 'w') as f:
        json.dump(tags, f, indent=4)

def main():
    for env_name, config in environments.items():
        aws_creds = get_aws_credentials(env_name)
        if not aws_creds:
            print(f"Skipping environment '{env_name}' due to credential issues.")
            continue

        acm_client = create_boto3_client('acm', config['region'], aws_creds)
        kms_client = create_boto3_client('kms', config['region'], aws_creds)

        for file_path in config['output_files'].values():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        certificates = fetch_certificates(acm_client, config['output_files']['certificates'])
        fetch_certificate_details(acm_client, certificates, config['output_files']['certificate_details'])
        fetch_acm_tags(acm_client, certificates, config['output_files']['tags'])
        fetch_renewal_status(acm_client, certificates, config['output_files']['renewal_status'])

        keys = fetch_kms_keys(kms_client, config['output_files']['keys'])
        fetch_kms_key_policies(kms_client, keys, config['output_files']['key_policies'])
        fetch_kms_grants(kms_client, keys, config['output_files']['grants'])
        fetch_kms_tags(kms_client, keys, config['output_files']['kms_tags'])

    print("AWS ACM and KMS configuration evidence collection completed.")

if __name__ == "__main__":
    main()
