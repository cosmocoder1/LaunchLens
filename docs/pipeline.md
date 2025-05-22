# 🔄 ETL Pipeline

The LaunchLens ETL pipeline extracts, normalizes, and stores public SpaceX launch data into a structured SQLite database.  
It powers the downstream machine learning and analytics layers.

---

## 📥 Data Sources

LaunchLens pulls data from the [SpaceX public API](https://github.com/r-spacex/SpaceX-API), including:

- Rockets
- Launchpads
- Payloads
- Launches

The data is stored in local JSON files (`data/files/`) for transparency and reproducibility.

---

## 🧱 Schema Overview

The SQLite database includes the following core tables:

- `rockets`: Rocket ID, name, and type
- `launchpads`: Launch site info (ID, name, region)
- `payloads`: Orbit type, payload mass, and classification
- `launches`: Launch metadata including date and success flag
- `launch_payload`: Join table linking launches to payloads (many-to-many)

---

## 🛠️ Pipeline Stages

The ETL flow is orchestrated by the `DataPipeline` class:

1. **Reset Schema**  
   Drops any existing database and rebuilds it using `schema.sql`.

2. **Data Retrieval**  
   Downloads fresh SpaceX data and saves raw JSONs.

3. **Load + Insert**  
   Parses and inserts each entity into its respective table using bulk-safe operations (`INSERT OR IGNORE`).

4. **Join Table Construction**  
   Populates `launch_payload` to map each launch to its associated payload(s).

---

## ✅ Run the Pipeline

You can run the full ETL + analysis + ML + RAG build using:

```bash
python main.py
```

This will reset the DB, ingest data, train the model, run analytics, and index content for querying.