import requests
import json
import utils.elastic_utils

def fetch_all_repositories():
    """
    Fetch all snapshot repositories from Elasticsearch.
    """
    try:
        # Construct the API URL for listing repositories
        api_url = f"{utils.elastic_utils.ELASTIC_BASE_URL}/_snapshot"

        # Set headers with API key for authentication
        headers = {
            "Authorization": f"ApiKey {utils.elastic_utils.ELASTIC_API_KEY}"
        }

        # Send GET request
        response = requests.get(api_url, headers=headers)

        # Check response status
        if response.status_code == 200:
            # Parse and return JSON data
            repositories = response.json()
            print("Fetched all snapshot repositories successfully!")
            return repositories
        else:
            print(f"Failed to fetch snapshot repositories. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def fetch_repository_configuration(repo_name):
    """
    Fetch the configuration for a specific snapshot repository.
    """
    try:
        # Construct the API URL for the repository
        api_url = f"{utils.elastic_utils.ELASTIC_BASE_URL}/_snapshot/{repo_name}"

        # Set headers with API key for authentication
        headers = {
            "Authorization": f"ApiKey {utils.elastic_utils.ELASTIC_API_KEY}"
        }

        # Send GET request
        response = requests.get(api_url, headers=headers)

        # Check response status
        if response.status_code == 200:
            # Parse and return JSON data
            config = response.json()
            print(f"Fetched configuration for repository: {repo_name}")
            return config
        else:
            print(f"Failed to fetch configuration for repository: {repo_name}. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred for repository {repo_name}: {e}")
        return None

def save_to_file(data, filename):
    """
    Save JSON data to a file.
    """
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Failed to save data to file: {e}")

# Main execution
if __name__ == "__main__":
    # Fetch all snapshot repositories
    repositories = fetch_all_repositories()

    if repositories:
        all_configs = {}
        for repo_name in repositories.keys():
            # Fetch the configuration for each repository
            config = fetch_repository_configuration(repo_name)
            if config:
                all_configs[repo_name] = config

        # Save all configurations to a file
        save_to_file(all_configs, "all_snapshot_configurations.json")


###############################################################
# Framework: 
# - SOC 2: CC#.#, CC#.#
# - ISO 27001: A.#.#
###############################################################
# Auditor 1 - <Placeholder> ID's: 
# - R-### - 
# - 
###############################################################
# Auditor 2 - <Placeholder> ID's: 
# - 
###############################################################