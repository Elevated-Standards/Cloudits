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
            'backup_vaults': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-backup_vaults.json",
            'backup_plans': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-backup_plans.json",
            'recovery_points': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-recovery_points.json",
            'tags': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-backup_tags.json",
            'replication_configs': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-replication_configs.json",
            'replication_logs': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-replication_logs.json",
            'restoration_tests': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-restoration_tests.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            'backup_vaults': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-backup_vaults.json",
            'backup_plans': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-backup_plans.json",
            'recovery_points': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-recovery_points.json",
            'tags': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-backup_tags.json",
            'replication_configs': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-replication_configs.json",
            'replication_logs': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-replication_logs.json",
            'restoration_tests': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-restoration_tests.json"
        }
    }
}