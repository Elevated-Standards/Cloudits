from utils.utils import *
from utils.aws_utils import *

# Fetch shared date information and base directory
date_info = get_current_date_info()
BASE_DIR = get_base_dir()
YEAR = date_info["year"]
MONTH = date_info["month"]
END_DATE = date_info["end_date"]

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
