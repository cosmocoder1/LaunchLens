"""Initializes the SQLite database by executing the schema defined in schema/schema.sql.

Creates a new database file at data/spacex.sqlite if it doesn't exist.
Intended to be run before any ETL scripts.
"""

import sqlite3
from pathlib import Path

DB_PATH: Path = Path("data/spacex.sqlite")
SCHEMA_PATH: Path = Path("schema/schema.sql")


def build_database() -> None:
    """Creates the SQLite database and applies the schema."""
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")

    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA_PATH.read_text())

    print(f"✅ Database created at {DB_PATH}")


if __name__ == "__main__":
    build_database()
