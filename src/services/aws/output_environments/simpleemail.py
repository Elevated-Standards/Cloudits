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
            'identities': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-sesv2_email_identities.json",
            'configuration_sets': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-sesv2_configuration_sets.json",
            'dedicated_ips': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-sesv2_dedicated_ips.json",
            'event_destinations': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-sesv2_event_destinations.json",
            'tags': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-sesv2_tags.json"
        }
    },
        'federal': {
            'region': 'us-east-1',
            'output_files': {
                'identities': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-sesv2_email_identities.json",
                'configuration_sets': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-sesv2_configuration_sets.json",
                'dedicated_ips': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-sesv2_dedicated_ips.json",
                'event_destinations': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-sesv2_event_destinations.json",
                'tags': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-sesv2_tags.json"
            }
        }
    }