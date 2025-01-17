# src/credentials/aws.py

import os
import sys

def get_aws_credentials(environment):
    """
    Fetch AWS credentials directly from the environment variables.
    This assumes credentials are managed by `aws-actions/configure-aws-credentials`.

    Args:
        environment (str): The environment for which credentials are required ('commercial' or 'federal').

    Returns:
        dict: A dictionary containing 'access_key', 'secret_key', and 'region'.
    """
    # Define regions for each environment
    regions = {
        'commercial': 'us-east-1',
        'federal': 'us-east-1',
    }

    # Ensure the requested environment is valid
    if environment not in regions:
        print(f"Error: Invalid environment '{environment}' specified.")
        return None

    # Fetch credentials directly from environment variables
    credentials = {
        'access_key': os.getenv('AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'region': regions[environment],
    }

    # Check if credentials are missing
    if not credentials['access_key'] or not credentials['secret_key']:
        print(f"Error: Missing AWS credentials for the '{environment}' environment.")
        return None

    return credentials

if __name__ == "__main__":
    import sys

    # Ensure the script is called with the required environment argument
    if len(sys.argv) != 2:
        print("Usage: python aws.py <environment>")
        sys.exit(1)

    # Fetch and display credentials for the given environment
    env = sys.argv[1]
    credentials = get_aws_credentials(env)
    if credentials:
        print(f"Credentials for {env}: {credentials}")
