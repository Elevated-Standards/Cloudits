import requests
import json
import os
import sys
import csv
from datetime import datetime, timedelta

# Ensure 'src' is in Python's module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils.jira_utils import ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN

# Define lookback period
LOOKBACK_DAYS = 31
end_date = datetime.now()
start_date = end_date - timedelta(days=LOOKBACK_DAYS)

# Format date for JQL
start_date_str = start_date.strftime('%Y-%m-%d')

# Directory paths and project keys
PROJECTS = {
    "CORP_DEV": {
        "project_keys": ["<PLACEHOLDER>", "<PLACEHOLDER>"],  
        "output_dir": "evidence-artifacts/system/jira/commercial/completed_tickets/corp-dev/{YEAR}/{MONTH}/{END_DATE}"
    },
    "CORP_DEVOPS": {
        "project_keys": ["<PLACEHOLDER>", "<PLACEHOLDER>"],  
        "output_dir": "evidence-artifacts/system/jira/commercial/completed_tickets/corp-devops/{YEAR}/{MONTH}/{END_DATE}"
    },
    "FED_DEV": {
        "project_keys": ["<PLACEHOLDER>"],  
        "output_dir": "evidence-artifacts/system/jira/federal/completed_tickets/fed-dev/{YEAR}/{MONTH}/{END_DATE}"
    },
    "FED_DEVOPS": {
        "project_keys": ["<PLACEHOLDER>"],  
        "output_dir": "evidence-artifacts/system/jira/federal/completed_tickets/fed-devops/{YEAR}/{MONTH}/{END_DATE}"
    }
}

# Jira fields to retrieve (excluding avatar fields)
JIRA_FIELDS = [
    "id", "key", "summary", "description",
    "reporter", "assignee", "status", "created", "updated", "resolutiondate",
    "priority", "labels", "fixVersions", "components", "issuetype"
]

def fetch_completed_tickets(project_key):
    """Fetch completed tickets from Jira within the defined lookback period."""
    url = "https://<PLACEHOLDER>.atlassian.net/rest/api/3/search"
    jql = f"project={project_key} AND status=Done AND resolutiondate >= '{start_date_str}'"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    auth = (ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN)
    params = {
        "jql": jql,
        "fields": ",".join(JIRA_FIELDS),
        "maxResults": 100  # Adjust as needed
    }

    response = requests.get(url, headers=headers, auth=auth, params=params)
    if response.status_code == 200:
        data = response.json()
        return clean_issues(data.get('issues', []))
    else:
        print(f"Failed to fetch tickets for project {project_key}: {response.status_code}, {response.text}")
        return []

def clean_issues(issues):
    """Remove unnecessary avatar fields from Jira response."""
    for issue in issues:
        if "fields" in issue:
            for field in ["reporter", "assignee"]:
                if field in issue["fields"] and isinstance(issue["fields"][field], dict):
                    issue["fields"][field].pop("avatarUrls", None)  # Remove avatars
    return issues

def save_to_json(project_key, output_dir, issues):
    """Save ticket data to a JSON file."""
    if not issues:
        print(f"No completed tickets to save for project {project_key}.")
        return

    formatted_output_dir = output_dir.format(
        YEAR=end_date.strftime('%Y'),
        MONTH=end_date.strftime('%m'),
        END_DATE=end_date.strftime('%Y-%m-%d')
    )
    json_file_path = f"{formatted_output_dir}.json"

    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

    with open(json_file_path, 'w') as file:
        json.dump(issues, file, indent=4)
    
    print(f"Saved {len(issues)} completed tickets for {project_key} to {json_file_path}")

def save_to_csv(project_key, output_dir, issues):
    """Save ticket data to a CSV file."""
    if not issues:
        print(f"No completed tickets to save for project {project_key}.")
        return

    formatted_output_dir = output_dir.format(
        YEAR=end_date.strftime('%Y'),
        MONTH=end_date.strftime('%m'),
        END_DATE=end_date.strftime('%Y-%m-%d')
    )
    csv_file_path = f"{formatted_output_dir}.csv"

    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

    # Define CSV headers
    headers = [
        "id", "key", "summary", "description",
        "reporter", "assignee", "status", "created", "updated", "resolutiondate",
        "priority", "labels", "fixVersions", "components", "issuetype"
    ]

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        for issue in issues:
            row = {
                "id": issue.get("id"),
                "key": issue.get("key"),
                "summary": issue["fields"].get("summary", ""),
                "description": issue["fields"].get("description", ""),
                "reporter": issue["fields"].get("reporter", {}).get("displayName", ""),
                "assignee": issue["fields"].get("assignee", {}).get("displayName", "") if issue["fields"].get("assignee") else "Unassigned",
                "status": issue["fields"].get("status", {}).get("name", ""),
                "created": issue["fields"].get("created", ""),
                "updated": issue["fields"].get("updated", ""),
                "resolutiondate": issue["fields"].get("resolutiondate", ""),
                "priority": issue["fields"].get("priority", {}).get("name", ""),
                "labels": ", ".join(issue["fields"].get("labels", [])),
                "fixVersions": ", ".join(fv["name"] for fv in issue["fields"].get("fixVersions", [])),
                "components": ", ".join(c["name"] for c in issue["fields"].get("components", [])),
                "issuetype": issue["fields"].get("issuetype", {}).get("name", ""),
            }
            writer.writerow(row)

    print(f"Saved {len(issues)} completed tickets for {project_key} to {csv_file_path}")

def main():
    """Main function to fetch and save completed Jira tickets."""
    for project_info in PROJECTS.values():
        for project_key in project_info["project_keys"]:  
            output_dir = project_info["output_dir"]
            print(f"Fetching completed tickets for project {project_key} (last {LOOKBACK_DAYS} days)...")
            issues = fetch_completed_tickets(project_key)
            save_to_json(project_key, output_dir, issues)
            save_to_csv(project_key, output_dir, issues)

if __name__ == "__main__":
    main()





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