"""Orchestrates analysis jobs using the MissionAnalyzer class.

Each job wraps a standalone insight or visualization for clarity and modularity.
"""

from pathlib import Path
from service import MissionAnalyzer


def run_launch_trends() -> None:
    """
    Job: Show number of launches per year with table and bar chart.
    """
    analyzer = MissionAnalyzer(db_path=Path("data/spacex.sqlite"))
    analyzer.launches_per_year()


if __name__ == "__main__":
    print("🛰️ Running SpaceX analysis jobs...\n")
    run_launch_trends()
