import os
import datetime
import json
import boto3
from botocore.exceptions import ClientError
from credentials.aws import get_aws_credentials

# Define current year and month for directory paths
YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
DAY = datetime.datetime.now().day
START_DATE = (datetime.datetime.utcnow() - datetime.timedelta(days=31)).isoformat()  # 31 days ago
END_DATE = datetime.datetime.utcnow().isoformat()  # current time

environments = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            'functions': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-lambda_functions.json",
            'environment_variables': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-lambda_environment_variables.json",
            'execution_roles': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-lambda_execution_roles.json",
            'function_policies': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-lambda_function_policies.json",
            'event_source_mappings': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-lambda_event_source_mappings.json",
            'tags': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{MONTH}-{DAY}-lambda_tags.json"
        }
    },
    'federal': {
        'region': 'us-west-2',
        'output_files': {
            'functions': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-lambda_functions.json",
            'environment_variables': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-lambda_environment_variables.json",
            'execution_roles': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-lambda_execution_roles.json",
            'function_policies': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-lambda_function_policies.json",
            'event_source_mappings': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-lambda_event_source_mappings.json",
            'tags': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}-lambda_tags.json"
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

def fetch_lambda_functions(client, output_file):
    paginator = client.get_paginator('list_functions')
    functions = []
    for page in paginator.paginate():
        functions.extend(page['Functions'])
    with open(output_file, 'w') as f:
        json.dump(functions, f, indent=4)
    return functions

def fetch_environment_variables(client, function_name):
    try:
        response = client.get_function_configuration(FunctionName=function_name)
        return response.get('Environment', {}).get('Variables', {})
    except ClientError as e:
        return {'Error': str(e)}

def fetch_execution_role(client, function_name):
    try:
        response = client.get_function_configuration(FunctionName=function_name)
        return response.get('Role')
    except ClientError as e:
        return {'Error': str(e)}

def fetch_function_policies(client, function_name):
    try:
        response = client.get_policy(FunctionName=function_name)
        return response.get('Policy')
    except ClientError as e:
        return {'Error': str(e)}

def fetch_event_source_mappings(client, function_name):
    try:
        response = client.list_event_source_mappings(FunctionName=function_name)
        return response.get('EventSourceMappings', [])
    except ClientError as e:
        return {'Error': str(e)}

def fetch_lambda_tags(client, function_arn):
    try:
        response = client.list_tags(Resource=function_arn)
        return response.get('Tags', {})
    except ClientError as e:
        return {'Error': str(e)}

def main():
    for env_name, config in environments.items():
        aws_creds = get_aws_credentials(env_name)
        if not aws_creds:
            print(f"Skipping environment '{env_name}' due to credential issues.")
            continue

        # Create Boto3 Lambda client
        lambda_client = create_boto3_client('lambda', config['region'], aws_creds)

        # Ensure directories exist for output files
        for file_path in config['output_files'].values():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Fetch all Lambda functions
        functions = fetch_lambda_functions(lambda_client, config['output_files']['functions'])

        env_vars_data, execution_roles_data, policies_data, event_source_data, tags_data = [], [], [], [], []

        for function in functions:
            function_name = function['FunctionName']
            function_arn = function['FunctionArn']

            env_vars_data.append({
                'FunctionName': function_name,
                'EnvironmentVariables': fetch_environment_variables(lambda_client, function_name)
            })
            execution_roles_data.append({
                'FunctionName': function_name,
                'ExecutionRole': fetch_execution_role(lambda_client, function_name)
            })
            policies_data.append({
                'FunctionName': function_name,
                'Policy': fetch_function_policies(lambda_client, function_name)
            })
            event_source_data.append({
                'FunctionName': function_name,
                'EventSourceMappings': fetch_event_source_mappings(lambda_client, function_name)
            })
            tags_data.append({
                'FunctionArn': function_arn,
                'Tags': fetch_lambda_tags(lambda_client, function_arn)
            })

        # Write each collected evidence to its respective output file
        with open(config['output_files']['environment_variables'], 'w') as f:
            json.dump(env_vars_data, f, indent=4)
        with open(config['output_files']['execution_roles'], 'w') as f:
            json.dump(execution_roles_data, f, indent=4)
        with open(config['output_files']['function_policies'], 'w') as f:
            json.dump(policies_data, f, indent=4)
        with open(config['output_files']['event_source_mappings'], 'w') as f:
            json.dump(event_source_data, f, indent=4)
        with open(config['output_files']['tags'], 'w') as f:
            json.dump(tags_data, f, indent=4)

    print("AWS Lambda configuration evidence collection completed for both environments.")

if __name__ == "__main__":
    main()
