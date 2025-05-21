"""ETL script to populate the SQLite database from raw SpaceX JSON data.

Each function is responsible for loading and inserting a specific entity:
- Rockets
- Launchpads
- Payloads
- Launches
- Launch-Payload join table

All insertions are idempotent and wrapped in transactions for reliability.
"""

import json
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path("data/spacex.sqlite")
DATA_PATH = Path("data/rockets.json")


def load_json(path: Path) -> list[dict[str, Any]]:
    """
    Loads and parses a JSON file.

    Args:
        path (Path): Path to the JSON file.

    Returns:
        list[dict[str, Any]]: Parsed list of records from the file.
    """
    with open(path, "r") as f:
        return json.load(f)


def insert_rockets(connection: sqlite3.Connection, rockets: list[dict[str, Any]]) -> None:
    """
    Inserts rocket records into the SQLite database.

    Args:
        connection (sqlite3.Connection): Active SQLite DB connection.
        rockets (list[dict[str, Any]]): List of rocket records to insert.
    """
    with connection:
        for rocket in rockets:
            connection.execute(
                """
                INSERT OR IGNORE INTO rockets (id, name, type)
                VALUES (?, ?, ?)
                """,
                (
                    rocket.get("id"),
                    rocket.get("name"),
                    rocket.get("type")
                )
            )
    print(f"Inserted {len(rockets)} rockets")


def run() -> None:
    """
    Runs the ETL process for loading rockets into the database.
    """
    connection = sqlite3.connect(DB_PATH)
    rockets = load_json(DATA_PATH)
    insert_rockets(connection, rockets)


if __name__ == "__main__":
    run()
