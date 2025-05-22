"""
MainPipeline orchestrates the entire SpaceX data pipeline:
- Rebuilds the SQLite schema
- Runs full ETL to load data from raw JSON
- Executes all analytical jobs to generate insights and plots
"""

import sqlite3
from pathlib import Path

from etl.pipeline import DataPipeline
from analysis.service import MissionAnalyzer
from core.logging import LOGGER
from rag.indexer import build_vector_store

DB_PATH = Path("data/spacex.sqlite")
SCHEMA_PATH = Path("schema/schema.sql")


class MainPipeline:
    """
    Top-level runner for resetting, ingesting, and analyzing SpaceX data.
    """

    def __init__(self, db_path: Path = DB_PATH, schema_path: Path = SCHEMA_PATH):
        """
        Initializes the MainPipeline.

        Args:
            db_path (Path): Path to the SQLite DB file.
            schema_path (Path): Path to the SQL schema definition.
        """
        self.db_path = db_path
        self.schema_path = schema_path

    def reset_database(self) -> None:
        """
        Deletes any existing database file and recreates the schema.
        """
        if self.db_path.exists():
            self.db_path.unlink()
            LOGGER.info(f"🗑️ Removed existing DB at {self.db_path}")

        with sqlite3.connect(self.db_path) as conn:
            with open(self.schema_path, "r") as f:
                conn.executescript(f.read())
            LOGGER.info("🧱 Recreated schema from schema.sql")

    def run_etl(self) -> None:
        """
        Runs the full ETL pipeline using DataPipeline.
        """
        pipeline = DataPipeline(self.db_path)
        pipeline.run()

    @staticmethod
    def run_analysis() -> None:
        """
        Executes all analysis jobs using the MissionAnalyzer service.

        This includes:
        - Trend visualizations
        - Launchpad and payload analytics
        - Strategic mission planning
        - Configuration stability
        - Rocket fatigue trend detection

        Outputs charts, CSVs, and summaries to the `analysis/plots/` directory.
        """
        analyzer = MissionAnalyzer(db_path=Path("data/spacex.sqlite"))

        analyzer.launches_per_year()
        analyzer.rocket_success_rates()
        analyzer.payload_mass_over_time()
        analyzer.launchpad_performance()
        analyzer.plan_successful_launch()
        analyzer.analyze_config_stability()
        analyzer.detect_rocket_fatigue()

    def run_all(self) -> None:
        """
        Executes the entire pipeline from schema reset to analysis.
        """
        LOGGER.info("🚀 Starting MainPipeline...")

        self.reset_database()
        self.run_etl()

        LOGGER.info("🧠 Starting analysis phase...")

        self.run_analysis()

        # Import and run model training
        from model.trainer import train_and_save_model
        train_and_save_model(db_path=str(self.db_path))
        LOGGER.info("🤖 ML model retrained and saved.")

        # Build RAG index from analysis outputs
        from rag.indexer import build_vector_store
        build_vector_store()
        LOGGER.info("🧠 RAG vector store built from analysis outputs.")

        LOGGER.info("🏁 MainPipeline complete.")


if __name__ == "__main__":
    MainPipeline().run_all()
