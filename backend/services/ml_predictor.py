import joblib
import pandas as pd
from pathlib import Path
# ==========================================
# LOAD TRAINED MODEL
# ==========================================
MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "ml"
    / "models"
    / "cybershield_url_model.joblib"
)
model = joblib.load(MODEL_PATH)
# ==========================================
# FEATURES EXPECTED BY THE MODEL
# ==========================================
FEATURES = [
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
# ==========================================
# PREDICTION FUNCTION
# ==========================================
def predict_url(features: dict):
    data = {}
    for feature in FEATURES:
        data[feature] = features.get(feature, 0)
    input_data = pd.DataFrame([data])
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    # Dataset:
    # 0 = phishing
    # 1 = legitimate
    phishing_probability = probabilities[0]
    legitimate_probability = probabilities[1]
    return {
        "prediction": int(prediction),
        "phishing_probability": float(phishing_probability),
        "legitimate_probability": float(legitimate_probability)
    }