"""Provides structured, reusable analysis methods for SpaceX mission data.

This class wraps analytical SQL queries and Python-based visualizations
to offer insight into launches, rockets, payloads, and performance metrics.
"""

import sqlite3
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from core.logging import LOGGER


class MissionAnalyzer:
    def __init__(self, db_path: Path) -> None:
        """
        Initializes the analyzer with a connection to the SQLite database.

        Args:
            db_path (Path): Path to the SQLite database file.

        Returns:
            None
        """
        self.db_path = db_path

    def query(self, sql: str) -> pd.DataFrame:
        """
        Executes a SQL query against the database and returns the result as a DataFrame.

        Args:
            sql (str): SQL query string.

        Returns:
            pd.DataFrame: Query results as a pandas DataFrame.
        """
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(sql, conn)

    def launches_per_year(self) -> None:
        """
        Displays a summary table and bar chart of the number of launches per year.

        Why it's useful:
        - Shows operational growth and frequency trends over time

        Args:
            None

        Returns:
            None
        """
        LOGGER.info("Analyzing launches per year.")

        try:
            dataframe = self.query("""
                SELECT strftime('%Y', date_utc) AS year, COUNT(*) AS launch_count
                FROM launches
                GROUP BY year
                ORDER BY year ASC;
            """)
        except Exception as ex:
            LOGGER.error("Failed to run SQL query for launches per year.")
            LOGGER.exception(ex)
            return

        if dataframe.empty:
            LOGGER.warning("No data returned for launches per year.")
            return

        plot_path = Path("analysis/plots/launches_per_year.png")

        try:
            dataframe.plot(x="year", y="launch_count", kind="bar", legend=False, title="Launches per Year")
            plt.ylabel("Number of Launches")
            plt.tight_layout()
            plt.savefig(plot_path)
            plt.close()
            LOGGER.info(f"✅ Saved launch trend chart to {plot_path}")
        except Exception as ex:
            LOGGER.error("Failed to render or save the plot.")
            LOGGER.exception(ex)

    def rocket_success_rates(self) -> None:
        """
        Displays success rates for each rocket, highlighting reliability.

        Why it's useful:
        - Helps identify the most reliable vehicles in the fleet
        - Distinguishes between high-frequency and high-accuracy performers

        Args:
            None

        Returns:
            None
        """

        LOGGER.info("Analyzing rocket success rates...")

        try:
            dataframe = self.query("""
                SELECT
                    r.name AS rocket,
                    COUNT(*) AS total_launches,
                    SUM(CASE WHEN l.success THEN 1 ELSE 0 END) AS successful,
                    ROUND(100.0 * SUM(CASE WHEN l.success THEN 1 ELSE 0 END) / COUNT(*), 2) AS success_rate
                FROM launches l
                JOIN rockets r ON l.rocket_id = r.id
                GROUP BY r.name
                ORDER BY success_rate DESC;
            """)
        except Exception as ex:
            LOGGER.error("Failed to compute rocket success rates.")
            LOGGER.exception(ex)
            return

        if dataframe.empty:
            LOGGER.warning("No rocket launch data available.")
            return

        # Highlight rockets with perfect record
        perfect_rockets = dataframe[dataframe["success_rate"] == 100.0]
        if not perfect_rockets.empty:
            LOGGER.info("\n🚀 Rockets with a flawless success rate:")
            LOGGER.info("\n" + perfect_rockets.to_string(index=False))

        # Plotting
        plot_path = Path("analysis/plots/rocket_success_rates.png")
        try:
            dataframe.plot(x="rocket", y="success_rate", kind="bar", legend=False, title="Rocket Success Rates")
            plt.ylabel("Success Rate (%)")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig(plot_path)
            plt.close()
            LOGGER.info(f"✅ Saved rocket success rate chart to {plot_path}")
        except Exception as ex:
            LOGGER.error("Failed to render or save rocket success rate plot.")
            LOGGER.exception(ex)
