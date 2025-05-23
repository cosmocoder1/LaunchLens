"""Provides structured, reusable analysis methods for SpaceX mission data.

This class wraps analytical SQL queries and Python-based visualizations
to offer insight into launches, rockets, payloads, and performance metrics.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from core.logging import LOGGER
from data.sqlite_database import SQLiteDatabase


class MissionAnalyzer:
    """Provides data analysis and statistical insight generation for SpaceX launch data.

    This service layer reads from the SQLite database and generates visualizations,
    tabular summaries, and strategic outputs such as launch planning recommendations,
    configuration stability metrics, and fatigue detection.
    """
    def __init__(self, db_path: Path) -> None:
        """Initializes the analyzer with a connection to the SQLite database.

        Args:
            db_path (Path): Path to the SQLite database file.

        Returns:
            None
        """
        self.db = SQLiteDatabase(db_path)

    def launches_per_year(self) -> None:
        """Displays a summary table and bar chart of the number of launches per year.

        Why it's useful:
        - Shows operational growth and frequency trends over time

        Args:
            None

        Returns:
            None
        """
        LOGGER.info("Analyzing launches per year.")

        try:
            dataframe = self.db.get_launches_per_year()
        except Exception as ex:
            LOGGER.error("Failed to run SQL query for launches per year.")
            LOGGER.exception(ex)
            return

        if dataframe.empty:
            LOGGER.warning("No data returned for launches per year.")
            return

        plot_path = Path("analysis/plots/launches_per_year.png")

        try:
            dataframe.plot(
                x="year",
                y="launch_count",
                kind="bar",
                legend=False,
                title="Launches per Year"
            )
            plt.ylabel("Number of Launches")
            plt.tight_layout()
            plt.savefig(plot_path)
            plt.close()

            LOGGER.info(f"✅ Saved launch trend chart to {plot_path}")

        except Exception as ex:

            LOGGER.error("Failed to render or save the plot.")
            LOGGER.exception(ex)

    def rocket_success_rates(self) -> None:
        """Displays success rates for each rocket, highlighting reliability.

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
            dataframe = self.db.get_rocket_success_rates()

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
            dataframe.plot(
                x="rocket",
                y="success_rate",
                kind="bar",
                legend=False,
                title="Rocket Success Rates"
            )
            plt.ylabel("Success Rate (%)")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig(plot_path)
            plt.close()

            LOGGER.info(f"✅ Saved rocket success rate chart to {plot_path}")

        except Exception as ex:

            LOGGER.error("Failed to render or save rocket success rate plot.")
            LOGGER.exception(ex)

    def payload_mass_over_time(self) -> None:
        """Visualizes payload mass over time to show mission scale and evolution.

        Why it's useful:
        - Highlights trends in mission heaviness
        - Gives intuitive picture of capability growth over time

        Args:
            None

        Returns:
            None
        """
        LOGGER.info("Analyzing payload mass over time...")

        try:
            dataframe = self.db.get_payload_mass_over_time()
        except Exception as ex:
            LOGGER.error("Failed to retrieve payload mass data.")
            LOGGER.exception(ex)
            return

        if dataframe.empty:
            LOGGER.warning("No payload mass data available.")
            return

        dataframe["date"] = pd.to_datetime(dataframe["date_utc"])

        plot_path = Path("analysis/plots/payload_mass_over_time.png")

        try:
            dataframe.plot.scatter(x="date", y="mass_kg", alpha=0.5, title="Payload Mass Over Time")
            plt.ylabel("Mass (kg)")
            plt.xlabel("Launch Date")
            plt.tight_layout()
            plt.savefig(plot_path)
            plt.close()

            LOGGER.info(f"✅ Saved payload mass trend chart to {plot_path}")

        except Exception as ex:

            LOGGER.error("Failed to render or save payload mass plot.")
            LOGGER.exception(ex)

    def launchpad_performance(self) -> None:
        """Analyzes launchpad usage and reliability.

        Why it's useful:
        - Reveals which launchpads are most trusted and used
        - Highlights operational distribution and success rates

        Args:
            None

        Returns:
            None
        """
        LOGGER.info("Analyzing launchpad performance...")

        try:
            dataframe = self.db.get_launchpad_performance()

        except Exception as ex:
            LOGGER.error("Failed to query launchpad performance.")
            LOGGER.exception(ex)
            return

        if dataframe.empty:
            LOGGER.warning("No launchpad performance data found.")
            return

        plot_path = Path("analysis/plots/launchpad_performance.png")
        try:
            dataframe.plot.barh(
                x="launchpad",
                y="success_rate",
                legend=False,
                title="Launchpad Success Rates"
            )
            plt.xlabel("Success Rate (%)")
            plt.xlim(0, 100)
            plt.tight_layout()
            plt.savefig(plot_path)
            plt.close()

            LOGGER.info(f"✅ Saved launchpad performance chart to {plot_path}")

        except Exception as ex:

            LOGGER.error("Failed to render or save launchpad performance plot.")
            LOGGER.exception(ex)

    def plan_successful_launch(self) -> None:
        """Analyzes mission data to identify statistically reliable launch configurations.

        Why it's useful:
        - Guides strategic decisions for mission design
        - Synthesizes multi-factor insights across rocket, launchpad, payload, and orbit

        Returns:
            None
        """
        LOGGER.info("Planning ideal mission configuration based on historical success rates...")

        try:
            # 1. Rocket + Launchpad Pair Success
            rocket_pad_df = self.db.get_rocket_launchpad_combinations()

            rocket_pad_df.head(5).to_csv("analysis/plots/top_launchpad_configs.csv", index=False)

            # 2. Orbit + Mass Bin Success
            orbit_mass_df = self.db.get_orbit_mass_profiles()
            orbit_mass_df.head(5).to_csv("analysis/plots/orbit_mass_profiles.csv", index=False)

            # 3. Success Rate by Year
            year_df = self.db.get_success_by_year()

            year_df["year"] = year_df["year"].astype(int)
            recent_years = year_df[year_df["year"] >= 2018]
            avg_recent = round(recent_years["success_rate"].mean(), 2)
            year_df.tail(5).to_csv("analysis/plots/success_by_year.csv", index=False)

            # 4. Final Recommendation Markdown Summary
            rec = rocket_pad_df.iloc[0]
            orbit_rec = orbit_mass_df.iloc[0]

            summary_md = f"""
    🧾 **Recommended Launch Profile Based on Historical Data**

    - **Rocket:** {rec['rocket']}
    - **Launchpad:** {rec['launchpad']}
    - **Orbit:** {orbit_rec['orbit']}
    - **Payload:** {orbit_rec['mass_bin']}
    - **Timeframe:** 2018–2023  
    - **Expected Success Rate:** ~{avg_recent}%
            """.strip()

            Path("analysis/plots").mkdir(parents=True, exist_ok=True)
            Path("analysis/plots/launch_recommendation.md").write_text(summary_md)

            LOGGER.info("✅ Launch plan summary and supporting CSVs written to analysis/plots/")

        except Exception as ex:
            LOGGER.error("Failed to generate mission planning output.")
            LOGGER.exception(ex)

    def analyze_config_stability(self) -> None:
        """Analyzes the stability of rocket + launchpad configurations over time.

        This method calculates the year-by-year success rate for each configuration
        and evaluates how consistent each one is by computing the standard deviation
        and coefficient of variation (CV) of success rates across years.

        Outputs:
            - CSV: analysis/plots/config_stability.csv
        """
        LOGGER.info("Analyzing configuration stability over time...")

        try:
            dataframe = self.db.get_config_stability_by_year()

            grouped = dataframe.groupby(["rocket", "launchpad"])
            stats = grouped["success_rate"].agg(["mean", "std"])
            stats["cv"] = (stats["std"] / stats["mean"]).round(2)
            stats = stats.reset_index().sort_values(by="cv")

            stats.to_csv("analysis/plots/config_stability.csv", index=False)
            LOGGER.info("✅ Saved configuration stability analysis to config_stability.csv")

        except Exception as ex:
            LOGGER.error("Failed to analyze configuration stability.")
            LOGGER.exception(ex)

    def detect_rocket_fatigue(self) -> None:
        """Detects performance drift across sequential launches for each rocket.

        Assigns a launch number to each rocket over time and correlates launch number
        with success rate to identify potential degradation or performance trends.

        Outputs:
            - CSV: analysis/plots/rocket_fatigue.csv
        """
        LOGGER.info("Detecting rocket fatigue and sequential performance trends...")

        try:
            dataframe = self.db.get_rocket_sequential_launches()

            dataframe["launch_number"] = (
                dataframe.groupby("rocket")["date_utc"]
                .rank(method="first")
                .astype(int)
            )
            dataframe["success"] = dataframe["success"].astype(int)

            grouped = dataframe.groupby(["rocket", "launch_number"]).agg(
                launches=("success", "count"),
                successful=("success", "sum")
            ).reset_index()

            grouped["success_rate"] = (100 * grouped["successful"] / grouped["launches"]).round(2)

            grouped.to_csv("analysis/plots/rocket_fatigue.csv", index=False)
            LOGGER.info("✅ Saved rocket fatigue trend data to rocket_fatigue.csv")

        except Exception as ex:
            LOGGER.error("Failed to analyze rocket fatigue.")
            LOGGER.exception(ex)

