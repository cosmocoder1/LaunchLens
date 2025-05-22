"""
SpaceX Launch Insights Dashboard

This Streamlit app provides an interactive interface for exploring visual and textual analytics
derived from public SpaceX launch data. It loads pre-generated plots and summaries to help
users understand launch frequency, performance trends, payload dynamics, and strategic patterns.

Author: Nathan A. Lucy
Email: nathanalucy@gmail.com
"""

import os
from dotenv import load_dotenv
from pathlib import Path

import pandas as pd
from PIL import Image
import streamlit as st


st.set_page_config(page_title="LaunchLens", layout="wide")

st.title("🚀 LaunchLens Dashboard")
st.markdown("Analyze historical SpaceX launch data with visual insights and machine learning–powered predictions.")

# Navigation options
reports = {
    "Launches per Year": "launches_per_year",
    "Launchpad Performance": "launchpad_performance",
    "Payload Mass Over Time": "payload_mass_over_time",
    "Rocket Success Rates": "rocket_success_rates",
    "🧠 Strategic Launch Planner (Data-driven)": "launch_planner",
    "🧪 Advanced Insights": "advanced_insights"
}

selection = st.selectbox("Choose a report:", list(reports.keys()))
key = reports[selection]

# --- Special case: Data-driven Launch Planner ---
if key == "launch_planner":
    st.subheader("🚀 Top Rocket + Launchpad Configurations")
    pad_path = Path("analysis/plots/top_launchpad_configs.csv")
    if pad_path.exists():
        st.dataframe(pd.read_csv(pad_path))
    else:
        st.info("Rocket + Launchpad data not found.")

    st.subheader("📦 Best Orbit + Payload Mass Profiles")
    orbit_path = Path("analysis/plots/orbit_mass_profiles.csv")
    if orbit_path.exists():
        st.dataframe(pd.read_csv(orbit_path))
    else:
        st.info("Orbit + payload profile data not found.")

    st.subheader("📆 Success Rate by Year")
    year_path = Path("analysis/plots/success_by_year.csv")
    if year_path.exists():
        st.dataframe(pd.read_csv(year_path))
    else:
        st.info("Success by year data not found.")

    st.subheader("🧾 Recommended Launch Profile")
    rec_path = Path("analysis/plots/launch_recommendation.md")
    if rec_path.exists():
        st.markdown(rec_path.read_text())
    else:
        st.info("Recommendation summary not found.")

    # 🎯 Predictive Model
    st.subheader("🎯 Predict Mission Success")
    rocket = st.selectbox("Rocket", ["Falcon 9", "Falcon Heavy"])
    launchpad = st.selectbox("Launchpad", ["KSC LC 39A", "CCSFS SLC 40", "VAFB SLC 4E"])
    orbit = st.selectbox("Orbit", ["LEO", "SSO", "PO", "GTO"])
    mass_bin = st.selectbox("Payload Bin", ["0–500", "500–2000", "2000+"])

    if st.button("Predict Success Rate"):
        try:
            from model.predictor import predict_successful_launch
            score = predict_successful_launch(rocket, launchpad, orbit, mass_bin)
            st.success(f"Estimated Success Probability: **{score}%**")
        except Exception as ex:
            st.error("Model not found or failed to predict.")
            st.exception(ex)

    # 💬 Natural Language Query (RAG)
    st.subheader("💬 Ask a Question About the Launch Data")

    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    if OPENAI_API_KEY:
        user_question = st.text_area(
            "Enter your question:",
            placeholder="e.g. What rocket and launchpad combination has the highest success rate?",
            height=100
        )

        if st.button("Ask LaunchLens") and user_question.strip():
            with st.spinner("Thinking..."):
                try:
                    from rag.query_engine import query_launchlens
                    response = query_launchlens(user_question)
                    if response:
                        st.success(response)
                    else:
                        st.warning("No answer was returned.")
                except Exception as ex:
                    st.error("Query failed.")
                    st.exception(ex)

        st.markdown("**Example questions:**")
        st.markdown("- What is the most successful orbit and payload combination?")
        st.markdown("- How has the launch success rate changed since 2018?")
        st.markdown("- Which launchpad has the highest volume?")
    else:
        st.info("To enable natural language queries, add your OpenAI API key to a `.env` file.")

elif key == "advanced_insights":
    st.subheader("📊 Configuration Stability by Rocket + Launchpad")
    stability_path = Path("analysis/plots/config_stability.csv")
    if stability_path.exists():
        df = pd.read_csv(stability_path)
        st.dataframe(df)
    else:
        st.info("Stability data not available.")

    st.subheader("📉 Rocket Fatigue Over Sequential Launches")
    fatigue_path = Path("analysis/plots/rocket_fatigue.csv")
    if fatigue_path.exists():
        df = pd.read_csv(fatigue_path)
        st.dataframe(df)
    else:
        st.info("Fatigue analysis not available.")

    st.subheader("💬 Ask a Question About These Insights")

    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    if OPENAI_API_KEY:
        user_question = st.text_area(
            "Enter your question:",
            placeholder="e.g. Which rocket shows the most stable launch performance over time?",
            height=100
        )

        if st.button("Ask (Advanced)") and user_question.strip():
            with st.spinner("Thinking..."):
                try:
                    from rag.query_engine import query_launchlens
                    response = query_launchlens(user_question)
                    if response:
                        st.success(response)
                    else:
                        st.warning("No answer was returned.")
                except Exception as e:
                    st.error("Query failed.")
                    st.exception(e)

        st.markdown("**Example questions:**")
        st.markdown("- Which configuration is most stable?")
        st.markdown("- Are there signs of rocket fatigue over time?")
        st.markdown("- How does Falcon 9 performance vary year to year?")
    else:
        st.info("To enable natural language queries, add your OpenAI API key to a `.env` file.")


# --- Standard case: Plot + optional summary ---
else:
    image_path = os.path.join("analysis", "plots", f"{key}.png")
    text_path = os.path.join("analysis", "plots", f"{key}.txt")

    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, caption=selection)

    if os.path.exists(text_path):
        with open(text_path, "r") as f:
            st.markdown(f"**Summary:**\n\n{f.read()}")

    if not os.path.exists(image_path) and not os.path.exists(text_path):
        st.error("No content available for this report.")
