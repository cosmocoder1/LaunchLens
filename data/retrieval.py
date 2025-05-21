"""
retrieval.py

Fetches raw SpaceX API data and stores it locally as JSON files.

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

import requests
import json
from pathlib import Path

BASE_URL = "https://api.spacexdata.com/v4"
ENDPOINTS = ["launches", "rockets", "launchpads", "payloads"]

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def fetch_and_save(endpoint: str) -> None:
    """Fetches data from a SpaceX API endpoint and saves it as a local JSON file."""
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    with open(DATA_DIR / f"{endpoint}.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved {endpoint}.json ({len(data)} records)")


if __name__ == "__main__":
    for ep in ENDPOINTS:
        fetch_and_save(ep)
