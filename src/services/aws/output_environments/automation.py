from utils.utils import *
from utils.aws_utils import *

# Fetch shared date information and base directory
date_info = get_current_date_info()
BASE_DIR = get_base_dir()
YEAR = date_info["year"]
MONTH = date_info["month"]
END_DATE = date_info["end_date"]

environments = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            'functions': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-lambda_functions.json",
            'environment_variables': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-lambda_environment_variables.json",
            'execution_roles': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-lambda_execution_roles.json",
            'function_policies': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-lambda_function_policies.json",
            'event_source_mappings': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-lambda_event_source_mappings.json",
            'tags': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-lambda_tags.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            'functions': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{MONTH}-lambda_functions.json",
            'environment_variables': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{MONTH}-lambda_environment_variables.json",
            'execution_roles': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{MONTH}-lambda_execution_roles.json",
            'function_policies': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{MONTH}-lambda_function_policies.json",
            'event_source_mappings': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{MONTH}-lambda_event_source_mappings.json",
            'tags': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{MONTH}-lambda_tags.json"
        }
    }
}