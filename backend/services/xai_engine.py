# =========================================================
# CYBERSHIELD AI
# EXPLAINABLE AI ENGINE
# =========================================================


def generate_url_explanation(
    url,
    features,
    ml_analysis,
    rule_analysis,
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
    # EVIDENCE
    # =====================================================

    evidence = []


    # -----------------------------------------------------
    # IP ADDRESS
    # -----------------------------------------------------

    if features.get("IsDomainIP") == 1:

        evidence.append({
            "severity": "HIGH",
            "signal": "IP ADDRESS",
            "explanation":
                "The URL uses an IP address instead of a normal domain name."
        })


    # -----------------------------------------------------
    # HTTPS
    # -----------------------------------------------------

    if not features.get("uses_https", True):

        evidence.append({
            "severity": "MEDIUM",
            "signal": "NO HTTPS",
            "explanation":
                "The website does not use HTTPS, so the connection is not protected by TLS."
        })


    # -----------------------------------------------------
    # SUSPICIOUS WORDS
    # -----------------------------------------------------

    if features.get("has_suspicious_words", False):

        evidence.append({
            "severity": "MEDIUM",
            "signal": "SUSPICIOUS KEYWORDS",
            "explanation":
                "The URL contains words commonly associated with account verification, login, security, or payment activity."
        })


    # -----------------------------------------------------
    # SUBDOMAINS
    # -----------------------------------------------------

    subdomains = features.get(
        "NoOfSubDomain",
        features.get("number_of_dots", 0)
    )

    if subdomains >= 2:

        evidence.append({
            "severity": "MEDIUM",
            "signal": "MULTIPLE SUBDOMAINS",
            "explanation":
                f"The URL contains {subdomains} subdomain level(s), which can sometimes be used to make a domain appear more trustworthy."
        })


    # -----------------------------------------------------
    # OBFUSCATION
    # -----------------------------------------------------

    if features.get("HasObfuscation") == 1:

        evidence.append({
            "severity": "HIGH",
            "signal": "URL OBFUSCATION",
            "explanation":
                "The URL contains encoded or obfuscated characters that may hide its actual structure."
        })


    # -----------------------------------------------------
    # LONG URL
    # -----------------------------------------------------

    url_length = features.get(
        "URLLength",
        features.get("url_length", 0)
    )

    if url_length >= 75:

        evidence.append({
            "severity": "MEDIUM",
            "signal": "LONG URL",
            "explanation":
                f"The URL is unusually long ({url_length} characters), which can be associated with complex or deceptive URLs."
        })


    # =====================================================
    # ML EXPLANATION
    # =====================================================

    ml_explanation = []

    if ml_classification == "PHISHING":

        ml_explanation.append(
            f"The machine-learning model classified the URL as phishing with a {round(phishing_probability * 100, 2)}% phishing probability."
        )

    else:

        ml_explanation.append(
            f"The machine-learning model classified the URL as legitimate with a {round(legitimate_probability * 100, 2)}% legitimate probability."
        )


    # =====================================================
    # RULE EXPLANATION
    # =====================================================

    rule_explanation = []

    rule_reasons = rule_analysis.get(
        "reasons",
        []
    )

    for reason in rule_reasons:

        rule_explanation.append(reason)


    # =====================================================
    # SIGNAL ANALYSIS
    # =====================================================

    if agreement == "STRONG AGREEMENT":

        signal_explanation = (
            "The machine-learning model and rule-based engine "
            "are pointing in the same direction."
        )

    else:

        signal_explanation = (
            "The machine-learning model and rule-based engine "
            "produced different risk signals. The final score "
            "combines both signals to produce a balanced assessment."
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
            "Do not open the website or enter passwords, "
            "OTP, payment information, or other sensitive data."
        )

    elif classification == "SUSPICIOUS":

        recommendation = (
            "Proceed with caution. Verify the website through "
            "an official source before entering sensitive information."
        )

    else:

        recommendation = (
            "No strong phishing indicators were detected, "
            "but users should still follow normal security practices."
        )


    # =====================================================
    # RETURN
    # =====================================================

    return {

        "summary": (
            f"CyberShield classified this URL as "
            f"{classification} with a final risk score of "
            f"{final_score}/100."
        ),

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


# =========================================================
# MESSAGE XAI
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
    # MESSAGE SIGNALS
    # =====================================================

    signals = rule_analysis.get(
        "signals",
        {}
    )


    # =====================================================
    # EVIDENCE
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
                "The message uses urgency-related language that may pressure the recipient into acting quickly."
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
            "signal": "THREAT / CONSEQUENCE",
            "explanation":
                "The message contains threatening or consequence-based language designed to pressure the recipient."
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
            "signal": "FINANCIAL CONTENT",
            "explanation":
                "The message contains financial-related terms such as banking, payment, money, cards, transactions or OTPs."
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
            "signal": "CREDENTIAL REQUEST",
            "explanation":
                "The message references sensitive credentials or authentication information such as passwords, PINs, CVV or OTPs."
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
                "The message attempts to persuade the recipient to perform an action such as clicking, verifying, logging in or downloading."
        })


    # -----------------------------------------------------
    # EXTERNAL URL
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
                f"The message contains {len(urls)} external URL(s), which may direct the recipient to a malicious or fraudulent website."
        })


    # =====================================================
    # ML EXPLANATION
    # =====================================================

    ml_explanation = []

    if "PHISHING" in ml_classification:

        ml_explanation.append(
            f"The machine-learning model classified the message as phishing or social engineering with a {round(phishing_probability * 100, 2)}% phishing probability."
        )

    else:

        ml_explanation.append(
            f"The machine-learning model classified the message as legitimate with a {round(legitimate_probability * 100, 2)}% legitimate probability."
        )


    # =====================================================
    # RULE EXPLANATION
    # =====================================================

    rule_explanation = []

    rule_reasons = rule_analysis.get(
        "reasons",
        []
    )

    for reason in rule_reasons:

        rule_explanation.append(reason)


    # =====================================================
    # SIGNAL ANALYSIS
    # =====================================================

    if agreement == "STRONG AGREEMENT":

        signal_explanation = (
            "The machine-learning model and rule-based engine "
            "are pointing in the same direction."
        )

    else:

        signal_explanation = (
            "The machine-learning model and rule-based engine "
            "produced different risk signals. The final score "
            "combines both signals to produce a balanced assessment."
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
            "Do not follow links, provide OTPs, passwords, "
            "payment details or other sensitive information."
        )

    elif classification == "SUSPICIOUS":

        recommendation = (
            "Treat the message with caution. Verify the sender "
            "through an independent and trusted channel before taking action."
        )

    else:

        recommendation = (
            "No strong social engineering indicators were detected, "
            "but continue following normal security practices."
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
    # RETURN
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