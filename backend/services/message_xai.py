# =========================================================
# CYBERSHIELD AI
# MESSAGE EXPLAINABLE AI ENGINE
# =========================================================


def generate_message_explanation(
    message,
    rule_analysis,
    ml_analysis,
    risk_fusion
):

    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    final_score = risk_fusion.get(
        "final_risk_score",
        0
    )

    classification = risk_fusion.get(
        "classification",
        "UNKNOWN"
    )

    ml_score = risk_fusion.get(
        "ml_score",
        0
    )

    rule_score = risk_fusion.get(
        "rule_score",
        0
    )

    agreement = risk_fusion.get(
        "signal_agreement",
        "UNKNOWN"
    )


    # =====================================================
    # ML INFORMATION
    # =====================================================

    phishing_probability = ml_analysis.get(
        "phishing_probability",
        0
    )

    legitimate_probability = ml_analysis.get(
        "legitimate_probability",
        0
    )

    ml_classification = ml_analysis.get(
        "classification",
        "UNKNOWN"
    )


    # =====================================================
    # SIGNALS FROM RULE ENGINE
    # =====================================================

    signals = rule_analysis.get(
        "signals",
        {}
    )


    # =====================================================
    # EVIDENCE COLLECTION
    # =====================================================

    evidence = []


    # -----------------------------------------------------
    # URGENCY
    # -----------------------------------------------------

    urgency = signals.get(
        "urgency",
        []
    )

    if urgency:

        evidence.append({
            "severity": "MEDIUM",
            "signal": "URGENCY / TIME PRESSURE",
            "explanation":
                "The message uses urgency-related language that may pressure the user into acting quickly.",
            "detected": urgency
        })


    # -----------------------------------------------------
    # THREATS
    # -----------------------------------------------------

    threats = signals.get(
        "threats",
        []
    )

    if threats:

        evidence.append({
            "severity": "HIGH",
            "signal": "THREAT / CONSEQUENCE LANGUAGE",
            "explanation":
                "The message contains threatening or consequence-based language designed to create fear or pressure.",
            "detected": threats
        })


    # -----------------------------------------------------
    # FINANCIAL
    # -----------------------------------------------------

    financial = signals.get(
        "financial",
        []
    )

    if financial:

        evidence.append({
            "severity": "HIGH",
            "signal": "FINANCIAL LANGUAGE",
            "explanation":
                "The message contains financial-related terms that may indicate an attempt to obtain money or financial information.",
            "detected": financial
        })


    # -----------------------------------------------------
    # CREDENTIALS
    # -----------------------------------------------------

    credentials = signals.get(
        "credential_request",
        []
    )

    if credentials:

        evidence.append({
            "severity": "HIGH",
            "signal": "CREDENTIAL / SENSITIVE INFORMATION",
            "explanation":
                "The message references passwords, login details, OTPs, PINs, card information, or other sensitive credentials.",
            "detected": credentials
        })


    # -----------------------------------------------------
    # ACTION PRESSURE
    # -----------------------------------------------------

    actions = signals.get(
        "action_pressure",
        []
    )

    if actions:

        evidence.append({
            "severity": "MEDIUM",
            "signal": "ACTION REQUEST",
            "explanation":
                "The message attempts to persuade the user to perform an action such as clicking, verifying, updating, downloading, or replying.",
            "detected": actions
        })


    # -----------------------------------------------------
    # URL
    # -----------------------------------------------------

    urls = signals.get(
        "urls_detected",
        []
    )

    if urls:

        evidence.append({
            "severity": "HIGH",
            "signal": "EXTERNAL URL",
            "explanation":
                "The message contains an external URL. Links in unsolicited messages can redirect users to phishing or malicious websites.",
            "detected": urls
        })


    # =====================================================
    # ML EXPLANATION
    # =====================================================

    ml_explanation = []

    if ml_classification == "PHISHING / SOCIAL ENGINEERING":

        ml_explanation.append(
            "The machine-learning model classified this message "
            f"as phishing/social engineering with a "
            f"{round(phishing_probability * 100, 2)}% phishing probability."
        )

    else:

        ml_explanation.append(
            "The machine-learning model classified this message "
            f"as legitimate with a "
            f"{round(legitimate_probability * 100, 2)}% legitimate probability."
        )


    # =====================================================
    # RULE EXPLANATION
    # =====================================================

    rule_explanation = rule_analysis.get(
        "reasons",
        []
    )


    # =====================================================
    # SIGNAL ANALYSIS
    # =====================================================

    if agreement == "STRONG AGREEMENT":

        signal_explanation = (
            "The machine-learning model and rule-based engine "
            "produced consistent risk signals. Both analytical "
            "approaches support the final assessment."
        )

    else:

        signal_explanation = (
            "The machine-learning model and rule-based engine "
            "produced different risk signals. The final score "
            "combines both signals to provide a balanced assessment."
        )


    # =====================================================
    # CONTRIBUTION
    # =====================================================

    ml_contribution = round(
        ml_score * 0.65,
        2
    )

    rule_contribution = round(
        rule_score * 0.35,
        2
    )


    # =====================================================
    # RECOMMENDATION
    # =====================================================

    if classification == "HIGH RISK":

        recommendation = (
            "Do not follow links, reply to the message, "
            "share passwords, OTPs, payment information, "
            "or other sensitive data. Verify the request "
            "through an official channel."
        )

    elif classification == "SUSPICIOUS":

        recommendation = (
            "Treat this message with caution. Do not click "
            "unknown links or provide sensitive information. "
            "Verify the sender and request through an official source."
        )

    else:

        recommendation = (
            "No strong social-engineering indicators were detected, "
            "but continue to follow normal security practices "
            "when handling unexpected messages."
        )


    # =====================================================
    # SUMMARY
    # =====================================================

    summary = (
        f"CyberShield classified this message as "
        f"{classification} with a final risk score of "
        f"{final_score}/100."
    )


    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    return {

        "summary": summary,

        "risk_score": final_score,

        "classification": classification,

        "ml_explanation": ml_explanation,

        "rule_explanation": rule_explanation,

        "evidence": evidence,

        "signal_analysis": signal_explanation,

        "contribution": {

            "ml_contribution": ml_contribution,

            "rule_contribution": rule_contribution

        },

        "recommendation": recommendation

    }
