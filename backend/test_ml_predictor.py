from services.url_feature_extractor import extract_url_features
from services.ml_predictor import predict_url


# ==========================================
# TEST URL
# ==========================================

test_url = "https://example.com/login?user=test"


# ==========================================
# EXTRACT FEATURES
# ==========================================

features = extract_url_features(test_url)


print("\n========== EXTRACTED FEATURES ==========\n")

for feature, value in features.items():
    print(f"{feature}: {value}")


# ==========================================
# ML PREDICTION
# ==========================================

result = predict_url(features)


print("\n========== ML PREDICTION ==========\n")

print("Prediction:", result["prediction"])

print(
    "Phishing Probability:",
    round(result["phishing_probability"], 4)
)

print(
    "Legitimate Probability:",
    round(result["legitimate_probability"], 4)
)