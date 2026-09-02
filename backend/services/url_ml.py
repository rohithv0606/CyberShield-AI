import joblib
import pandas as pd

from huggingface_hub import hf_hub_download


# =========================================================
# HUGGING FACE MODEL
# =========================================================

REPO_ID = "Rohithv06/cybershield-url-model"

MODEL_FILE = "cybershield_url_model.joblib"


# =========================================================
# DOWNLOAD / LOAD MODEL
# =========================================================

print("Loading CyberShield URL ML model from Hugging Face...")

MODEL_PATH = hf_hub_download(
    repo_id=REPO_ID,
    filename=MODEL_FILE
)

model = joblib.load(MODEL_PATH)

print("CyberShield URL Random Forest loaded successfully!")


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
            float(phishing_probability),
            4
        ),

        "legitimate_probability": round(
            float(legitimate_probability),
            4
        ),

        "features": features
    }