import os
import datetime
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3
from botocore.exceptions import ClientError
from credentials.aws import get_aws_credentials

YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
DAY = datetime.datetime.now().day

# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            'elbv2_load_balancers': f"{BASE_DIR}/systems/aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-elbv2_load_balancers.json",
            'elbv2_listeners': f"{BASE_DIR}/systems/aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-elbv2_listeners.json",
            'elbv2_listener_rules': f"{BASE_DIR}/systems/aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-elbv2_listener_rules.json",
            'elbv2_target_groups': f"{BASE_DIR}/systems/aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-elbv2_target_groups.json",
            'elbv2_tags': f"{BASE_DIR}/systems/aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-elbv2_tags.json",
            'meshes': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_meshes.json",
            'virtual_services': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_services.json",
            'virtual_routers': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_routers.json",
            'virtual_nodes': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_nodes.json",
            'virtual_gateways': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_gateways.json",
            'routes': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_routes.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            'elbv2_load_balancers': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-elbv2_load_balancers.json",
            'elbv2_listeners': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-elbv2_listeners.json",
            'elbv2_listener_rules': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-elbv2_listener_rules.json",
            'elbv2_target_groups': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-elbv2_target_groups.json",
            'elbv2_tags': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-elbv2_tags.json",
            'meshes': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_meshes.json",
            'virtual_services': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_services.json",
            'virtual_routers': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_routers.json",
            'virtual_nodes': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_nodes.json",
            'virtual_gateways': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_gateways.json",
            'routes': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_routes.json"
        }
    }
}

def create_boto3_client(service, region, aws_creds):
    return boto3.client(
        service,
        region_name=region,
        aws_access_key_id=aws_creds['access_key'],
        aws_secret_access_key=aws_creds['secret_key']
    )

def fetch_and_save_data(client_method, output_file, **kwargs):
    try:
        response = client_method(**kwargs)
        with open(output_file, 'w') as f:
            json.dump(response, f, indent=4)
        return response
    except ClientError as e:
        print(f"Error fetching data: {str(e)}")
        return {}

def main():
    for env_name, config in environments.items():
        aws_creds = get_aws_credentials(env_name)
        if not aws_creds:
            print(f"Skipping environment '{env_name}' due to credential issues.")
            continue

        elbv2_client = create_boto3_client('elbv2', config['region'], aws_creds)
        appmesh_client = create_boto3_client('appmesh', config['region'], aws_creds)

        # Create necessary directories
        for file_path in config['output_files'].values():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        tasks = [
            (fetch_and_save_data, elbv2_client.describe_load_balancers, config['output_files']['elbv2_load_balancers']),
            (fetch_and_save_data, elbv2_client.describe_target_groups, config['output_files']['elbv2_target_groups']),
            (fetch_and_save_data, appmesh_client.list_meshes, config['output_files']['meshes']),
        ]

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(task[0], task[1], task[2]): task[2] for task in tasks}

            for future in as_completed(futures):
                output_file = futures[future]
                try:
                    future.result()
                    print(f"Task for file '{output_file}' completed successfully.")
                except Exception as e:
                    print(f"Task for file '{output_file}' failed with error: {e}")

    print("Evidence collection completed.")

if __name__ == "__main__":
    main()
