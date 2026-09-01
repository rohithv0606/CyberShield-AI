import joblib
import pandas as pd
import os


# =========================================================
# LOAD MODEL
# =========================================================

MODEL_PATH = "ml/models/cybershield_url_model.joblib"

print("Loading CyberShield URL ML model...")

model = joblib.load(MODEL_PATH)

print("URL Random Forest loaded successfully!")


# =========================================================
# URL PREDICTION
# =========================================================

def predict_url(features: dict):

    # Convert dictionary into DataFrame
    df = pd.DataFrame([features])

    # Prediction
    prediction = model.predict(df)[0]

    # Probability
    probabilities = model.predict_proba(df)[0]

    # Assuming:
    # 0 = legitimate
    # 1 = phishing

    legitimate_probability = probabilities[0]
    phishing_probability = probabilities[1]

    if prediction == 1:
        classification = "PHISHING"
    else:
        classification = "LEGITIMATE"

    return {

        "classification": classification,

        "prediction": int(prediction),

        "phishing_probability": round(
            float(phishing_probability), 4
        ),

        "legitimate_probability": round(
            float(legitimate_probability), 4
        ),

        "features": features

    }