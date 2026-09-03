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
# SHOW EXPECTED FEATURES
# =========================================================

EXPECTED_FEATURES = list(model.feature_names_in_)

print("======================================")
print("MODEL EXPECTS THESE FEATURES:")
print("======================================")

for feature in EXPECTED_FEATURES:
    print(feature)

print("======================================")


# =========================================================
# URL PREDICTION
# =========================================================

def predict_url(features: dict):

    # -----------------------------------------------------
    # Check features
    # -----------------------------------------------------

    missing_features = [
        feature
        for feature in EXPECTED_FEATURES
        if feature not in features
    ]

    if missing_features:

        raise ValueError(
            f"URL analyzer is missing model features: "
            f"{missing_features}"
        )


    # -----------------------------------------------------
    # Keep ONLY features used during training
    # AND keep them in the exact same order
    # -----------------------------------------------------

    model_features = {
        feature: features[feature]
        for feature in EXPECTED_FEATURES
    }


    # -----------------------------------------------------
    # DataFrame
    # -----------------------------------------------------

    df = pd.DataFrame(
        [model_features],
        columns=EXPECTED_FEATURES
    )


    # -----------------------------------------------------
    # Prediction
    # -----------------------------------------------------

    prediction = model.predict(df)[0]


    # -----------------------------------------------------
    # Probability
    # -----------------------------------------------------

    probabilities = model.predict_proba(df)[0]


    legitimate_probability = probabilities[0]

    phishing_probability = probabilities[1]


    # -----------------------------------------------------
    # Classification
    # -----------------------------------------------------

    if prediction == 1:

        classification = "PHISHING"

    else:

        classification = "LEGITIMATE"


    # -----------------------------------------------------
    # RETURN
    # -----------------------------------------------------

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

        "features": model_features

    }