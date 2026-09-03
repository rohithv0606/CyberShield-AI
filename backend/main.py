from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# =========================================================
# CYBERSHIELD SERVICES
# =========================================================

from backend.services.url_analyzer import analyze_url
from backend.services.url_ml import predict_url
from backend.services.risk_engine import calculate_risk
from backend.services.risk_fusion import calculate_fused_risk

from backend.services.message_analyzer import analyze_message
from backend.services.message_ml import predict_message

from backend.services.xai_engine import generate_url_explanation
from backend.services.message_xai import generate_message_explanation


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="CyberShield AI",
    description="AI-powered phishing and social engineering detection system",
    version="1.0"
)


# =========================================================
# CORS CONFIGURATION
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# REQUEST MODELS
# =========================================================

class URLRequest(BaseModel):
    url: str


class MessageRequest(BaseModel):
    message: str


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "CyberShield AI is running!"
    }


# =========================================================
# URL SCANNING
# =========================================================

@app.post("/scan/url")
def scan_url(request: URLRequest):

    # =====================================================
    # 1. URL RULE-BASED ANALYSIS
    # =====================================================

    features = analyze_url(
        request.url
    )

    rule_analysis = calculate_risk(
        features
    )


    # =====================================================
    # 2. URL MACHINE LEARNING ANALYSIS
    # =====================================================

    ml_analysis = predict_url(
        features
    )


    # =====================================================
    # 3. GET PHISHING PROBABILITY
    # =====================================================

    phishing_probability = ml_analysis.get(
        "phishing_probability",
        0
    )


    # =====================================================
    # 4. RISK FUSION
    # =====================================================

    risk_fusion = calculate_fused_risk(
        rule_analysis,
        phishing_probability
    )


    # =====================================================
    # 5. URL EXPLAINABLE AI
    # =====================================================

    explanation = generate_url_explanation(
        request.url,
        features,
        ml_analysis,
        rule_analysis,
        risk_fusion
    )


    # =====================================================
    # 6. FINAL RESPONSE
    # =====================================================

    return {

        "type": "URL",

        "url": request.url,

        "rule_analysis": rule_analysis,

        "ml_analysis": ml_analysis,

        "risk_fusion": risk_fusion,

        "explanation": explanation,

        "features": features

    }


# =========================================================
# MESSAGE SCANNING
# =========================================================

@app.post("/scan/message")
def scan_message(request: MessageRequest):

    # =====================================================
    # 1. MESSAGE RULE-BASED ANALYSIS
    # =====================================================

    rule_analysis = analyze_message(
        request.message
    )


    # =====================================================
    # 2. DISTILBERT ML ANALYSIS
    # =====================================================

    ml_analysis = predict_message(
        request.message
    )


    # =====================================================
    # 3. GET PHISHING PROBABILITY
    # =====================================================

    phishing_probability = ml_analysis.get(
        "phishing_probability",
        0
    )


    # =====================================================
    # 4. RISK FUSION
    # =====================================================

    risk_fusion = calculate_fused_risk(
        rule_analysis,
        phishing_probability
    )


    # =====================================================
    # 5. MESSAGE EXPLAINABLE AI
    # =====================================================

    explanation = generate_message_explanation(
        request.message,
        rule_analysis,
        ml_analysis,
        risk_fusion
    )


    # =====================================================
    # 6. FINAL RESPONSE
    # =====================================================

    return {

        "type": "MESSAGE",

        "message": request.message,

        "rule_analysis": rule_analysis,

        "ml_analysis": ml_analysis,

        "risk_fusion": risk_fusion,

        "explanation": explanation

    }