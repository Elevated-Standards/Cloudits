import requests
import json
import utils.elastic_utils

# Configuration
INDEX_NAME = "logs-endpoint.events.*"  # Replace with your endpoint logs index pattern

def fetch_isolation_events():
    """
    Fetch endpoint isolation events from Elasticsearch.
    """
    try:
        # Construct the API URL for search
        api_url = f"{utils.elastic_utils.ELASTIC_BASE_URL}/_search"

        # Set headers with API key for authentication
        headers = {
            "Authorization": f"ApiKey {utils.elastic_utils.ELASTIC_API_KEY}",
            "Content-Type": "application/json"
        }

        # Search query for isolation events
        query = {
            "index": INDEX_NAME,
            "query": {
                "bool": {
                    "must": [
                        {"match": {"event.action": "isolate"}},
                        {"match": {"event.module": "endpoint"}}
                    ]
                }
            }
        }

        # Send POST request
        response = requests.post(api_url, headers=headers, data=json.dumps(query))

        # Check response status
        if response.status_code == 200:
            # Parse and return JSON data
            events = response.json()
            print("Endpoint isolation events fetched successfully!")
            return events
        else:
            print(f"Failed to fetch isolation events. Status Code: {response.status_code}")
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
        print(f"Isolation events saved to {filename}")
    except Exception as e:
        print(f"Failed to save data to file: {e}")

# Main execution
if __name__ == "__main__":
    isolation_events = fetch_isolation_events()
    if isolation_events:
        save_to_file(isolation_events, "isolation_events.json")
