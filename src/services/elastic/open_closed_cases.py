import requests
import json
import utils.elastic_utils

# Configuration
INDEX_NAME = ".cases*"  # Default index for Elastic cases

def fetch_cases(status):
    """
    Fetch cases with the given status (open or closed).
    """
    try:
        # Construct the API URL for search
        api_url = f"{utils.elastic_utils.ELASTIC_BASE_URL}/_search"

        # Set headers with API key for authentication
        headers = {
            "Authorization": f"ApiKey {utils.elastic_utils.ELASTIC_API_KEY}",
            "Content-Type": "application/json"
        }

        # Search query for cases
        query = {
            "index": INDEX_NAME,
            "query": {
                "term": {
                    "cases.attributes.status.keyword": status
                }
            },
            "sort": [{"cases.attributes.created_at": {"order": "desc"}}]
        }

        # Send POST request
        response = requests.post(api_url, headers=headers, data=json.dumps(query))

        # Check response status
        if response.status_code == 200:
            # Parse and return JSON data
            cases = response.json()
            print(f"{status.capitalize()} cases fetched successfully!")
            return cases
        else:
            print(f"Failed to fetch {status} cases. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching {status} cases: {e}")
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
    # Fetch open cases
    open_cases = fetch_cases("open")
    if open_cases:
        save_to_file(open_cases, "open_cases.json")

    # Fetch closed cases
    closed_cases = fetch_cases("closed")
    if closed_cases:
        save_to_file(closed_cases, "closed_cases.json")
