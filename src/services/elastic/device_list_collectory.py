import requests
import json
import utils.elastic_utils



def fetch_elastic_agents():
    """
    Fetch a list of devices running Elastic Agent.
    """
    try:
        # Construct the API URL for Elastic Agent information
        api_url = f"{utils.elastic_utils.ELASTIC_BASE_URL}/_fleet/agents"

        # Set headers with API key for authentication
        headers = {
            "Authorization": f"ApiKey {utils.elastic_utils.ELASTIC_API_KEY}"
        }

        # Send GET request
        response = requests.get(api_url, headers=headers)

        # Check response status
        if response.status_code == 200:
            # Parse and return JSON data
            agents = response.json()
            print("Elastic Agents fetched successfully!")
            return agents
        else:
            print(f"Failed to fetch Elastic Agents. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_device_details(agents):
    """
    Extract details about devices running Elastic Agent.
    """
    device_list = []
    for agent in agents.get("items", []):
        device = {
            "id": agent.get("id"),
            "name": agent.get("local_metadata", {}).get("host", {}).get("name"),
            "os": agent.get("local_metadata", {}).get("os", {}).get("full"),
            "ip": agent.get("local_metadata", {}).get("host", {}).get("ip"),
            "status": agent.get("status"),
            "policy_id": agent.get("policy_id"),
        }
        device_list.append(device)
    return device_list

def save_to_file(data, filename):
    """
    Save JSON data to a file.
    """
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Device list saved to {filename}")
    except Exception as e:
        print(f"Failed to save data to file: {e}")

# Main execution
if __name__ == "__main__":
    # Fetch Elastic Agents
    agents_data = fetch_elastic_agents()
    if agents_data:
        # Extract device details
        device_details = extract_device_details(agents_data)
        save_to_file(device_details, "elastic_agents.json")
