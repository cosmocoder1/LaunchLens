# 🚀 spacex-data-pipeline

**ETL pipeline and analysis for public SpaceX launch data using Python + SQLite.**

This project builds a complete data flow from raw API ingestion to feature-rich visual analysis, producing insights into mission trends, rocket performance, and strategic planning.

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

- **Plug-and-play Runner**  
  One command to run the full system from scratch.

---

## 🗘️ Project Structure

- `main.py` – Orchestrates the full pipeline
- `data/retrieval.py` – Downloads raw JSON from the SpaceX API
- `data/etl.py` – Loads data into SQLite (DataPipeline class)
- `data/schema.sql` – SQL table definitions
- `data/files/` – Raw JSON storage (gitignored)
- `data/spacex.sqlite` – Generated database
- `service/service.py` – MissionAnalyzer (visual and tabular insights)
- `service/jobs.py` – Executes individual analysis jobs
- `analysis/plots/` – Output charts and summaries (gitignored)
- `core/logging.py` – Shared logger utility
- `.gitignore`
- `README.md`

---

## ⚡ Quickstart

### 1. Clone and install

    git clone https://github.com/your-username/spacex-data-pipeline.git
    cd spacex-data-pipeline
    pipenv install  

### 2. Run the full pipeline

    python main.py

This will:

- Recreate the SQLite database  
- Fetch fresh data from the SpaceX API  
- Load data into normalized tables  
- Generate visual insights in `analysis/plots/`

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