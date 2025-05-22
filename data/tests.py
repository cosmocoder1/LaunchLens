"""Performs basic validation and inspection of SpaceX API data saved locally in JSON format.

This script assumes that raw data has already been downloaded via `retrieval.py`
and saved under the `data/` directory. It loads each file and:

- Verifies that the file exists and contains valid JSON
- Prints the number of records in each dataset
- Displays a partial, formatted preview of the first launch record

Usage:
    python data/tests.py

This script helps verify that the data ingestion step was successful and
provides a lightweight overview before further processing.
"""


import json
from pathlib import Path

from core.logging import LOGGER

DATA_DIR = Path("data")
FILES = ["launches.json", "rockets.json", "launchpads.json", "payloads.json"]


def load_json(name: str) -> list[dict]:
    """Loads a JSON file from the data directory.

    Args:
        name (str): Filename (e.g., "launches.json")

    Returns:
        list[dict]: Parsed JSON content as a list of records
    """
    with open(DATA_DIR / name) as f:
        return json.load(f)


if __name__ == "__main__":
    LOGGER.info("Data File Summary:")

    for file in FILES:
        data = load_json(file)
        LOGGER.info(f"{file:<20} → {len(data):>5} records")

    launches = load_json("launches.json")
    LOGGER.info("Sample launch preview:")
    LOGGER.info(json.dumps(launches[0], indent=2)[:800] + "\n...")

