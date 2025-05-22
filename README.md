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

### Prerequisites

- Python 3.10+
- [Pipenv](https://pipenv.pypa.io/en/latest/) installed (`pip install pipenv`)
- `xgboost` installed locally (included in `Pipfile`, but must compile successfully)
- OpenAI API key (optional, for RAG querying)

If you're using M1/M2 Mac or encounter install issues, 
- try:
brew install libomp before installing xgboost

### 1. Clone and install

```bash
git clone https://github.com/cosmocoder1/LaunchLens.git
cd LaunchLens
pipenv install
```

### 2. Run the full data pipeline
```
pipenv run python main.py
```

This will:

- Recreate the SQLite database  
- Fetch fresh SpaceX data from the public API  
- Load and normalize data into structured tables  
- Train a machine learning model to predict launch success  
- Embed analytical outputs into a local Chroma vector store for RAG querying  
- Generate visual plots, CSV summaries, and strategic markdown insights in `analysis/plots/`


### 3. Launch the interactive dashboard

    pipenv run streamlit run app.py

This will:

- Display all pre-generated plots and summaries  
- Showcase strategic planning insights using interactive tables  
- Provide a clean, modular UI for exploring launch patterns

---

## 📊 Example Insights

- Launch frequency trends and year-over-year growth  
- Rocket success rates across configurations  
- Payload mass distribution over time  
- Launchpad performance and reliability metrics  
- Strategic launch planner (rocket + pad + orbit + payload)  
- Predicted success likelihood from custom mission inputs  
- Rocket + launchpad configuration stability over time  
- Sequential launch analysis to detect signs of rocket fatigue  
- Natural language question answering over all insights (via RAG) 

Charts and logs are written to `analysis/plots/`.

---

## 🧪 Tech Stack

- Python 3.10+
- SQLite3
- Pandas + Matplotlib
- Scikit-learn + XGBoost (for predictive modeling)
- Streamlit (interactive dashboard)
- LangChain + ChromaDB + OpenAI (RAG-based question answering)
- MkDocs + Material Theme (project documentation)
- Modular CLI architecture
- Clean structured logging (via custom LOGGER)

---

## 💪 Future Additions

- ☁️ Cloud deployable / S3 integration
- Unit tests & CI   
- CLI argument support for partial runs (ETL-only, analysis-only)

---

## 📘 Documentation

This project includes live documentation powered by [MkDocs](https://www.mkdocs.org/) with the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

To run the docs locally:

```bash
pipenv run mkdocs serve
```

Then open your browser to: http://127.0.0.1:8000

Documentation covers architecture, ETL flow, machine learning, and RAG integration. You can find all source files under the docs/ directory.

---

## 📬 Contact

Built by **Nathan A. Lucy**  
📧 nathanalucy@gmail.com