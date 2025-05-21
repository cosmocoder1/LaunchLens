"""Provides structured, reusable analysis methods for SpaceX mission data.

This class wraps analytical SQL queries and Python-based visualizations
to offer insight into launches, rockets, payloads, and performance metrics.
"""

import sqlite3
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


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
        print("\nLaunches per Year:")
        df = self.query("""
            SELECT strftime('%Y', date_utc) AS year, COUNT(*) AS launch_count
            FROM launches
            GROUP BY year
            ORDER BY year ASC;
        """)
        print(df)

        # Optional: bar plot
        df.plot(x='year', y='launch_count', kind='bar', legend=False, title="Launches per Year")
        plt.ylabel("Number of Launches")
        plt.tight_layout()
        plt.show()
