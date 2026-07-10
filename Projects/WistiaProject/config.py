"""
All environment variables, API settings, AWS resources, and shared
constants should be defined here so the rest of the application
can simply import what it needs.
"""

import os

# ==========================================================
# AWS CONFIGURATION
# ==========================================================

S3_BUCKET = os.environ["S3_BUCKET"]

# ==========================================================
# WISTIA API CONFIGURATION
# ==========================================================

API_TOKEN = os.environ["WISTIA_API_TOKEN"]

BASE_URL = "https://api.wistia.com/modern"

API_VERSION = "2026-05"

REQUEST_TIMEOUT = 30  # seconds

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "X-Wistia-API-Version": API_VERSION,
    "Accept": "application/json"
}


# ==========================================================
# INGESTION CONFIGURATION
# ==========================================================

# Maximum number of records returned by the Wistia API.
DEFAULT_PAGE_SIZE = 100

# Location of the incremental ingestion checkpoint.
CHECKPOINT_KEY = "checkpoint/last_run.json"


# ==========================================================
# DEVELOPMENT SETTINGS
# ==========================================================

# Temporary media IDs used during development.
# Replace this once media discovery is automated.
MEDIA_IDS = [
    "8hunphufxp",
    "9k4tbcdfg0"
]