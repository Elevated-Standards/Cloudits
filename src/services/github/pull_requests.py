import requests
import json
import os
import csv
import jwt  # Requires 'pyjwt' package
import time
import base64
from datetime import datetime, timedelta

# GitHub App Credentials (Environment Variables from GitHub Actions)
GITHUB_APP_ID = os.getenv("SECURITY_GITHUB_APP_ID")
GITHUB_APP_PRIVATE_KEY_BASE64 = os.getenv("SECURITY_GITHUB_APP_KEY")  # Base64-encoded
GITHUB_INSTALLATION_ID = os.getenv("SECURITY_GITHUB_INSTALLATION_ID")
GITHUB_ORG = ""  # Replace with your GitHub organization
GITHUB_REPOS = ["-ios", "-web-app", "-android"]  # Repositories to scan

# Decode Base64 private key
GITHUB_APP_PRIVATE_KEY = None
if GITHUB_APP_PRIVATE_KEY_BASE64:
    try:
        GITHUB_APP_PRIVATE_KEY = base64.b64decode(GITHUB_APP_PRIVATE_KEY_BASE64).decode("utf-8")
    except Exception as e:
        raise ValueError(f"❌ Failed to decode private key: {e}")
else:
    raise ValueError("❌ SECURITY_GITHUB_APP_KEY is missing!")

# Define lookback period (in days)
LOOKBACK_DAYS = 190
end_date = datetime.now()
start_date = end_date - timedelta(days=LOOKBACK_DAYS)
start_date_str = start_date.strftime('%Y-%m-%d')

# Output directory for storing evidence
OUTPUT_DIR = "evidence-artifacts/github/pull_requests/{YEAR}/{MONTH}/{END_DATE}"
GITHUB_API_URL = "https://api.github.com"

def get_github_app_token():
    """Generates a short-lived installation token for the GitHub App."""
    
    try:
        # Debugging: Show first few characters of secrets safely
        print(f"App ID: {GITHUB_APP_ID[:4] if GITHUB_APP_ID else 'None'}")
        print(f"Installation ID: {GITHUB_INSTALLATION_ID[:4] if GITHUB_INSTALLATION_ID else 'None'}")
        print(f"Private key length: {len(GITHUB_APP_PRIVATE_KEY) if GITHUB_APP_PRIVATE_KEY else 0}")

        # Ensure private key is in correct format
        if not GITHUB_APP_PRIVATE_KEY or not GITHUB_APP_PRIVATE_KEY.startswith('-----BEGIN RSA PRIVATE KEY-----'):
            raise ValueError("Private key appears to be malformed or missing.")

        # Create JWT token
        now = int(time.time())
        payload = {
            "iat": now,
            "exp": now + (10 * 60),
            "iss": GITHUB_APP_ID
        }
        jwt_token = jwt.encode(payload, GITHUB_APP_PRIVATE_KEY, algorithm="RS256")

        # Debugging: Show first few characters of JWT token
        print(f"Generated JWT token starts with: {jwt_token[:20]}...")

        # Get installation token
        url = f"https://api.github.com/app/installations/{GITHUB_INSTALLATION_ID}/access_tokens"
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.post(url, headers=headers)

        if response.status_code == 201:
            return response.json().get("token")
        else:
            print(f"GitHub API Response: {response.text}")
            raise Exception(f"Failed to get installation token: {response.status_code}")
            
    except Exception as e:
        print(f"ERROR in get_github_app_token: {str(e)}")
        raise

def fetch_pull_requests(repo_name, state="all"):
    """Fetch pull requests from GitHub API for a given repository and filter by created_at date."""
    url = f"{GITHUB_API_URL}/repos/{GITHUB_ORG}/{repo_name}/pulls"
    headers = {
        "Authorization": f"token {get_github_app_token()}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    params = {
        "state": state,
        "per_page": 100
    }
    pull_requests = []

    print(f"Fetching PRs from {repo_name}...")

    while url:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            filtered_prs = [
                pr for pr in data
                if pr.get("created_at") and pr["created_at"] >= start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
            ]

            print(f"Fetched {len(data)} PRs, {len(filtered_prs)} match the last {LOOKBACK_DAYS} days filter.")

            pull_requests.extend(filtered_prs)

            # Check if there is a next page (GitHub API pagination)
            url = response.links.get('next', {}).get('url')
        else:
            print(f"Failed to fetch PRs for {repo_name}: {response.status_code}, {response.text}")
            break

    cleaned_prs = clean_pull_requests(pull_requests)
    print(f"Final count after cleaning: {len(cleaned_prs)} PRs for {repo_name}")
    return cleaned_prs

def clean_pull_requests(pull_requests):
    """Clean pull request data and remove unnecessary fields."""
    cleaned_prs = []
    
    for pr in pull_requests:
        cleaned_pr = {
            "id": pr.get("id"),
            "number": pr.get("number"),
            "title": pr.get("title"),
            "description": (pr.get("body") or "").replace("\n", " "),
            "state": pr.get("state"),
            "created_at": pr.get("created_at"),
            "updated_at": pr.get("updated_at"),
            "merged_at": pr.get("merged_at"),
            "user": pr.get("user", {}).get("login", "Unknown"),
            "assignees": ", ".join([a["login"] for a in pr.get("assignees", [])]),
            "labels": ", ".join([label["name"] for label in pr.get("labels", [])]),
            "base_branch": pr.get("base", {}).get("ref", ""),
            "head_branch": pr.get("head", {}).get("ref", ""),
            "url": pr.get("html_url")
        }
        cleaned_prs.append(cleaned_pr)
    
    return cleaned_prs

def save_to_json(repo_name, pull_requests):
    """Save pull request data to a JSON file."""
    if not pull_requests:
        print(f"No PRs to save for {repo_name}.")
        return

    formatted_output_dir = OUTPUT_DIR.format(
        YEAR=end_date.strftime('%Y'),
        MONTH=end_date.strftime('%m'),
        END_DATE=end_date.strftime('%Y-%m-%d')
    )

    json_file_path = f"{formatted_output_dir}/{repo_name}-pull-requests.json"
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

    with open(json_file_path, 'w') as file:
        json.dump(pull_requests, file, indent=4)

    print(f"Saved {len(pull_requests)} PRs for {repo_name} to {json_file_path}")

def save_to_csv(repo_name, pull_requests):
    """Save pull request data to a CSV file."""
    if not pull_requests:
        print(f"No PRs to save for {repo_name}.")
        return

    formatted_output_dir = OUTPUT_DIR.format(
        YEAR=end_date.strftime('%Y'),
        MONTH=end_date.strftime('%m'),
        END_DATE=end_date.strftime('%Y-%m-%d')
    )

    csv_file_path = f"{formatted_output_dir}/{repo_name}-pull-requests.csv"
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

    headers = [
        "id", "number", "title", "description", "state",
        "created_at", "updated_at", "merged_at",
        "user", "assignees", "labels", "base_branch", "head_branch", "url"
    ]

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        for pr in pull_requests:
            writer.writerow(pr)

    print(f"Saved {len(pull_requests)} PRs for {repo_name} to {csv_file_path}")

def main():
    """Main function to fetch and save pull requests from multiple repositories."""
    for repo in GITHUB_REPOS:
        print(f"Fetching PRs for {repo} (last {LOOKBACK_DAYS} days)...")
        pull_requests = fetch_pull_requests(repo, state="all")
        save_to_json(repo, pull_requests)
        save_to_csv(repo, pull_requests)

if __name__ == "__main__":
    main()
