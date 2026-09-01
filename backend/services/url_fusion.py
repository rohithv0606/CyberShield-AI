def calculate_url_risk(rule_risk, phishing_probability):
    """
    Combines URL rule-based risk and Random Forest
    phishing probability into one explainable score.
    """

    # ==========================================
    # RULE SCORE
    # ==========================================

    rule_score = rule_risk.get("risk_score", 0)

    rule_score = max(0, min(rule_score, 100))


    # ==========================================
    # ML SCORE
    # ==========================================

    ml_score = phishing_probability * 100

    ml_score = max(0, min(ml_score, 100))


    # ==========================================
    # WEIGHTED FUSION
    # ==========================================

    final_score = (
        (ml_score * 0.65) +
        (rule_score * 0.35)
    )

    final_score = round(final_score, 2)


    # ==========================================
    # CLASSIFICATION
    # ==========================================

    if final_score >= 75:

        classification = "HIGH RISK"

    elif final_score >= 45:

        classification = "SUSPICIOUS"

    else:

        classification = "LOW RISK"


    # ==========================================
    # SIGNAL AGREEMENT
    # ==========================================

    if ml_score >= 50 and rule_score >= 50:

        agreement = "STRONG AGREEMENT"

    elif ml_score < 50 and rule_score < 50:

        agreement = "STRONG AGREEMENT"

    else:

        agreement = "SIGNALS DISAGREE"


    # ==========================================
    # RETURN
    # ==========================================

    return {

        "final_risk_score": final_score,

        "classification": classification,

        "ml_score": round(ml_score, 2),

        "rule_score": rule_score,

        "signal_agreement": agreement

    }