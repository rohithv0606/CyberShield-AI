import re


# =========================================================
# SOCIAL ENGINEERING PATTERNS
# =========================================================

URGENCY_WORDS = [
    "urgent",
    "immediately",
    "now",
    "today",
    "within 24 hours",
    "act fast",
    "hurry",
    "last chance",
    "expires",
    "deadline"
]


THREAT_WORDS = [
    "blocked",
    "suspended",
    "terminated",
    "closed",
    "legal action",
    "police",
    "arrest",
    "penalty",
    "fine",
    "account will be closed"
]


FINANCIAL_WORDS = [
    "bank",
    "payment",
    "refund",
    "money",
    "credit card",
    "debit card",
    "transaction",
    "upi",
    "otp",
    "salary",
    "invoice"
]


CREDENTIAL_WORDS = [
    "password",
    "username",
    "login",
    "sign in",
    "verify your account",
    "verification",
    "otp",
    "pin",
    "cvv",
    "card number"
]


ACTION_WORDS = [
    "click",
    "open",
    "verify",
    "confirm",
    "update",
    "login",
    "sign in",
    "download",
    "send",
    "reply"
]


# =========================================================
# HELPER FUNCTION
# =========================================================

def count_matches(text, words):

    text = text.lower()

    matches = []

    for word in words:

        if word in text:
            matches.append(word)

    return matches


# =========================================================
# MESSAGE ANALYZER
# =========================================================

def analyze_message(message: str):

    text = message.lower()

    # -----------------------------------------------------
    # Detect categories
    # -----------------------------------------------------

    urgency = count_matches(
        text,
        URGENCY_WORDS
    )

    threats = count_matches(
        text,
        THREAT_WORDS
    )

    financial = count_matches(
        text,
        FINANCIAL_WORDS
    )

    credentials = count_matches(
        text,
        CREDENTIAL_WORDS
    )

    actions = count_matches(
        text,
        ACTION_WORDS
    )


    # -----------------------------------------------------
    # Detect URLs
    # -----------------------------------------------------

    urls = re.findall(
        r"https?://[^\s]+",
        message
    )


    # -----------------------------------------------------
    # Calculate risk
    # -----------------------------------------------------

    risk_score = 0

    risk_score += min(
        len(urgency) * 10,
        25
    )

    risk_score += min(
        len(threats) * 15,
        30
    )

    risk_score += min(
        len(financial) * 8,
        20
    )

    risk_score += min(
        len(credentials) * 12,
        30
    )

    risk_score += min(
        len(actions) * 5,
        15
    )

    if urls:
        risk_score += 10


    # -----------------------------------------------------
    # Keep score between 0 and 100
    # -----------------------------------------------------

    risk_score = min(
        risk_score,
        100
    )


    # -----------------------------------------------------
    # Classification
    # -----------------------------------------------------

    if risk_score >= 70:

        classification = "HIGH RISK"

    elif risk_score >= 40:

        classification = "SUSPICIOUS"

    else:

        classification = "LOW RISK"


    # -----------------------------------------------------
    # Generate explanations
    # -----------------------------------------------------

    reasons = []

    if urgency:

        reasons.append(
            "Message uses urgency or time-pressure language"
        )

    if threats:

        reasons.append(
            "Message contains threatening or consequence-based language"
        )

    if financial:

        reasons.append(
            "Message contains financial-related language"
        )

    if credentials:

        reasons.append(
            "Message requests or references sensitive credentials"
        )

    if actions:

        reasons.append(
            "Message attempts to make the user perform an action"
        )

    if urls:

        reasons.append(
            "Message contains an external URL"
        )


    # -----------------------------------------------------
    # Return analysis
    # -----------------------------------------------------

    return {

        "risk_score": risk_score,

        "classification": classification,

        "reasons": reasons,

        "signals": {

            "urgency": urgency,

            "threats": threats,

            "financial": financial,

            "credential_request": credentials,

            "action_pressure": actions,

            "urls_detected": urls

        }

    }