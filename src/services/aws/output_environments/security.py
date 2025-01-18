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
            # GuardDuty Files
            'detectors': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_detectors.json",
            'members': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_members.json",
            'ip_sets': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_ip_sets.json",
            'publishing_destinations': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_publishing_destinations.json",
            'coverage': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_coverage.json",
            'malware_scan_settings': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_malware_scan_settings.json",
            'organization_configuration': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_organization_configuration.json",
            'malware_scans': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-guardduty_malware_scans.json",
            # IAM Files
            'users': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-iam_users.json",
            'roles': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-iam_roles.json",
            'policies': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-iam_policies.json",
            'permissions_boundaries': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-iam_permissions_boundaries.json",
            'mfa_devices': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-iam_mfa_devices.json",
            'access_keys': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-iam_access_keys.json",
            'tags': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-iam_tags.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            # GuardDuty Files
            'detectors': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_detectors.json",
            'members': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_members.json",
            'ip_sets': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_ip_sets.json",
            'publishing_destinations': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_publishing_destinations.json",
            'coverage': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_coverage.json",
            'malware_scan_settings': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_malware_scan_settings.json",
            'organization_configuration': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_organization_configuration.json",
            'malware_scans': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-guardduty_malware_scans.json",
            # IAM Files
            'users': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-iam_users.json",
            'roles': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-iam_roles.json",
            'policies': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-iam_policies.json",
            'permissions_boundaries': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-iam_permissions_boundaries.json",
            'mfa_devices': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-iam_mfa_devices.json",
            'access_keys': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-iam_access_keys.json",
            'tags': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}-iam_tags.json"
        }
    }
}
