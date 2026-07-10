import os
import requests

# =========================
# ENVIRONMENT VARIABLES
# =========================
API_TOKEN = os.environ["WISTIA_API_TOKEN"]

BASE_URL = "https://api.wistia.com/modern"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "X-Wistia-API-Version": "2026-05",
    "Accept": "application/json"
}

MEDIA_IDS = [
    "8hunphufxp",
    "9k4tbcdfg0"
]

REQUEST_TIMEOUT = 30


# =========================
# MEDIA STATS API
# =========================
def fetch_media_data(media_id):
    """
    Retrieve statistics for a single media asset.
    """

    url = f"{BASE_URL}/stats/medias/{media_id}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Media API failed for media_id={media_id}: {e}"
        ) from e


# =========================
# VISITORS API
# =========================
def fetch_visitors(page=1, per_page=100):
    """
    Retrieve one page of visitors.
    """

    url = f"{BASE_URL}/stats/visitors"

    params = {
        "page": page,
        "per_page": per_page
    }

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Visitors API failed on page={page}: {e}"
        ) from e


# =========================
# EVENTS API
# =========================
def fetch_events(page=1, per_page=100, media_id=None):
    """
    Retrieve one page of engagement events.

    If media_id is provided, only events for that media are returned.
    """

    url = f"{BASE_URL}/stats/events"

    params = {
        "page": page,
        "per_page": per_page
    }

    if media_id:
        params["media_id"] = media_id

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Events API failed on page={page}: {e}"
        ) from e
