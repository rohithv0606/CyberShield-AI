from backend.services.message_analyzer import analyze_message

from backend.services.message_ml import predict_message

from backend.services.message_fusion import calculate_message_risk


# =========================================================
# TEST MESSAGE
# =========================================================

message = """
Your Amazon order has been shipped and will arrive tomorrow.
"""


# =========================================================
# 1. RULE-BASED ANALYSIS
# =========================================================

print("\n")
print("=" * 60)
print("MESSAGE RULE ANALYSIS")
print("=" * 60)

rule_result = analyze_message(message)

print("Rule Risk Score:", rule_result["risk_score"])

print("Classification:", rule_result["classification"])

print("\nReasons:")

for reason in rule_result["reasons"]:

    print("-", reason)


# =========================================================
# 2. DISTILBERT ANALYSIS
# =========================================================

print("\n")
print("=" * 60)
print("DISTILBERT ANALYSIS")
print("=" * 60)

ml_result = predict_message(message)

print(
    "Classification:",
    ml_result["classification"]
)

print(
    "Phishing Probability:",
    ml_result["phishing_probability"] * 100,
    "%"
)

print(
    "Legitimate Probability:",
    ml_result["legitimate_probability"] * 100,
    "%"
)


# =========================================================
# 3. MESSAGE RISK FUSION
# =========================================================

print("\n")
print("=" * 60)
print("MESSAGE RISK FUSION")
print("=" * 60)

message_risk = calculate_message_risk(

    rule_result,

    ml_result["phishing_probability"]

)


# =========================================================
# 4. DISPLAY FINAL RESULT
# =========================================================

print(
    "Final Message Risk:",
    message_risk["final_risk_score"]
)

print(
    "Classification:",
    message_risk["classification"]
)

print(
    "DistilBERT Score:",
    message_risk["distilbert_score"]
)

print(
    "Rule Score:",
    message_risk["rule_score"]
)

print(
    "Signal Agreement:",
    message_risk["signal_agreement"]
)

print("=" * 60)