"""Launch Success Model Trainer.

This script extracts historical launch data from the SQLite database,
performs feature engineering, and trains a classification model to
predict launch success based on rocket, launchpad, orbit, and payload bin.

The trained XGBoost model is saved alongside its input feature schema
for use in downstream prediction utilities.

"""

import sqlite3
from pathlib import Path

import joblib
import pandas as pd
from xgboost import XGBClassifier


def train_and_save_model(
    db_path: str = "data/spacex.sqlite",
    model_path: str = "model/models/success_model.pkl"
) -> None:
    """Trains a launch success classifier using historical data and saves the model.

    Args:
        db_path (str): Path to the SQLite database file.
        model_path (str): Output path for the saved model file (.pkl).
    """
    # Connect to SQLite and fetch relevant data
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("""
        SELECT
            r.name AS rocket,
            lp.name AS launchpad,
            p.orbit,
            p.mass_kg,
            l.success
        FROM launches l
        JOIN rockets r ON l.rocket_id = r.id
        JOIN launchpads lp ON l.launchpad_id = lp.id
        JOIN launch_payload lpmap ON l.id = lpmap.launch_id
        JOIN payloads p ON lpmap.payload_id = p.id
        WHERE l.success IS NOT NULL
          AND p.orbit IS NOT NULL
          AND p.mass_kg IS NOT NULL
    """, conn)
    conn.close()

    # Feature engineering
    df["mass_bin"] = pd.cut(
        df["mass_kg"],
        bins=[0, 500, 2000, float("inf")],
        labels=["0–500", "500–2000", "2000+"]
    )
    df["success"] = df["success"].astype(int)

    features = df[["rocket", "launchpad", "orbit", "mass_bin"]]
    X = pd.get_dummies(features)
    y = df["success"]

    # Train XGBoost classifier
    model = XGBClassifier(eval_metric="logloss")
    model.fit(X, y)

    # Save model and column schema
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump((model, X.columns.tolist()), model_path)


if __name__ == "__main__":
    train_and_save_model()
