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

DATA_DIR = Path("data")
FILES = ["launches.json", "rockets.json", "launchpads.json", "payloads.json"]


def load_json(name):
    with open(DATA_DIR / name, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    print("Data File Summary:\n")
    for file in FILES:
        data = load_json(file)
        print(f"{file:<20} → {len(data):>5} records")

    print("\nSample launch:")
    launches = load_json("launches.json")
    print(json.dumps(launches[0], indent=2)[:800] + "\n...")
