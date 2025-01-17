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
            'alarms': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_alarms.json",
            'metrics': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_metrics.json",
            'dashboards': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_dashboards.json",
            'log_groups': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_log_groups.json",
            'tags': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_tags.json",
            'trails': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_trails.json",
            'event_data_stores': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_event_data_stores.json",
            'insights': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_insights.json",
            'tags': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_tags.json"
        }
    },
    'federal': {
        'region': 'us-west-2',
        'output_files': {
            'alarms': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_alarms.json",
            'metrics': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_metrics.json",
            'dashboards': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_dashboards.json",
            'log_groups': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_log_groups.json",
            'tags': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudwatch_tags.json",
            'trails': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_trails.json",
            'event_data_stores': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_event_data_stores.json",
            'insights': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_insights.json",
            'tags': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-cloudtrail_tags.json"
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

def fetch_cloudwatch_alarms(client, output_file):
    alarms = client.describe_alarms()
    with open(output_file, 'w') as f:
        json.dump(alarms, f, indent=4)

def fetch_cloudwatch_metrics(client, output_file):
    metrics = client.list_metrics()
    with open(output_file, 'w') as f:
        json.dump(metrics, f, indent=4)

def fetch_cloudwatch_dashboards(client, output_file):
    dashboards = client.list_dashboards()
    with open(output_file, 'w') as f:
        json.dump(dashboards, f, indent=4)

def fetch_cloudwatch_log_groups(client, output_file):
    paginator = client.get_paginator('describe_log_groups')
    log_groups = []
    try:
        for page in paginator.paginate():
            log_groups.extend(page['logGroups'])
    except ClientError as e:
        print(f"Error fetching log groups: {e}")
    with open(output_file, 'w') as f:
        json.dump(log_groups, f, indent=4)

def fetch_cloudtrail_trails(client, output_file):
    trails = client.list_trails()
    with open(output_file, 'w') as f:
        json.dump(trails, f, indent=4)

def fetch_cloudtrail_event_data_stores(client, output_file):
    event_data_stores = client.list_event_data_stores()
    with open(output_file, 'w') as f:
        json.dump(event_data_stores, f, indent=4)

def fetch_cloudtrail_insights(client, trails, output_file):
    insights = []
    for trail in trails.get('Trails', []):
        trail_name = trail['Name']
        try:
            insight_selectors = client.get_insight_selectors(TrailName=trail_name)
            insights.append({
                'TrailName': trail_name,
                'InsightSelectors': insight_selectors.get('InsightSelectors', [])
            })
        except ClientError as e:
            insights.append({'TrailName': trail_name, 'Error': str(e)})
    with open(output_file, 'w') as f:
        json.dump(insights, f, indent=4)

def main():
    for env_name, config in environments.items():
        aws_creds = get_aws_credentials(env_name)
        if not aws_creds:
            print(f"Skipping environment '{env_name}' due to credential issues.")
            continue

        cloudwatch_client = create_boto3_client('cloudwatch', config['region'], aws_creds)
        cloudtrail_client = create_boto3_client('cloudtrail', config['region'], aws_creds)
        logs_client = create_boto3_client('logs', config['region'], aws_creds)

        for file_path in config['output_files'].values():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Fetch CloudWatch data
        fetch_cloudwatch_alarms(cloudwatch_client, config['output_files']['alarms'])
        fetch_cloudwatch_metrics(cloudwatch_client, config['output_files']['metrics'])
        fetch_cloudwatch_dashboards(cloudwatch_client, config['output_files']['dashboards'])
        fetch_cloudwatch_log_groups(logs_client, config['output_files']['log_groups'])

        # Fetch CloudTrail data
        trails = fetch_cloudtrail_trails(cloudtrail_client, config['output_files']['trails'])
        fetch_cloudtrail_event_data_stores(cloudtrail_client, config['output_files']['event_data_stores'])
        fetch_cloudtrail_insights(cloudtrail_client, trails, config['output_files']['insights'])

    print("AWS CloudWatch and CloudTrail evidence collection completed.")

if __name__ == "__main__":
    main()
