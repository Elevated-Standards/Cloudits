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
            # ACM Files
            'certificates': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-acm_certificates.json",
            'certificate_details': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-acm_certificate_details.json",
            'tags': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-acm_tags.json",
            'renewal_status': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-acm_renewal_status.json",
            # KMS Files
            'keys': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-kms_keys.json",
            'key_policies': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-kms_key_policies.json",
            'grants': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-kms_grants.json",
            'kms_tags': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-kms_tags.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            # ACM Files
            'certificates': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-acm_certificates.json",
            'certificate_details': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-acm_certificate_details.json",
            'tags': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-acm_tags.json",
            'renewal_status': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-acm_renewal_status.json",
            # KMS Files
            'keys': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-kms_keys.json",
            'key_policies': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-kms_key_policies.json",
            'grants': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-kms_grants.json",
            'kms_tags': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{END_DATE}-kms_tags.json"
        }
    }
}