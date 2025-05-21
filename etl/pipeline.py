"""
ETL pipeline for populating the local SQLite database with structured SpaceX launch data.

This module defines the DataPipeline class, which loads raw JSON records from disk and
inserts them into the appropriate tables:
- Rockets
- Launchpads
- Payloads
- Launches
- Launch-Payload join table

All insertions are idempotent and executed within transactions for consistency and reliability.
"""


import json
import sqlite3
from pathlib import Path
from typing import Any

from core.logging import LOGGER
from data.retrieval import fetch_all

DB_PATH: Path = Path("data/spacex.sqlite")
DATA_DIR: Path = Path("data/files")
DATA_DIR.mkdir(parents=True, exist_ok=True)

ROCKETS_PATH: Path = DATA_DIR / "rockets.json"
LAUNCHPADS_PATH: Path = DATA_DIR / "launchpads.json"
PAYLOADS_PATH: Path = DATA_DIR / "payloads.json"
LAUNCHES_PATH: Path = DATA_DIR / "launches.json"


class DataPipeline:
    """
    Loads and inserts structured SpaceX API data into a local SQLite database.
    Supports rockets, launchpads, payloads, launches, and their relationships.
    """

    def __init__(self, db_path: Path = DB_PATH):
        """
        Initializes the pipeline with a database path and opens a SQLite connection.

        Args:
            db_path (Path): Path to the target SQLite database.
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)

    @staticmethod
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

    def insert_rockets(self, rockets: list[dict[str, Any]]) -> None:
        """
        Inserts rocket records into the database.

        Args:
            rockets (list[dict[str, Any]]): List of rocket records.
        """
        with self.connection:
            for rocket in rockets:
                self.connection.execute(
                    """
                    INSERT OR IGNORE INTO rockets (id, name, type)
                    VALUES (?, ?, ?)
                    """,
                    (rocket.get("id"), rocket.get("name"), rocket.get("type"))
                )
        LOGGER.info(f"🛰️ Inserted {len(rockets)} rockets")

    def insert_launchpads(self, launchpads: list[dict[str, Any]]) -> None:
        """
        Inserts launchpad records into the database.

        Args:
            launchpads (list[dict[str, Any]]): List of launchpad records.
        """
        with self.connection:
            for pad in launchpads:
                self.connection.execute(
                    """
                    INSERT OR IGNORE INTO launchpads (id, name, locality, region)
                    VALUES (?, ?, ?, ?)
                    """,
                    (pad.get("id"), pad.get("name"), pad.get("locality"), pad.get("region"))
                )
        LOGGER.info(f"🏗️ Inserted {len(launchpads)} launchpads")

    def insert_payloads(self, payloads: list[dict[str, Any]]) -> None:
        """
        Inserts payload records into the database.

        Args:
            payloads (list[dict[str, Any]]): List of payload records.
        """
        with self.connection:
            for payload in payloads:
                self.connection.execute(
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
        LOGGER.info(f"📦 Inserted {len(payloads)} payloads")

    def insert_launches(self, launches: list[dict[str, Any]]) -> None:
        """
        Inserts launch records into the database.

        Args:
            launches (list[dict[str, Any]]): List of launch records.
        """
        with self.connection:
            for launch in launches:
                self.connection.execute(
                    """
                    INSERT OR IGNORE INTO launches (id, name, date_utc, success, rocket_id, launchpad_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        launch.get("id"),
                        launch.get("name"),
                        launch.get("date_utc"),
                        launch.get("success"),
                        launch.get("rocket"),
                        launch.get("launchpad")
                    )
                )
        LOGGER.info(f"🚀 Inserted {len(launches)} launches")

    def insert_launch_payloads(self, launches: list[dict[str, Any]]) -> None:
        """
        Inserts launch-to-payload mappings into the join table.

        Args:
            launches (list[dict[str, Any]]): Launch records containing payload ID lists.
        """
        with self.connection:
            for launch in launches:
                launch_id = launch.get("id")
                for payload_id in launch.get("payloads", []):
                    self.connection.execute(
                        """
                        INSERT OR IGNORE INTO launch_payload (launch_id, payload_id)
                        VALUES (?, ?)
                        """,
                        (launch_id, payload_id)
                    )
        LOGGER.info(f"🔗 Mapped payloads for {len(launches)} launches")

    def run(self) -> None:
        """
        Runs the full ETL pipeline:
        - Retrieves fresh SpaceX data
        - Loads JSON records from disk
        - Inserts rockets, launchpads, payloads, and launches
        - Populates join table for launch-to-payload relationships
        """

        LOGGER.info("🌐 Fetching fresh SpaceX data...")

        fetch_all()

        LOGGER.info("🔄 Running ETL pipeline...")

        rockets = self.load_json(ROCKETS_PATH)
        self.insert_rockets(rockets)

        launchpads = self.load_json(LAUNCHPADS_PATH)
        self.insert_launchpads(launchpads)

        payloads = self.load_json(PAYLOADS_PATH)
        self.insert_payloads(payloads)

        launches = self.load_json(LAUNCHES_PATH)
        self.insert_launches(launches)
        self.insert_launch_payloads(launches)

        LOGGER.info("✅ ETL pipeline complete.")


if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run()
