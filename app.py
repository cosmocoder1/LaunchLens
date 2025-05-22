"""
SpaceX Launch Insights Dashboard

This Streamlit app provides an interactive interface for exploring visual and textual analytics
derived from public SpaceX launch data. It loads pre-generated plots and summaries to help
users understand launch frequency, performance trends, payload dynamics, and strategic patterns.

Author: Nathan A. Lucy
Email: nathanalucy@gmail.com
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image
import os

st.set_page_config(page_title="SpaceX Launch Insights", layout="wide")

st.title("🚀 SpaceX Launch Insights Dashboard")
st.markdown("Explore visual analytics and strategic summaries derived from the public SpaceX launch dataset.")

# Navigation options
reports = {
    "Launches per Year": "launches_per_year",
    "Launchpad Performance": "launchpad_performance",
    "Payload Mass Over Time": "payload_mass_over_time",
    "Rocket Success Rates": "rocket_success_rates",
    "🧠 Strategic Launch Planner (Data-driven)": "launch_planner"
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
