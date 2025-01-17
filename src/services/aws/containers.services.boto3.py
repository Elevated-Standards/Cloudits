import os
import datetime
import json
import boto3
from botocore.exceptions import ClientError
from utils.aws_utils import get_aws_credentials, run_command, ensure_directories_exist

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
            'clusters': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecs_clusters.json",
            'services': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecs_services.json",
            'tasks': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecs_tasks.json",
            'task_definitions': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecs_task_definitions.json",
            'ecs_tags': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecs_tags.json",
            'public_repositories': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecr_public_repositories.json",
            'public_images': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecr_public_images.json",
            'repository_policies': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecr_repository_policies.json",
            'ecr_tags': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecr_tags.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            'clusters': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-ecs_clusters.json",
            'services': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-ecs_services.json",
            'tasks': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-ecs_tasks.json",
            'task_definitions': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-ecs_task_definitions.json",
            'ecs_tags': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-ecs_tags.json",
            'public_repositories': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-ecr_public_repositories.json",
            'public_images': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-ecr_public_images.json",
            'repository_policies': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-ecr_repository_policies.json",
            'ecr_tags': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-ecr_tags.json"
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

def fetch_clusters(client, output_file):
    clusters = client.list_clusters()['clusterArns']
    with open(output_file, 'w') as f:
        json.dump(clusters, f, indent=4)
    return clusters

def fetch_services(client, clusters, output_file):
    services = []
    for cluster in clusters:
        services.extend(client.list_services(cluster=cluster)['serviceArns'])
    with open(output_file, 'w') as f:
        json.dump(services, f, indent=4)
    return services

def fetch_tasks(client, clusters, output_file):
    tasks = []
    for cluster in clusters:
        tasks.extend(client.list_tasks(cluster=cluster)['taskArns'])
    with open(output_file, 'w') as f:
        json.dump(tasks, f, indent=4)
    return tasks

def fetch_task_definitions(client, output_file):
    task_definitions = client.list_task_definitions()['taskDefinitionArns']
    with open(output_file, 'w') as f:
        json.dump(task_definitions, f, indent=4)
    return task_definitions

def fetch_ecs_tags(client, clusters, output_file):
    tags = []
    for cluster in clusters:
        tags.append({
            'ResourceArn': cluster,
            'Tags': client.list_tags_for_resource(resourceArn=cluster)['tags']
        })
    with open(output_file, 'w') as f:
        json.dump(tags, f, indent=4)

def fetch_public_repositories(client, output_file):
    repositories = client.describe_repositories()['repositories']
    with open(output_file, 'w') as f:
        json.dump(repositories, f, indent=4)
    return repositories

def fetch_public_images(client, repositories, output_file):
    images = []
    for repo in repositories:
        images.extend(client.describe_images(repositoryName=repo['repositoryName'])['imageDetails'])
    with open(output_file, 'w') as f:
        json.dump(images, f, indent=4)

def fetch_repository_policies(client, repositories, output_file):
    policies = []
    for repo in repositories:
        policies.append({
            'RepositoryName': repo['repositoryName'],
            'Policy': client.get_repository_policy(repositoryName=repo['repositoryName'])['policyText']
        })
    with open(output_file, 'w') as f:
        json.dump(policies, f, indent=4)

def fetch_ecr_public_tags(client, repositories, output_file):
    tags = []
    for repo in repositories:
        tags.append({
            'RepositoryArn': repo['repositoryArn'],
            'Tags': client.list_tags_for_resource(resourceArn=repo['repositoryArn'])['tags']
        })
    with open(output_file, 'w') as f:
        json.dump(tags, f, indent=4)

def main():
    for env_name, config in environments.items():
        aws_creds = get_aws_credentials(env_name)
        if not aws_creds:
            print(f"Skipping environment '{env_name}' due to credential issues.")
            continue

        ecs_client = create_boto3_client('ecs', config['region'], aws_creds)
        ecr_client = create_boto3_client('ecr-public', config['region'], aws_creds)

        for file_path in config['output_files'].values():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        clusters = fetch_clusters(ecs_client, config['output_files']['clusters'])
        fetch_services(ecs_client, clusters, config['output_files']['services'])
        fetch_tasks(ecs_client, clusters, config['output_files']['tasks'])
        fetch_task_definitions(ecs_client, config['output_files']['task_definitions'])
        fetch_ecs_tags(ecs_client, clusters, config['output_files']['ecs_tags'])

        repositories = fetch_public_repositories(ecr_client, config['output_files']['public_repositories'])
        fetch_public_images(ecr_client, repositories, config['output_files']['public_images'])
        fetch_repository_policies(ecr_client, repositories, config['output_files']['repository_policies'])
        fetch_ecr_public_tags(ecr_client, repositories, config['output_files']['ecr_tags'])

    print("AWS ECS and ECR configuration evidence collection completed.")

if __name__ == "__main__":
    main()
