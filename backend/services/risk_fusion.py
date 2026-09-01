def calculate_fused_risk(rule_risk, phishing_probability):

    # ==========================================
    # EXTRACT SCORES
    # ==========================================

    rule_score = rule_risk.get("risk_score", 0)

    # Keep rule score between 0 and 100
    rule_score = max(0, min(rule_score, 100))

    # Convert ML probability (0-1) to score (0-100)
    ml_score = phishing_probability * 100

    # Keep ML score between 0 and 100
    ml_score = max(0, min(ml_score, 100))


    # ==========================================
    # NORMAL WEIGHTED FUSION
    # ==========================================

    # ML = 65%
    # Rules = 35%

    final_score = (
        (ml_score * 0.65) +
        (rule_score * 0.35)
    )


    # ==========================================
    # SECURITY OVERRIDE
    # ==========================================

    # Prevent a strong rule-based warning from
    # being completely ignored by a low ML score.

    if rule_score >= 70 and ml_score < 50:

        final_score = max(final_score, 70)

    elif rule_score >= 45 and ml_score < 20:

        final_score = max(final_score, 45)


    # ==========================================
    # ROUND SCORE
    # ==========================================

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

    # Both systems detect high risk
    if ml_score >= 50 and rule_score >= 50:

        agreement = "STRONG AGREEMENT"

    # Both systems detect low risk
    elif ml_score < 30 and rule_score < 30:

        agreement = "STRONG AGREEMENT"

    # One system detects risk while the other does not
    else:

        agreement = "SIGNALS DISAGREE"


    # ==========================================
    # RETURN RESULT
    # ==========================================

    return {

        "final_risk_score": final_score,

        "classification": classification,

        "ml_score": round(ml_score, 2),

        "rule_score": rule_score,

        "signal_agreement": agreement

    }