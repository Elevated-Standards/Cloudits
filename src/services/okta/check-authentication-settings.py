import os
import requests
import json
from datetime import datetime, timezone, timedelta
from utils.okta_utils import OKTA_DOMAIN, OKTA_API_TOKEN


# Create the output directory if it doesn't exist
output_dir = f"lists/{datetime.now().year}/okta"
os.makedirs(output_dir, exist_ok=True)

# Set the output file path
output_file = os.path.join(output_dir, f"{datetime.now().year}.okta-authentication-settings.json")

# Fetch the list of policies
response = requests.get(f"https://{OKTA_DOMAIN}/api/v1/policies",
                        headers={"Authorization": f"SSWS {OKTA_API_TOKEN}", "Accept": "application/json"})
policies = response.json()

# Initialize the JSON array for output
output_data = []

# Loop through each policy and fetch authentication settings
for policy in policies:
    policy_id = policy['id']
    policy_name = policy['name']
    policy_type = policy['type']



    # Fetch policy rules
    rules_response = requests.get(f"https://{OKTA_DOMAIN}/api/v1/policies/{policy_id}/rules",
                                  headers={"Authorization": f"SSWS {OKTA_API_TOKEN}", "Accept": "application/json"})
    rules = rules_response.json()

    # Create a JSON object for the policy with its rules
    policy_with_rules = {
        "id": policy_id,
        "name": policy_name,
        "type": policy_type,
        "rules": rules
    }
    output_data.append(policy_with_rules)

# Save the policies to the output file
with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=4)

print(f"Authentication settings for policies have been saved to {output_file}")

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