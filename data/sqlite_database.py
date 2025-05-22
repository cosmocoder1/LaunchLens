"""Provides a centralized interface for querying structured SpaceX launch data.

All query methods return pandas DataFrames and encapsulate reusable SQL used across
the analysis layer.
"""

import sqlite3
from pathlib import Path

import pandas as pd


class SQLiteDatabase:
    """Encapsulates reusable SQL queries for accessing SpaceX launch data from SQLite."""

    def __init__(self, db_path: Path) -> None:
        """Initializes the database connection.

        Args:
            db_path (Path): Path to the SQLite database file.
        """
        self.connection = sqlite3.connect(db_path)

    def get_launches_per_year(self) -> pd.DataFrame:
        """Returns the number of launches per year."""
        return pd.read_sql_query(
            """
            SELECT strftime('%Y', date_utc) AS year, COUNT(*) AS launch_count
            FROM launches
            GROUP BY year
            ORDER BY year ASC;
            """,
            self.connection,
        )

    def get_rocket_success_rates(self) -> pd.DataFrame:
        """Returns total launches and success rate per rocket."""
        return pd.read_sql_query(
            """
            SELECT
                r.name AS rocket,
                COUNT(*) AS total_launches,
                SUM(CASE WHEN l.success THEN 1 ELSE 0 END) AS successful,
                ROUND(
                    100.0 * SUM(CASE WHEN l.success THEN 1 ELSE 0 END) / COUNT(*),
                    2
                ) AS success_rate
            FROM launches l
            JOIN rockets r ON l.rocket_id = r.id
            GROUP BY r.name
            ORDER BY success_rate DESC;
            """,
            self.connection,
        )

    def get_payload_mass_over_time(self) -> pd.DataFrame:
        """Returns payload mass and launch dates for all launches with valid mass."""
        return pd.read_sql_query(
            """
            SELECT p.mass_kg, l.date_utc
            FROM payloads p
            JOIN launch_payload lp ON p.id = lp.payload_id
            JOIN launches l ON l.id = lp.launch_id
            WHERE p.mass_kg IS NOT NULL
            """,
            self.connection,
        )

    def get_launchpad_performance(self) -> pd.DataFrame:
        """Returns launchpad usage and success metrics."""
        return pd.read_sql_query(
            """
            SELECT
                lp.name AS launchpad,
                COUNT(*) AS total_launches,
                SUM(CASE WHEN l.success THEN 1 ELSE 0 END) AS successful,
                ROUND(
                    100.0 * SUM(CASE WHEN l.success THEN 1 ELSE 0 END) / COUNT(*),
                    2
                ) AS success_rate
            FROM launches l
            JOIN launchpads lp ON l.launchpad_id = lp.id
            GROUP BY lp.name
            ORDER BY total_launches DESC;
            """,
            self.connection,
        )

    def get_rocket_launchpad_combinations(self) -> pd.DataFrame:
        """Returns launch success rate for each rocket + launchpad pair."""
        return pd.read_sql_query(
            """
            SELECT
                r.name AS rocket,
                lp.name AS launchpad,
                COUNT(*) AS launches,
                SUM(CASE WHEN l.success THEN 1 ELSE 0 END) AS successful,
                ROUND(
                    100.0 * SUM(CASE WHEN l.success THEN 1 ELSE 0 END) / COUNT(*),
                    2
                ) AS success_rate
            FROM launches l
            JOIN rockets r ON l.rocket_id = r.id
            JOIN launchpads lp ON l.launchpad_id = lp.id
            GROUP BY r.name, lp.name
            HAVING launches >= 3
            ORDER BY success_rate DESC, launches DESC
            """,
            self.connection,
        )

    def get_orbit_mass_profiles(self) -> pd.DataFrame:
        """Returns success rate across orbit and payload mass bins."""
        return pd.read_sql_query(
            """
            SELECT
                p.orbit,
                CASE
                    WHEN p.mass_kg < 500 THEN '0–500 kg'
                    WHEN p.mass_kg < 2000 THEN '500–2000 kg'
                    ELSE '2000+ kg'
                END AS mass_bin,
                COUNT(*) AS missions,
                SUM(CASE WHEN l.success THEN 1 ELSE 0 END) AS successful,
                ROUND(
                    100.0 * SUM(CASE WHEN l.success THEN 1 ELSE 0 END) / COUNT(*),
                    2
                ) AS success_rate
            FROM payloads p
            JOIN launch_payload lp ON p.id = lp.payload_id
            JOIN launches l ON l.id = lp.launch_id
            WHERE p.mass_kg IS NOT NULL AND p.orbit IS NOT NULL
            GROUP BY orbit, mass_bin
            HAVING missions >= 3
            ORDER BY success_rate DESC, missions DESC
            """,
            self.connection,
        )

    def get_success_by_year(self) -> pd.DataFrame:
        """Returns yearly launch counts and success rates."""
        return pd.read_sql_query(
            """
            SELECT
                strftime('%Y', date_utc) AS year,
                COUNT(*) AS launches,
                SUM(CASE WHEN success THEN 1 ELSE 0 END) AS successful,
                ROUND(
                    100.0 * SUM(CASE WHEN success THEN 1 ELSE 0 END) / COUNT(*),
                    2
                ) AS success_rate
            FROM launches
            GROUP BY year
            ORDER BY year ASC
            """,
            self.connection,
        )

    def get_config_stability_by_year(self) -> pd.DataFrame:
        """Returns launch success rates over time for each rocket + launchpad combo."""
        return pd.read_sql_query(
            """
            SELECT
                r.name AS rocket,
                lp.name AS launchpad,
                strftime('%Y', l.date_utc) AS year,
                COUNT(*) AS launches,
                SUM(CASE WHEN l.success THEN 1 ELSE 0 END) AS successful,
                ROUND(
                    100.0 * SUM(CASE WHEN l.success THEN 1 ELSE 0 END) / COUNT(*),
                    2
                ) AS success_rate
            FROM launches l
            JOIN rockets r ON l.rocket_id = r.id
            JOIN launchpads lp ON l.launchpad_id = lp.id
            GROUP BY r.name, lp.name, year
            HAVING launches >= 2
            """,
            self.connection,
        )

    def get_rocket_sequential_launches(self) -> pd.DataFrame:
        """Returns rockets and their launches with success flags ordered by time."""
        return pd.read_sql_query(
            """
            SELECT
                r.name AS rocket,
                l.date_utc,
                l.success
            FROM launches l
            JOIN rockets r ON l.rocket_id = r.id
            WHERE l.success IS NOT NULL
            ORDER BY r.name, l.date_utc
            """,
            self.connection,
        )

    def close(self) -> None:
        """Closes the database connection."""
        self.connection.close()



