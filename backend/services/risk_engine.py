def calculate_risk(features):

    risk_score = 0
    reasons = []

    # ==========================================
    # HTTPS
    # ==========================================

    if not features.get("uses_https", True):
        risk_score += 20
        reasons.append("Website does not use HTTPS")


    # ==========================================
    # IP ADDRESS
    # ==========================================

    if features.get("IsDomainIP", 0) == 1:
        risk_score += 25
        reasons.append(
            "URL uses an IP address instead of a domain name"
        )


    # ==========================================
    # MANY SUBDOMAINS
    # ==========================================

    if features.get("NoOfSubDomain", 0) >= 2:
        risk_score += 20
        reasons.append(
            "URL contains many subdomains"
        )


    # ==========================================
    # LONG URL
    # ==========================================

    if features.get("URLLength", 0) > 75:
        risk_score += 10
        reasons.append(
            "URL is unusually long"
        )


    # ==========================================
    # OBFUSCATION
    # ==========================================

    if features.get("HasObfuscation", 0) == 1:
        risk_score += 15
        reasons.append(
            "URL contains obfuscated characters"
        )


    # ==========================================
    # MANY SPECIAL CHARACTERS
    # ==========================================

    if features.get("NoOfOtherSpecialCharsInURL", 0) > 10:
        risk_score += 10
        reasons.append(
            "URL contains many special characters"
        )


    # ==========================================
    # SUSPICIOUS PARAMETERS
    # ==========================================

    if features.get("NoOfQMarkInURL", 0) > 1:
        risk_score += 5
        reasons.append(
            "URL contains multiple query parameters"
        )


    # ==========================================
    # KEEP SCORE 0-100
    # ==========================================

    risk_score = min(risk_score, 100)


    # ==========================================
    # CLASSIFICATION
    # ==========================================

    if risk_score >= 75:

        classification = "HIGH RISK"

    elif risk_score >= 45:

        classification = "SUSPICIOUS"

    else:

        classification = "LOW RISK"


    # ==========================================
    # RETURN RESULT
    # ==========================================

    return {

        "risk_score": risk_score,

        "classification": classification,

        "reasons": reasons

    }