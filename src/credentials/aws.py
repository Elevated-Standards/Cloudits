# src/credentials/aws.py

import os

def get_aws_credentials(environment):
    """
    Fetch AWS credentials securely from environment variables based on the specified environment.
    Supports 'commercial' and 'federal' configurations.

    Args:
        environment (str): The environment for which credentials are required ('commercial' or 'federal').

    Returns:
        dict: A dictionary containing 'access_key', 'secret_key', and 'region' for the specified environment.
              Returns None if credentials are missing or the environment is invalid.
    """
    credentials = {
        'commercial': {
            'access_key': os.getenv('AUTOMATION_AWS_ACCESS_KEY_ID'),
            'secret_key': os.getenv('AUTOMATION_AWS_SECRET_ACCESS_KEY'),
            'region': 'us-east-1'
        },
        'federal': {
            'access_key': os.getenv('FEDERAL_AUTOMATION_AWS_ACCESS_KEY_ID'),
            'secret_key': os.getenv('FEDERAL_AUTOMATION_AWS_SECRET_ACCESS_KEY'),
            'region': 'us-west-2'
        }
    }

    # Fetch credentials for the specified environment
    creds = credentials.get(environment)

    if not creds:
        print(f"Error: Invalid environment '{environment}' specified.")
        return None

    # Validate that all required credentials are available
    if not creds['access_key'] or not creds['secret_key']:
        print(f"Error: Missing AWS credentials for the '{environment}' environment.")
        return None

    return creds
