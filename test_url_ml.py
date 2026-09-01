from backend.services.url_ml import predict_url


# =========================================================
# TEST URL
# =========================================================

url = "http://192.168.1.50/login/verify/account"


# =========================================================
# PREDICTION
# =========================================================

result = predict_url(url)


# =========================================================
# DISPLAY RESULT
# =========================================================

print("\n")
print("=" * 60)
print("CYBERSHIELD URL ML ANALYSIS")
print("=" * 60)

print("\nURL:")
print(url)

print("\nClassification:")
print(result["classification"])

print("\nPrediction:")
print(result["prediction"])

print("\nPhishing Probability:")
print(
    result["phishing_probability"] * 100,
    "%"
)

print("\nLegitimate Probability:")
print(
    result["legitimate_probability"] * 100,
    "%"
)

print("\nFeatures:")

for feature, value in result["features"].items():

    print(
        f"{feature}: {value}"
    )

print("=" * 60)