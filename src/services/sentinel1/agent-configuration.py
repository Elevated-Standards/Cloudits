import requests
import json
import os
from datetime import datetime, timezone, timedelta
import schedule
import time
from utils.s1_utils import S1_API_TOKEN, S1_URL


# Directory to save JSON files
OUTPUT_DIR = "sentinelone_agent_configs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_agent_configs():
    headers = {
        "Authorization": f"APIToken {S1_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(S1_URL, headers=headers)
    if response.status_code == 200:
        agents = response.json().get('data', [])
        return agents
    else:
        print("Failed to fetch agent configurations, Status Code:", response.status_code)
        return []

def save_to_json(agents):
    file_name = datetime.now().strftime('%Y-%m-%d') + "-sentinelone-agent-configs.json"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(file_path, 'w') as file:
        json.dump(agents, file, indent=4)
    print(f"Agent configurations saved to {file_path}")

def monthly_job():
    print("Fetching SentinelOne agent configurations...")
    agents = fetch_agent_configs()
    if agents:
        save_to_json(agents)

# Schedule the job every month
schedule.every().month.do(monthly_job)

# Main loop to run the scheduled tasks
print("Scheduler started...")
try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute
except KeyboardInterrupt:
    print("Scheduler stopped manually.")
