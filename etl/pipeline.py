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

DB_PATH: Path = Path("data/spacex.sqlite")
DATA_DIR: Path = Path("data")
ROCKETS_PATH: Path = DATA_DIR / "rockets.json"
LAUNCHPADS_PATH: Path = DATA_DIR / "launchpads.json"
PAYLOADS_PATH: Path = DATA_DIR / "payloads.json"


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


def insert_launchpads(connection: sqlite3.Connection, launchpads: list[dict[str, Any]]) -> None:
    """
    Inserts launchpad records into the SQLite database.

    Args:
        connection (sqlite3.Connection): Active SQLite DB connection.
        launchpads (list[dict[str, Any]]): List of launchpad records to insert.
    """
    with connection:
        for pad in launchpads:
            connection.execute(
                """
                INSERT OR IGNORE INTO launchpads (id, name, locality, region)
                VALUES (?, ?, ?, ?)
                """,
                (
                    pad.get("id"),
                    pad.get("name"),
                    pad.get("locality"),
                    pad.get("region")
                )
            )
    print(f"Inserted {len(launchpads)} launchpads")

def insert_payloads(connection: sqlite3.Connection, payloads: list[dict[str, Any]]) -> None:
    """
    Inserts payload records into the SQLite database.

    Args:
        connection (sqlite3.Connection): Active SQLite DB connection.
        payloads (list[dict[str, Any]]): List of payload records to insert.
    """
    with connection:
        for payload in payloads:
            connection.execute(
                """
                INSERT OR IGNORE INTO payloads (id, name, type, mass_kg, orbit)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    payload.get("id"),
                    payload.get("name"),
                    payload.get("type"),
                    payload.get("mass_kg"),
                    payload.get("orbit")
                )
            )
    print(f"Inserted {len(payloads)} payloads")


def run() -> None:
    """Runs the ETL pipeline for rockets, launchpads, and payloads."""
    connection = sqlite3.connect(DB_PATH)

    rockets = load_json(ROCKETS_PATH)
    insert_rockets(connection, rockets)

    launchpads = load_json(LAUNCHPADS_PATH)
    insert_launchpads(connection, launchpads)

    payloads = load_json(PAYLOADS_PATH)
    insert_payloads(connection, payloads)


if __name__ == "__main__":
    run()
