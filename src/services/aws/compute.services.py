# Purpose: Provide Evidence for AWS Compute Related Services.#
##############################################################
import os
import subprocess
import datetime, timezone, timedelta
import json
from utils.aws_utils import *

# Define current year and month for directory paths
YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
DAY = datetime.datetime.now().day
START_DATE = (datetime.datetime.utcnow() - datetime.timedelta(days=31)).isoformat()  # 31 days ago
END_DATE = datetime.datetime.utcnow().isoformat()  # current time


