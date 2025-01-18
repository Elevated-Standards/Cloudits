import requests
import json
from datetime import datetime
import os

# Constants
JC_API_KEY = os.getenv("JUMPCLOUD_API_KEY")
JC_URL = "https://api.jumpcloud.com/v2/policies/passwordpolicy"


