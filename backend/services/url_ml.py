import joblib
import pandas as pd
from pathlib import Path

from backend.services.url_feature_extractor import extract_url_features


# =========================================================
# MODEL PATH
# =========================================================

MODEL_PATH = Path("ml/models/cybershield_url_model.joblib")


# =========================================================
# LOAD MODEL
# =========================================================

print("Loading CyberShield URL ML model...")

model = joblib.load(MODEL_PATH)

print("URL Random Forest loaded successfully!")

print("Model classes:", model.classes_)


# =========================================================
# FEATURE ORDER
# =========================================================

FEATURE_COLUMNS = [

    "URLLength",
    "DomainLength",
    "IsDomainIP",
    "TLDLength",
    "NoOfSubDomain",
    "HasObfuscation",
    "NoOfObfuscatedChar",
    "ObfuscationRatio",
    "NoOfLettersInURL",
    "NoOfDegitsInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL"

]


# =========================================================
# URL PREDICTION
# =========================================================

def predict_url(url: str):

    # ---------------------------------------------
    # Extract ML features
    # ---------------------------------------------

    features = extract_url_features(url)


    # ---------------------------------------------
    # Create DataFrame
    # ---------------------------------------------

    X = pd.DataFrame(
        [features],
        columns=FEATURE_COLUMNS
    )


    # ---------------------------------------------
    # Model prediction
    # ---------------------------------------------

    prediction = int(model.predict(X)[0])


    # ---------------------------------------------
    # Get probabilities
    # ---------------------------------------------

    probabilities = model.predict_proba(X)[0]


    # =====================================================
    # IMPORTANT:
    #
    # Your model uses:
    #
    # 0 = PHISHING
    # 1 = LEGITIMATE
    #
    # model.classes_ = [0, 1]
    # =====================================================

    phishing_probability = probabilities[0]

    legitimate_probability = probabilities[1]


    # ---------------------------------------------
    # Classification
    # ---------------------------------------------

    if prediction == 0:

        classification = "PHISHING"

    else:

        classification = "LEGITIMATE"


    # ---------------------------------------------
    # Return result
    # ---------------------------------------------

    return {

        "classification": classification,

        "prediction": prediction,

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