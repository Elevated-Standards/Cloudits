import requests
import json
import os
import csv
import jwt  # Requires 'pyjwt' package
import time
from datetime import datetime, timedelta, UTC

# GitHub App Credentials (Set these in your Codespace environment)
GITHUB_APP_ID = os.getenv("SECURITY_GITHUB_APP_ID")
GITHUB_APP_PRIVATE_KEY = os.getenv("SECURITY_GITHUB_APP_KEY")
GITHUB_INSTALLATION_ID = os.getenv("SECURITY_GITHUB_INSTALLATION_ID")
GITHUB_ORG = ""
GITHUB_REPOS = ["-ios", "-web-app", "-android"]

# Define the lookback period in days
LOOKBACK_DAYS = 90
end_date = datetime.now(UTC)
start_date = end_date - timedelta(days=LOOKBACK_DAYS)

# Output directory for storing evidence
OUTPUT_DIR = "evidence-artifacts/github/security/{YEAR}/{MONTH}/{END_DATE}"
GITHUB_API_URL = "https://api.github.com"

def get_github_app_token():
    """Generates a short-lived installation token for the GitHub App."""
    
    missing_vars = [var for var, env in [
        ("SECURITY_GITHUB_APP_ID", GITHUB_APP_ID),
        ("SECURITY_GITHUB_APP_KEY", GITHUB_APP_PRIVATE_KEY),
        ("SECURITY_GITHUB_INSTALLATION_ID", GITHUB_INSTALLATION_ID)
    ] if not env]

    if missing_vars:
        raise ValueError(
            f"❌ ERROR: Missing required GitHub App credentials: {', '.join(missing_vars)}"
        )

    now = int(time.time())
    payload = {"iat": now, "exp": now + (10 * 60), "iss": GITHUB_APP_ID}
    jwt_token = jwt.encode(payload, GITHUB_APP_PRIVATE_KEY, algorithm="RS256")

    url = f"{GITHUB_API_URL}/app/installations/{GITHUB_INSTALLATION_ID}/access_tokens"
    headers = {"Authorization": f"Bearer {jwt_token}", "Accept": "application/vnd.github.v3+json"}
    
    response = requests.post(url, headers=headers)
    if response.status_code == 201:
        return response.json().get("token")
    else:
        raise Exception(f"Failed to get installation token: {response.status_code}, {response.text}")

TOKEN = get_github_app_token()  # Retrieve once and reuse

def is_within_lookup_period(date_str):
    """Checks if a GitHub event date is within the defined lookup period."""
    if not date_str:
        return False
    event_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)  # Make event_date timezone-aware
    return start_date <= event_date <= end_date  # Now all dates are UTC-aware


def fetch_paginated_results(url, max_pages=10):
    """Fetch all paginated results from GitHub API with timeout and max page cap."""
    headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
    }
    results = []
    page_count = 0

    while url and page_count < max_pages:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = data if isinstance(data, list) else data.get("workflow_runs", [])

                if not items:
                    print(f"⚠️ Empty response at {url}, stopping pagination. Response: {response.json()}")
                    break


                results.extend(items)
                url = response.links.get("next", {}).get("url")
                page_count += 1
            else:
                print(f"❌ API request failed: {response.status_code} {response.text}")
                break
        except requests.exceptions.Timeout:
            print(f"⏳ Timeout on {url}, retrying...")
            time.sleep(5)  # Wait before retrying
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            break

    return results


def fetch_pull_request_reviews(repo_name):
    """Fetch pull request reviews within the lookup period."""
    pull_requests = fetch_paginated_results(f"{GITHUB_API_URL}/repos/{GITHUB_ORG}/{repo_name}/pulls?state=all&per_page=100")
    reviews = []

    for pr in pull_requests:
        pr_number = pr["number"]
        review_url = f"{GITHUB_API_URL}/repos/{GITHUB_ORG}/{repo_name}/pulls/{pr_number}/reviews"
        review_data = fetch_paginated_results(review_url)

        # 🚀 Log API response when no reviews exist
        if not review_data:
            print(f"⚠️ No reviews found for PR #{pr_number} in {repo_name}. Response: {review_data}")

        for review in review_data:
            if is_within_lookup_period(review.get("submitted_at")):
                reviews.append({
                    "repo": repo_name,
                    "pr_number": pr_number,
                    "pr_title": pr["title"],
                    "reviewer": review.get("user", {}).get("login", "Unknown"),
                    "state": review["state"],
                    "submitted_at": review["submitted_at"],
                    "url": pr["html_url"]
                })
    
    return reviews


def fetch_github_actions_runs(repo_name):
    """Fetch GitHub Actions workflow runs within the lookup period."""
    workflow_runs = fetch_paginated_results(f"{GITHUB_API_URL}/repos/{GITHUB_ORG}/{repo_name}/actions/runs?per_page=100")
    runs = [
        {
            "repo": repo_name,
            "workflow_id": run["workflow_id"],
            "run_id": run["id"],
            "status": run["status"],
            "conclusion": run["conclusion"],
            "created_at": run["created_at"],
            "updated_at": run["updated_at"],
            "event": run["event"],
            "actor": run.get("actor", {}).get("login", "Unknown"),
            "url": run["html_url"]
        }
        for run in workflow_runs if is_within_lookup_period(run.get("created_at"))
    ]

    return runs

def save_to_json(filename, data):
    """Save data to JSON file."""
    formatted_output_dir = OUTPUT_DIR.format(
        YEAR=end_date.strftime('%Y'),
        MONTH=end_date.strftime('%m'),
        END_DATE=end_date.strftime('%Y-%m-%d')
    )
    
    os.makedirs(formatted_output_dir, exist_ok=True)
    filepath = os.path.join(formatted_output_dir, f"{filename}.json")

    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

    print(f"📂 Saved {len(data)} records to {filepath}")

def save_to_csv(filename, data, headers):
    """Save data to CSV file."""
    formatted_output_dir = OUTPUT_DIR.format(
        YEAR=end_date.strftime('%Y'),
        MONTH=end_date.strftime('%m'),
        END_DATE=end_date.strftime('%Y-%m-%d')
    )

    os.makedirs(formatted_output_dir, exist_ok=True)
    filepath = os.path.join(formatted_output_dir, f"{filename}.csv")

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    print(f"📂 Saved {len(data)} records to {filepath}")

def main():
    """Main function to collect GitHub Actions security evidence within lookup period."""
    all_runs = []

    for repo in GITHUB_REPOS:
        print(f"🔍 Fetching Deployment & CI/CD Security Evidence for {repo} (Last {LOOKBACK_DAYS} days)...")
        runs = fetch_github_actions_runs(repo)
        print(f"✅ Found {len(runs)} runs for {repo}")
        all_runs.extend(runs)

    save_to_json("github_actions_runs", all_runs)
    save_to_csv("github_actions_runs", all_runs, ["repo", "workflow_id", "run_id", "status", "conclusion", "created_at", "updated_at", "event", "actor", "url"])

if __name__ == "__main__":
    main()

