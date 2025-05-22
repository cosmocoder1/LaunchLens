# 🧠 Machine Learning

LaunchLens includes a machine learning module that predicts the probability of a successful launch based on historical mission data.

This classifier enables forward-looking analysis by simulating outcomes for hypothetical configurations.

---

## 🔍 Features Used

Each mission is represented by:

- **Rocket name**
- **Launchpad**
- **Target orbit**
- **Payload mass bin** (0–500 kg, 500–2000 kg, 2000+ kg)

These features are one-hot encoded into a sparse vector suitable for gradient-boosted trees.

---

## 🤖 Model: XGBoost Classifier

LaunchLens uses an `XGBClassifier` from `xgboost` with simple configuration:

- `eval_metric="logloss"`
- No hyperparameter tuning (can be added later)

Trained using all valid historical missions where outcome and payload info is available.

---

## 📦 Output

The trained model is saved to:

- model/models/success_model.pkl

It’s loaded during dashboard runtime for interactive prediction.

---

## 🎯 Streamlit Integration

Inside the app, users can select:

- Rocket
- Launchpad
- Orbit
- Payload mass bin

The app then predicts the likelihood of success and displays a confidence percentage.

---

## 🔁 Model Training in Pipeline

Every time `main.py` runs, the model is automatically retrained on fresh data:

```python
from model.trainer import train_and_save_model
train_and_save_model()
```

This ensures predictions always reflect the most recent launch records.


