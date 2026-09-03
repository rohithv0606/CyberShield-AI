import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)


# =========================================================
# HUGGING FACE MODEL
# =========================================================

MODEL_PATH = "Rohithv06/cybershield_distilbert"


# =========================================================
# DEVICE
# =========================================================

device = torch.device("cpu")


# =========================================================
# MODEL VARIABLES
# =========================================================

tokenizer = None
model = None


# =========================================================
# LOAD MODEL
# =========================================================

def load_model():

    global tokenizer
    global model

    # -----------------------------------------
    # Prevent loading multiple times
    # -----------------------------------------

    if model is not None:

        return


    print("======================================")
    print("Loading CyberShield NLP model...")
    print("Device: CPU")
    print("======================================")


    # -----------------------------------------
    # Load tokenizer
    # -----------------------------------------

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH
    )


    # -----------------------------------------
    # Load model
    # -----------------------------------------

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_PATH
    )


    # -----------------------------------------
    # CPU
    # -----------------------------------------

    model.to(device)

    model.eval()


    print("CyberShield DistilBERT loaded successfully!")


# =========================================================
# MESSAGE PREDICTION
# =========================================================

def predict_message(message: str):

    # -----------------------------------------
    # Load model only when required
    # -----------------------------------------

    load_model()


    # -----------------------------------------
    # Tokenize
    # -----------------------------------------

    inputs = tokenizer(
        message,
        return_tensors="pt",
        truncation=True,
        max_length=128
    )


    # -----------------------------------------
    # Move inputs to CPU
    # -----------------------------------------

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }


    # -----------------------------------------
    # Prediction
    # -----------------------------------------

    with torch.no_grad():

        outputs = model(**inputs)


    # -----------------------------------------
    # Probabilities
    # -----------------------------------------

    probabilities = torch.softmax(
        outputs.logits,
        dim=-1
    )


    # -----------------------------------------
    # 0 = legitimate
    # 1 = phishing
    # -----------------------------------------

    legitimate_probability = (
        probabilities[0][0].item()
    )

    phishing_probability = (
        probabilities[0][1].item()
    )


    # -----------------------------------------
    # Prediction
    # -----------------------------------------

    prediction = torch.argmax(
        probabilities,
        dim=-1
    ).item()


    # -----------------------------------------
    # Classification
    # -----------------------------------------

    if prediction == 1:

        classification = (
            "PHISHING / SOCIAL ENGINEERING"
        )

    else:

        classification = "LEGITIMATE"


    # -----------------------------------------
    # Return
    # -----------------------------------------

    return {

        "classification": classification,

        "prediction": prediction,

        "phishing_probability": round(
            phishing_probability,
            4
        ),

        "legitimate_probability": round(
            legitimate_probability,
            4
        )

    }