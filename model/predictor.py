"""Launch Success Probability Inference

This module provides a utility function for predicting the probability of a successful
SpaceX launch given key mission parameters. It loads a pre-trained XGBoost model and
produces a success probability based on historical data patterns.

"""

import joblib
import pandas as pd

# Load trained model and feature columns
model, columns = joblib.load("model/models/success_model.pkl")


def predict_successful_launch(
    rocket: str,
    launchpad: str,
    orbit: str,
    mass_bin: str
) -> float:
    """
    Predict the probability of a successful launch based on mission parameters.

    Args:
        rocket (str): Name of the rocket (e.g., "Falcon 9").
        launchpad (str): Launchpad location (e.g., "KSC LC 39A").
        orbit (str): Target orbit (e.g., "LEO", "SSO", "PO").
        mass_bin (str): Payload mass bin (e.g., "0–500", "500–2000", "2000+").

    Returns:
        float: Estimated success probability as a percentage (e.g., 94.25).
    """
    dataframe = pd.DataFrame([{
        "rocket": rocket,
        "launchpad": launchpad,
        "orbit": orbit,
        "mass_bin": mass_bin
    }])
    dataframe_encoded = pd.get_dummies(dataframe).reindex(columns=columns, fill_value=0)
    prob = model.predict_proba(dataframe_encoded)[0][1]

    return round(prob * 100, 2)
