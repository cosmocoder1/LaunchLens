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


def run_rocket_success_rates() -> None:
    """
    Job: Show rocket success rates and highlight flawless performers.
    """
    analyzer = MissionAnalyzer(db_path=Path("data/spacex.sqlite"))
    analyzer.rocket_success_rates()


def run_payload_mass_trend() -> None:
    """
    Job: Show payload mass distribution over time with scatterplot.
    """
    analyzer = MissionAnalyzer(db_path=Path("data/spacex.sqlite"))
    analyzer.payload_mass_over_time()


if __name__ == "__main__":
    print("Running SpaceX analysis jobs...\n")
    run_launch_trends()
    run_rocket_success_rates()
    run_payload_mass_trend()

