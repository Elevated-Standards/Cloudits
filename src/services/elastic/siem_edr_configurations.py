import requests
import json
import utils.elastic_utils

# Configuration
INDEX_NAME = "auditbeat-*"  # Replace with your audit logs index pattern

def fetch_siem_edr_config_changes():
    """
    Fetch changes made to Elastic SIEM/EDR configurations from Elasticsearch.
    """
    try:
        # Construct the API URL for search
        api_url = f"{utils.elastic_utils.ELASTIC_BASE_URL}/_search"

        # Set headers with API key for authentication
        headers = {
            "Authorization": f"ApiKey {utils.elastic_utils.ELASTIC_API_KEY}",
            "Content-Type": "application/json"
        }

        # Search query for SIEM/EDR configuration changes
        query = {
            "index": INDEX_NAME,
            "query": {
                "bool": {
                    "must": [
                        {"match": {"event.category": "configuration"}},
                        {"match": {"event.action": "change"}},
                        {"match": {"event.module": "security"}}
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
            print("SIEM/EDR configuration change logs fetched successfully!")
            return logs
        else:
            print(f"Failed to fetch configuration change logs. Status Code: {response.status_code}")
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
        print(f"Configuration change logs saved to {filename}")
    except Exception as e:
        print(f"Failed to save data to file: {e}")

# Main execution
if __name__ == "__main__":
    config_change_logs = fetch_siem_edr_config_changes()
    if config_change_logs:
        save_to_file(config_change_logs, "siem_edr_config_changes.json")
