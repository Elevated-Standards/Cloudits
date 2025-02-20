import sys
import json
import os
import logging
import boto3
from datetime import datetime
from utils.aws_utils import get_required_parameters

# Load unified config.json
CONFIG_PATH = "/workspaces/Cloudits/utils/config.json"
try:
    with open(CONFIG_PATH, 'r') as config_file:
        config = json.load(config_file)
except Exception as e:
    print(f"Error loading configuration file: {e}")
    sys.exit(1)

# Configure logging
LOG_FILE_PATH = config["log_file_path"]
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler(LOG_FILE_PATH, mode='w'),
    logging.StreamHandler()
])
logger = logging.getLogger(__name__)

# Load constants from config.json
BASE_DIR = config["base_dir"]
ENVIRONMENTS = config["aws_environments"]
ROLES = config["aws_roles"]
EVIDENCE_COLLECTION_ENABLED = config["evidence_collection_enabled"]
SERVICE_CONFIG = config["services"]  # AWS services enable/disable

# Time-based values (dynamically generated)
YEAR = datetime.now().year
MONTH = datetime.now().month
END_DATE = datetime.now().strftime("%Y-%m-%d")

def assume_role(role_arn, session_name):
    """Assumes an AWS IAM role and returns credentials."""
    try:
        client = boto3.client('sts')
        response = client.assume_role(RoleArn=role_arn, RoleSessionName=session_name)
        return response['Credentials']
    except Exception as e:
        logger.error(f"Error assuming role {role_arn}: {e}")
        return None

def create_evidence(service, function, region, parameters=None, credentials=None, framework_mapping=None):
    """Calls the AWS service function and retrieves evidence."""
    try:
        client = boto3.client(
            service,
            region_name=region,
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

        method = getattr(client, function)
        response = method(**(parameters or {}))


        # Check if response is completely empty
        if not response or response in [[], {}]:
            logger.info(f"No data returned for {service} - {function} in {region}. Skipping evidence creation.")
            return None

        # Remove AWS metadata (like HTTPResponse)
        filtered_response = {k: v for k, v in response.items() if k != 'ResponseMetadata'}

        if not filtered_response:  # If the response contains only metadata
            logger.info(f"No meaningful data returned for {service} - {function} in {region}. Skipping evidence creation.")
            return None

        # Check for result_key from framework_mapping and ensure it isn't empty
        if framework_mapping:
            for item in framework_mapping:
                if item['service'] == service and item['function'] == function:
                    result_key = item.get('result_key', None)
                    if result_key and (result_key not in response or not response[result_key]):
                        logger.info(f"Empty result_key '{result_key}' for {service} - {function} in {region}. Skipping evidence creation.")
                        return None

        return response

    except Exception as e:
        logger.error(f"Error creating evidence for {service} - {function}: {e}")
        return None


def save_evidence(evidence, file_path):
    """Saves evidence JSON to file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(evidence, f, indent=4, default=str)
        logger.info(f"Evidence saved to {file_path}")
    except Exception as e:
        logger.error(f"Error saving evidence to {file_path}: {e}")

def main():
    """Main function that executes evidence collection."""
    if len(sys.argv) != 2 or sys.argv[1] not in ENVIRONMENTS:
        print("Usage: python refractor.py <environment>")
        sys.exit(1)

    environment = sys.argv[1]
    regions = ENVIRONMENTS[environment]['regions']

    try:
        with open('/workspaces/Cloudits/framework_mapping/aws_with_frameworks.json', 'r') as f:
            framework_mapping = json.load(f)
    except Exception as e:
        logger.error(f"Error loading framework mapping: {e}")
        sys.exit(1)

    for role_key, role_arn in ROLES.items():
        if not EVIDENCE_COLLECTION_ENABLED.get(role_key, False):
            logger.info(f"Skipping evidence collection for role: {role_key}")
            continue

        logger.info(f"Starting evidence collection for role: {role_key}")
        credentials = assume_role(role_arn, f'session-{role_key}')
        if not credentials:
            continue

        for region in regions:
            for item in framework_mapping:
                service = item.get('service')
                function = item.get('function')
                parameters = item.get('parameters', {})

                # Skip services that are disabled in config.json
                if not SERVICE_CONFIG.get(service, False):  # Check if service is enabled
                    logger.info(f"Skipping disabled service: {service}")
                    continue

                if not service or not function:
                    logger.warning(f"Skipping due to missing service or function: {item}")
                    continue

                try:
                    dynamic_params = get_required_parameters(service, function, region, credentials)
                    parameters = parameters or {}  # Ensure parameters is a dictionary
                    parameters.update(dynamic_params)
                    evidence = create_evidence(service, function, region, parameters, credentials, framework_mapping)

                    if evidence and evidence not in [[], {}]:
                        file_path = os.path.join(BASE_DIR, "systems", "aws", environment, role_key, region, str(YEAR), str(MONTH), END_DATE, f"{service}-{function}.json")
                        save_evidence(evidence, file_path)
                        logger.info(f"Evidence saved for {service} - {function} in {region}")
                    else:
                        logger.info(f"Skipping evidence creation for {service} - {function} in {region} due to empty response.")
                except Exception as e:
                    logger.error(f"Error processing {service} - {function} in {region}: {e}")

if __name__ == "__main__":
    main()
