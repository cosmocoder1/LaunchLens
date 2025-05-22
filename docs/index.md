# 🚀 LaunchLens

**LaunchLens** is a lightweight, full-stack AI and data pipeline for analyzing SpaceX launch data.  
It combines ETL, visual analytics, machine learning, and natural language querying into a single, composable system.

---

## 🧠 Purpose

LaunchLens was designed as a modular, production-ready demonstration of how to turn raw public data into:

- Actionable insights (e.g., launchpad performance, success rates)
- Predictive modeling (launch success classifier)
- Natural language interfaces (RAG-powered questions over CSV/Markdown summaries)

---

## 🧱 Architecture Overview

The system flows through the following stages:

**SpaceX API**
<br>↓<br>
**Raw JSON Fetchers**
<br>↓<br>
**SQLite Database** -
Normalized tables: rockets, launchpads, payloads, launches
<br>↓<br>
**Feature Engineering + ML Modeling** -
XGBoost classifier predicts mission success
<br>↓<br>
**Analysis Outputs** -
Plots, CSV summaries, markdown recommendations
<br>↓<br>
**RAG Indexing (ChromaDB)** -
Embeds analysis outputs into a local vector store
<br>↓<br>
**Streamlit Frontend** - 
Interactive reports, model predictions, and natural language querying

---

## ⚡ Quickstart

```bash
# Clone the repo
git clone https://github.com/cosmocoder1/LaunchLens.git
cd LaunchLens

# Install dependencies
pipenv install

# Add your OpenAI key
echo "OPENAI_API_KEY=sk-..." > .env

# Run the full pipeline (ETL + ML + RAG index)
pipenv run python main.py

# Launch the dashboard
pipenv run streamlit run app.py

```
---

## 📘 Docs

Use the navigation sidebar to explore each part of the system:

- [🔄 ETL Pipeline](pipeline.md): How raw API data is ingested, normalized, and stored in SQLite.
- [🧠 Machine Learning](ml.md): How features are engineered and used to train a launch success classifier.
- [💬 RAG Querying](rag.md): How natural language questions are answered using ChromaDB + OpenAI.

To run the documentation locally:

```bash
pipenv run mkdocs serve
```
Then open http://127.0.0.1:8000 in your browser.

---