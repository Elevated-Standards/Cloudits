from utils.project import *
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