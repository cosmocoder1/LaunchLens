"""Fetches raw SpaceX API data and stores it locally as JSON files.

This script downloads data from the public SpaceX REST API v4 for the following endpoints:
- launches
- rockets
- launchpads
- payloads

All responses are saved under the local `data/` directory as prettified JSON files
(e.g., `data/launches.json`) for inspection and offline processing.

Usage:
    python data/retrieval.py

This is intended as the first step in the ETL process for building a normalized SQLite database.
"""

import json
from pathlib import Path

import requests

from core.logging import LOGGER

BASE_URL = "https://api.spacexdata.com/v4"
ENDPOINTS = ["launches", "rockets", "launchpads", "payloads"]

DATA_DIR = Path("data/files")
DATA_DIR.mkdir(exist_ok=True)


def fetch_and_save(endpoint: str) -> None:
    """Downloads data from the SpaceX public API and saves it as a formatted JSON file.

    Args:
        endpoint (str): The API endpoint to fetch (e.g., "launches", "rockets").

    Behavior:
        - Sends a GET request to BASE_URL/{endpoint}
        - Raises an HTTPError if the request fails
        - Writes the JSON response to data/files/{endpoint}.json
        - Prints a success message with record count

    Returns:
        None
    """
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    with open(DATA_DIR / f"{endpoint}.json", "w") as file:
        json.dump(data, file, indent=2)

    LOGGER.info(f"✅ Saved {endpoint}.json ({len(data)} records)")


def fetch_all() -> None:
    """Fetches all SpaceX data endpoints and saves them as JSON files locally."""
    for endpoint in ENDPOINTS:
        fetch_and_save(endpoint)


if __name__ == "__main__":
    for ep in ENDPOINTS:
        fetch_and_save(ep)
