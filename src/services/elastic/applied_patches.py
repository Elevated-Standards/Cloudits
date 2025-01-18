import requests
import json

# Configuration
ELASTIC_BASE_URL = "https://your-elastic-instance.com"  # Replace with your Elasticsearch URL
API_KEY = "your_api_key"  # Replace with your Elasticsearch API key
INDEX_NAME = "logs-system.updates.*"  # Replace with your system updates index pattern

def fetch_patch_logs():
    """
    Fetch logs of applied patches and updates from Elasticsearch.
    """
    try:
        # Construct the API URL for search
        api_url = f"{ELASTIC_BASE_URL}/_search"

        # Set headers with API key for authentication
        headers = {
            "Authorization": f"ApiKey {API_KEY}",
            "Content-Type": "application/json"
        }

        # Search query for patch and update logs
        query = {
            "index": INDEX_NAME,
            "query": {
                "bool": {
                    "must": [
                        {"match": {"event.category": "package"}},
                        {"terms": {"event.action": ["install", "update", "patch"]}}
                    ]
                }
            },
            "sort": [{"@timestamp": {"order": "desc"}}]
        }

        # Send POST request
        response = requests.post(api_url, headers=headers, data=json.dumps(query))

        # Check response status
        if response.status_code == 200:
            # Parse and return JSON data
            logs = response.json()
            print("Patch and update logs fetched successfully!")
            return logs
        else:
            print(f"Failed to fetch patch logs. Status Code: {response.status_code}")
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
        print(f"Patch logs saved to {filename}")
    except Exception as e:
        print(f"Failed to save data to file: {e}")

# Main execution
if __name__ == "__main__":
    patch_logs = fetch_patch_logs()
    if patch_logs:
        save_to_file(patch_logs, "patch_logs.json")
