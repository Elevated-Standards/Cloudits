# Purpose: Provide Evidence for AWS Container Related Services.#
################################################################
import os
import subprocess
import datetime, timezone, timedelta 
import json
import sys
from utils.aws_utils import *
from output_environments.containers import *

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
            # ECS Files
            'clusters': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecs_clusters.json",
            'services': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecs_services.json",
            'tasks': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecs_tasks.json",
            'task_definitions': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecs_task_definitions.json",
            'ecs_tags': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecs_tags.json",
            # ECR Public Files
            'public_repositories': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecr_public_repositories.json",
            'public_images': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecr_public_images.json",
            'public_repository_policies': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecr_public_repository_policies.json",
            'public_ecr_tags': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecr_public_tags.json",
            # ECR Private Files
            'private_repositories': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecr_private_repositories.json",
            'private_images': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecr_private_images.json",
            'private_repository_policies': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecr_private_repository_policies.json",
            'private_ecr_tags': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-ecr_private_tags.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            # ECS Files
            'clusters': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ecs_clusters.json",
            'services': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ecs_services.json",
            'tasks': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ecs_tasks.json",
            'task_definitions': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ecs_task_definitions.json",
            'ecs_tags': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ecs_tags.json",
            # ECR Public Files
            'public_repositories': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ecr_public_repositories.json",
            'public_images': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ecr_public_images.json",
            'public_repository_policies': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ecr_public_repository_policies.json",
            'public_ecr_tags': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ecr_public_tags.json",
            # ECR Private Files
            'private_repositories': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ecr_private_repositories.json",
            'private_images': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ecr_private_images.json",
            'private_repository_policies': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ecr_private_repository_policies.json",
            'private_ecr_tags': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-ecr_private_tags.json"
        }
    }
}

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(command)}\nError: {e.stderr}")
        return {}

# ECS Evidence Collection Functions
def fetch_clusters(config, output_file):
    clusters_data = run_command(['aws', 'ecs', 'list-clusters', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(clusters_data, f, indent=4)

def fetch_services(config, output_file):
    clusters_data = run_command(['aws', 'ecs', 'list-clusters', '--region', config['region'], '--output', 'json'])
    services_data = []
    for cluster_arn in clusters_data.get('clusterArns', []):
        services = run_command(['aws', 'ecs', 'list-services', '--cluster', cluster_arn, '--output', 'json'])
        services_data.extend(services.get('serviceArns', []))
    with open(output_file, 'w') as f:
        json.dump(services_data, f, indent=4)

def fetch_tasks(config, output_file):
    clusters_data = run_command(['aws', 'ecs', 'list-clusters', '--region', config['region'], '--output', 'json'])
    tasks_data = []
    for cluster_arn in clusters_data.get('clusterArns', []):
        tasks = run_command(['aws', 'ecs', 'list-tasks', '--cluster', cluster_arn, '--output', 'json'])
        tasks_data.extend(tasks.get('taskArns', []))
    with open(output_file, 'w') as f:
        json.dump(tasks_data, f, indent=4)

def fetch_task_definitions(config, output_file):
    task_definitions_data = run_command(['aws', 'ecs', 'list-task-definitions', '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(task_definitions_data, f, indent=4)

def fetch_ecs_tags(config, output_file):
    clusters_data = run_command(['aws', 'ecs', 'list-clusters', '--region', config['region'], '--output', 'json'])
    tags_data = []
    for cluster_arn in clusters_data.get('clusterArns', []):
        cluster_tags = run_command(['aws', 'ecs', 'list-tags-for-resource', '--resource-arn', cluster_arn, '--output', 'json'])
        tags_data.append({'ResourceArn': cluster_arn, 'Tags': cluster_tags.get('tags', [])})
    with open(output_file, 'w') as f:
        json.dump(tags_data, f, indent=4)

# ECR Evidence Collection Functions
def fetch_public_repositories(config, output_file):
    print(f"Fetching public repositories for {config['region']}...")
    public_repositories_data = run_command(['aws', 'ecr-public', 'describe-repositories', '--output', 'json'])
    if public_repositories_data:
        with open(output_file, 'w') as f:
            json.dump(public_repositories_data, f, indent=4)

def fetch_public_images(config, output_file):
    print(f"Fetching public images for repositories in {config['region']}...")
    repositories_data = run_command(['aws', 'ecr-public', 'describe-repositories', '--output', 'json'])
    images_data = []
    if repositories_data:
        for repo in repositories_data.get('repositories', []):
            repo_name = repo['repositoryName']
            images = run_command(['aws', 'ecr-public', 'describe-images', '--repository-name', repo_name, '--output', 'json'])
            if images:
                images_data.extend(images.get('imageDetails', []))
        with open(output_file, 'w') as f:
            json.dump(images_data, f, indent=4)

# Fetch policies for public repositories
def fetch_public_repository_policies(config, output_file):
    print(f"Fetching public repository policies for {config['region']}...")
    repositories_data = run_command(['aws', 'ecr-public', 'describe-repositories', '--output', 'json'])
    repository_policies_data = []
    if repositories_data:
        for repo in repositories_data.get('repositories', []):
            repo_name = repo['repositoryName']
            repo_policy = run_command(['aws', 'ecr-public', 'get-repository-policy', '--repository-name', repo_name, '--output', 'json'])
            if repo_policy:
                repository_policies_data.append({'RepositoryName': repo_name, 'Policy': repo_policy})
        with open(output_file, 'w') as f:
            json.dump(repository_policies_data, f, indent=4)

# Fetch tags for public repositories
def fetch_ecr_public_tags(config, output_file):
    print(f"Fetching tags for public repositories for {config['region']}...")
    repositories_data = run_command(['aws', 'ecr-public', 'describe-repositories', '--output', 'json'])
    tags_data = []
    if repositories_data:
        for repo in repositories_data.get('repositories', []):
            repo_arn = repo['repositoryArn']
            repo_tags = run_command(['aws', 'ecr-public', 'list-tags-for-resource', '--resource-arn', repo_arn, '--output', 'json'])
            if repo_tags:
                tags_data.append({'RepositoryArn': repo_arn, 'Tags': repo_tags.get('tags', [])})
        with open(output_file, 'w') as f:
            json.dump(tags_data, f, indent=4)


def fetch_private_repositories(config, output_file):
    print(f"Fetching private repositories for {config['region']}...")
    private_repositories_data = run_command(['aws', 'ecr', 'describe-repositories', '--region', config['region'], '--output', 'json'])
    if private_repositories_data:
        with open(output_file, 'w') as f:
            json.dump(private_repositories_data, f, indent=4)

def fetch_private_images(config, output_file):
    print(f"Fetching private images for repositories in {config['region']}...")
    repositories_data = run_command(['aws', 'ecr', 'describe-repositories', '--region', config['region'], '--output', 'json'])
    images_data = []
    if repositories_data:
        for repo in repositories_data.get('repositories', []):
            repo_name = repo['repositoryName']
            images = run_command(['aws', 'ecr', 'describe-images', '--repository-name', repo_name, '--region', config['region'], '--output', 'json'])
            if images:
                images_data.extend(images.get('imageDetails', []))
        with open(output_file, 'w') as f:
            json.dump(images_data, f, indent=4)

def fetch_private_repository_policies(config, output_file):
    print(f"Fetching private repository policies for {config['region']}...")
    repositories_data = run_command(['aws', 'ecr', 'describe-repositories', '--region', config['region'], '--output', 'json'])
    repository_policies_data = []
    if repositories_data:
        for repo in repositories_data.get('repositories', []):
            repo_name = repo['repositoryName']
            repo_policy = run_command(['aws', 'ecr', 'get-repository-policy', '--repository-name', repo_name, '--region', config['region'], '--output', 'json'])
            if repo_policy:
                repository_policies_data.append({'RepositoryName': repo_name, 'Policy': repo_policy})
        with open(output_file, 'w') as f:
            json.dump(repository_policies_data, f, indent=4)

def fetch_private_tags(config, output_file):
    print(f"Fetching tags for private repositories in {config['region']}...")
    repositories_data = run_command(['aws', 'ecr', 'describe-repositories', '--region', config['region'], '--output', 'json'])
    tags_data = []
    if repositories_data:
        for repo in repositories_data.get('repositories', []):
            repo_arn = repo['repositoryArn']
            repo_tags = run_command(['aws', 'ecr', 'list-tags-for-resource', '--resource-arn', repo_arn, '--region', config['region'], '--output', 'json'])
            if repo_tags:
                tags_data.append({'RepositoryArn': repo_arn, 'Tags': repo_tags.get('tags', [])})
        with open(output_file, 'w') as f:
            json.dump(tags_data, f, indent=4)

# Main function to execute each evidence collection task for both environments
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
        
        # Collect evidence for ECS configurations
        fetch_clusters(config, config['output_files']['clusters'])
        fetch_services(config, config['output_files']['services'])
        fetch_tasks(config, config['output_files']['tasks'])
        fetch_task_definitions(config, config['output_files']['task_definitions'])
        fetch_ecs_tags(config, config['output_files']['ecs_tags'])

        # Collect evidence for ECR configurations (Public)
        fetch_public_repositories(config, config['output_files']['public_repositories'])
        fetch_public_images(config, config['output_files']['public_images'])
        fetch_public_repository_policies(config, config['output_files']['public_repository_policies'])
        fetch_ecr_public_tags(config, config['output_files']['public_ecr_tags'])

        # Collect evidence for ECR configurations (Private)
        fetch_private_repositories(config, config['output_files']['private_repositories'])
        fetch_private_images(config, config['output_files']['private_images'])
        fetch_private_repository_policies(config, config['output_files']['private_repository_policies'])
        fetch_private_tags(config, config['output_files']['private_ecr_tags'])


    print("AWS ECS and ECR (Public & Private) evidence collection completed for both environments.")

# Execute main function
if __name__ == "__main__":
    main()
