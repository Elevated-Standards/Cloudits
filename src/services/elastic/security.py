import requests
import json
import utils.elastic_utils


def fetch_users():
    """
    Fetch all users and their associated roles from Elasticsearch.
    """
    try:
        # Construct the API URL for users
        api_url = f"{utils.elastic_utils.ELASTIC_BASE_URL}/_security/user"

        # Set headers with API key for authentication
        headers = {
            "Authorization": f"ApiKey {utils.elastic_utils.ELASTIC_API_KEY}"
        }

        # Send GET request
        response = requests.get(api_url, headers=headers)

        # Check response status
        if response.status_code == 200:
            # Parse and return JSON data
            users = response.json()
            print("Users fetched successfully!")
            return users
        else:
            print(f"Failed to fetch users. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def fetch_roles():
    """
    Fetch all role definitions from Elasticsearch.
    """
    try:
        # Construct the API URL for roles
        api_url = f"{utils.elastic_utils.ELASTIC_BASE_URL}/_security/role"

        # Set headers with API key for authentication
        headers = {
            "Authorization": f"ApiKey {utils.elastic_utils.ELASTIC_API_KEY}"
        }

        # Send GET request
        response = requests.get(api_url, headers=headers)

        # Check response status
        if response.status_code == 200:
            # Parse and return JSON data
            roles = response.json()
            print("Roles fetched successfully!")
            return roles
        else:
            print(f"Failed to fetch roles. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
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
    # Fetch users
    users = fetch_users()
    if users:
        save_to_file(users, "users.json")

    # Fetch roles
    roles = fetch_roles()
    if roles:
        save_to_file(roles, "roles.json")

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