# Purpose: Provide Evidence for AWS Automation Related Services.#
#################################################################
import os
import subprocess
import datetime
import json
import sys
from credentials.aws import get_aws_credentials


# Ensure the 'src' directory is in the Python module search path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Define toggles to enable or disable environments
enable_environments = {
    'commercial': True,  # Set to False to disable 'commercial'
    'federal': False      # Set to False to disable 'federal'
}

# Define current year and month for directory paths
YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
DAY = datetime.datetime.now().day
START_DATE = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=31)).isoformat()  # 31 days ago
END_DATE = datetime.datetime.now(datetime.timezone.utc).isoformat() 


# Base directory for evidence artifacts
BASE_DIR = os.path.join(os.getcwd(), "evidence-artifacts")

environments = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            'functions': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-lambda_functions.json",
            'environment_variables': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-lambda_environment_variables.json",
            'execution_roles': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-lambda_execution_roles.json",
            'function_policies': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-lambda_function_policies.json",
            'event_source_mappings': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-lambda_event_source_mappings.json",
            'tags': f"{BASE_DIR}/commercial/systems/aws/{YEAR}/{MONTH}/{END_DATE}-lambda_tags.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            'functions': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{MONTH}-lambda_functions.json",
            'environment_variables': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{MONTH}-lambda_environment_variables.json",
            'execution_roles': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{MONTH}-lambda_execution_roles.json",
            'function_policies': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{MONTH}-lambda_function_policies.json",
            'event_source_mappings': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{MONTH}-lambda_event_source_mappings.json",
            'tags': f"{BASE_DIR}/federal/systems/aws/{YEAR}/{MONTH}/{MONTH}-lambda_tags.json"
        }
    }
}

# Helper function to run AWS CLI commands
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return json.loads(result.stdout)

# Fetch all Lambda functions
def fetch_lambda_functions(config, output_file):
    aws_command = ['aws', 'lambda', 'list-functions', '--region', config['region'], '--output', 'json']
    functions_data = run_command(aws_command)
    with open(output_file, 'w') as f:
        json.dump(functions_data, f, indent=4)
    return functions_data['Functions']

# Fetch environment variables for each Lambda function
def fetch_environment_variables(config, function_name):
    aws_command = ['aws', 'lambda', 'get-function-configuration', '--function-name', function_name, '--region', config['region'], '--query', 'Environment.Variables', '--output', 'json']
    return run_command(aws_command)

# Fetch execution role for each Lambda function
def fetch_execution_role(config, function_name):
    aws_command = ['aws', 'lambda', 'get-function-configuration', '--function-name', function_name, '--region', config['region'], '--query', 'Role', '--output', 'json']
    return run_command(aws_command)

# Fetch function policies
def fetch_function_policies(config, function_name):
    aws_command = ['aws', 'lambda', 'get-policy', '--function-name', function_name, '--region', config['region'], '--output', 'json']
    return run_command(aws_command)

# Fetch event source mappings for each Lambda function
def fetch_event_source_mappings(config, function_name):
    aws_command = ['aws', 'lambda', 'list-event-source-mappings', '--function-name', function_name, '--region', config['region'], '--output', 'json']
    return run_command(aws_command)

# Fetch tags for a specific Lambda function
def fetch_lambda_tags(config, function_arn):
    aws_command = ['aws', 'lambda', 'list-tags', '--resource', function_arn, '--region', config['region'], '--output', 'json']
    return run_command(aws_command)

# Main function to execute each evidence collection task
def main():
    for env_name, config in environments.items():
        # Check if the environment is enabled
        if not enable_environments.get(env_name, False):
            print(f"Skipping environment '{env_name}' as it is disabled.")
            continue

        # Fetch AWS credentials for the current environment
        aws_creds = get_aws_credentials(env_name)
        if not aws_creds:
            print(f"Skipping environment '{env_name}' due to credential issues.")
            continue
        
        # Set AWS environment variables for subprocess commands
        os.environ['AWS_ACCESS_KEY_ID'] = aws_creds['access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_creds['secret_key']
        os.environ['AWS_DEFAULT_REGION'] = aws_creds['region']

        # Ensure directories exist for output files
        for file_path in config['output_files'].values():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)


        # Collect all Lambda functions and iterate through each
        functions = fetch_lambda_functions(config, config['output_files']['functions'])

        # Initialize empty lists to collect data for each function attribute
        env_vars_data, execution_roles_data, policies_data, event_source_data, tags_data = [], [], [], [], []

        for function in functions:
            function_name = function['FunctionName']
            function_arn = function['FunctionArn']

            # Collect and store each piece of evidence for the function
            env_vars_data.append({
                'FunctionName': function_name,
                'EnvironmentVariables': fetch_environment_variables(config, function_name)
            })
            execution_roles_data.append({
                'FunctionName': function_name,
                'ExecutionRole': fetch_execution_role(config, function_name)
            })
            policies_data.append({
                'FunctionName': function_name,
                'Policy': fetch_function_policies(config, function_name)
            })
            event_source_data.append({
                'FunctionName': function_name,
                'EventSourceMappings': fetch_event_source_mappings(config, function_name)
            })
            tags_data.append({
                'FunctionArn': function_arn,
                'Tags': fetch_lambda_tags(config, function_arn)
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
# Execute main function
if __name__ == "__main__":
    main()
