from backend.services.url_analyzer import analyze_url

from backend.services.risk_engine import calculate_risk

from backend.services.url_ml import predict_url

from backend.services.url_fusion import calculate_url_risk


# =========================================================
# TEST URL
# =========================================================

url = "http://192.168.1.50/login/verify/account"


# =========================================================
# 1. URL FEATURE ANALYSIS
# =========================================================

print("\n")
print("=" * 60)
print("URL FEATURE ANALYSIS")
print("=" * 60)

features = analyze_url(url)

print("\nURL:")
print(url)

print("\nFeatures:")

for feature, value in features.items():

    print(f"{feature}: {value}")


# =========================================================
# 2. RULE ENGINE
# =========================================================

print("\n")
print("=" * 60)
print("URL RULE ENGINE")
print("=" * 60)

rule_result = calculate_risk(features)

print("\nRule Risk Score:")
print(rule_result["risk_score"])

print("\nRule Classification:")
print(rule_result["classification"])

print("\nReasons:")

for reason in rule_result["reasons"]:

    print("-", reason)


# =========================================================
# 3. RANDOM FOREST
# =========================================================

print("\n")
print("=" * 60)
print("URL RANDOM FOREST")
print("=" * 60)

ml_result = predict_url(url)

print("\nClassification:")
print(ml_result["classification"])

print("\nPrediction:")
print(ml_result["prediction"])

print("\nPhishing Probability:")
print(
    ml_result["phishing_probability"] * 100,
    "%"
)

print("\nLegitimate Probability:")
print(
    ml_result["legitimate_probability"] * 100,
    "%"
)


# =========================================================
# 4. URL RISK FUSION
# =========================================================

print("\n")
print("=" * 60)
print("URL RISK FUSION")
print("=" * 60)

final_result = calculate_url_risk(

    rule_result,

    ml_result["phishing_probability"]

)


# =========================================================
# 5. FINAL RESULT
# =========================================================

print("\nFinal URL Risk:")
print(
    final_result["final_risk_score"]
)

print("\nClassification:")
print(
    final_result["classification"]
)

print("\nML Score:")
print(
    final_result["ml_score"]
)

print("\nRule Score:")
print(
    final_result["rule_score"]
)

print("\nSignal Agreement:")
print(
    final_result["signal_agreement"]
)

print("\n" + "=" * 60)