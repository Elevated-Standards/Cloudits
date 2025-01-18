from utils.utils import *
from utils.aws_utils import *

# Fetch shared date information and base directory
date_info = get_current_date_info()
BASE_DIR = get_base_dir()
YEAR = date_info["year"]
MONTH = date_info["month"]
END_DATE = date_info["end_date"]

# AWS environment configurations
ENVIRONMENTS = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            'alarms': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_alarms.json",
            'metrics': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_metrics.json",
            'dashboards': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_dashboards.json",
            'log_groups': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_log_groups.json",
            'tags': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_tags.json",
            'trails': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_trails.json",
            'event_data_stores': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_event_data_stores.json",
            'insights': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_insights.json",
            'config_changes': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-config_changes.json",
            'cloudtrail_events': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_events.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            'alarms': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_alarms.json",
            'metrics': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_metrics.json",
            'dashboards': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_dashboards.json",
            'log_groups': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_log_groups.json",
            'tags': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudwatch_tags.json",
            'trails': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_trails.json",
            'event_data_stores': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_event_data_stores.json",
            'insights': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_insights.json",
            'config_changes': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-config_changes.json",
            'cloudtrail_events': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{END_DATE}-cloudtrail_events.json"
        }
    }
}
