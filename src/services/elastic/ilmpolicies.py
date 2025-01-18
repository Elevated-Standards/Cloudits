import requests
import json
import utils.elastic_utils


def fetch_ilm_policies():
    """
    Fetch all ILM policies from Elasticsearch.
    """
    try:
        # Construct the API URL for ILM policies
        api_url = f"{utils.elastic_utils.ELASTIC_BASE_URL}/_ilm/policy"

        # Set headers with API key for authentication
        headers = {
            "Authorization": f"ApiKey {utils.elastic_utils.ELASTIC_API_KEY}"
        }

        # Send GET request
        response = requests.get(api_url, headers=headers)

        # Check response status
        if response.status_code == 200:
            # Parse and return JSON data
            ilm_policies = response.json()
            print("ILM policies fetched successfully!")
            return ilm_policies
        else:
            print(f"Failed to fetch ILM policies. Status Code: {response.status_code}")
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
        print(f"ILM policies saved to {filename}")
    except Exception as e:
        print(f"Failed to save data to file: {e}")

# Main execution
if __name__ == "__main__":
    ilm_policies = fetch_ilm_policies()
    if ilm_policies:
        save_to_file(ilm_policies, "ilm_policies.json")
