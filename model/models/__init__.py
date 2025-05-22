import pandas as pd
from xgboost import XGBClassifier
import joblib
import sqlite3
from pathlib import Path

# Connect to SQLite
conn = sqlite3.connect("data/spacex.sqlite")

# Query launch data
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
df["mass_bin"] = pd.cut(df["mass_kg"], bins=[0, 500, 2000, float("inf")], labels=["0–500", "500–2000", "2000+"])
df["success"] = df["success"].astype(int)

features = df[["rocket", "launchpad", "orbit", "mass_bin"]]
X = pd.get_dummies(features)
y = df["success"]

# Train model
model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X, y)

# Save model and feature columns
Path("models").mkdir(exist_ok=True)
joblib.dump((model, X.columns.tolist()), "models/success_model.pkl")

print("✅ Model trained and saved to models/success_model.pkl")
