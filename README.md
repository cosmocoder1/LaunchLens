# 🚀 LaunchLens

**ETL pipeline and analysis for public SpaceX launch data using Python + SQLite.**

This project builds a complete data flow from raw SpaceX API ingestion to visual and ML-powered analysis, delivering insights into mission trends, rocket performance, strategic planning, and launch success prediction.

---

## 📦 Features

- 🔄 **Automated Data Retrieval**  
  Pulls fresh data from SpaceX's public API.

- 🧱 **SQLite Schema Management**  
  Rebuilds and resets the DB schema with one command.

- 🧪 **ETL Pipeline**  
  Loads, transforms, and inserts normalized records.

- 📊 **Analytical Reports**  
  Generates visuals and structured insights.

- 🧠 **Strategic Mission Planning**  
  Highlights optimal configurations based on historical data.

- 🧰 **Modular Codebase**  
  Clean separation of concerns via orchestrator, service classes, and jobs.

- 🤖 ML-Powered Insight: Predicts launch success probability using an XGBoost model trained on historical data

- **Plug-and-play Runner**  
  One command to run the full system from scratch.

---

## 🗘️ Project Structure

- `main.py` – Orchestrates the full pipeline
- `data/retrieval.py` – Downloads raw JSON from the SpaceX API
- `etl/pipeline.py` – Loads data into SQLite (DataPipeline class)
- `data/files/` – Raw JSON storage (gitignored)
- `data/spacex.sqlite` – Generated database
- `analysis/service.py` – MissionAnalyzer (visual and tabular insights)
- `analysis/plots/` – Output charts and summaries (gitignored)
- `core/logging.py` – Shared logger utility
- `model/models.py` – Trained classifier models
- `model/predictor.py` – Applies trained models
- `model/trainer.py` – Trains models
- `scripts/build_db.py` – Runs database creation
- `.gitignore`
- `README.md`

---

## ⚡ Quickstart

### 1. Clone and install

    git clone https://github.com/your-username/spacex-data-pipeline.git
    cd spacex-data-pipeline
    pipenv install

### 2. Run the full data pipeline

    python main.py

This will:

- Recreate the SQLite database  
- Fetch fresh SpaceX data from the public API  
- Load and normalize data into structured tables  
- Generate visual plots and CSV summaries in `analysis/plots/`

### 3. Launch the interactive dashboard

    streamlit run app.py

This will:

- Display all pre-generated plots and summaries  
- Showcase strategic planning insights using interactive tables  
- Provide a clean, modular UI for exploring launch patterns

---

## 📊 Example Insights

- Launches per year and growth trends  
- Rocket success rates by configuration  
- Orbit + payload mass profile analysis  
- 🧠 Strategic mission planner based on historical data  

Charts and logs are written to `analysis/plots/`.

---

## 🧪 Tech Stack

- Python 3.10+
- SQLite3
- Pandas + Matplotlib
- Requests
- Modular CLI structure
- Clean logging

---

## 💪 Future Additions

- 🔮 `predict_successful_launch()` – simulate success likelihood from hypothetical inputs  
- ☁️ Cloud deployable / S3 integration
- Unit tests & CI   
- CLI argument support for partial runs (ETL-only, analysis-only)

---

## 📬 Contact

Built by **Nathan A. Lucy**  
📧 nathanalucy@gmail.com