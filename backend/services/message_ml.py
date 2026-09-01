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

if torch.cuda.is_available():

    device = torch.device("cuda")

    print("======================================")
    print("CyberShield NLP using GPU")
    print("GPU:", torch.cuda.get_device_name(0))
    print("======================================")

else:

    device = torch.device("cpu")

    print("======================================")
    print("CyberShield NLP using CPU")
    print("======================================")


# =========================================================
# LOAD TOKENIZER
# =========================================================

print("Loading CyberShield NLP tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH
)


# =========================================================
# LOAD DISTILBERT
# =========================================================

print("Loading CyberShield DistilBERT model...")

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)


# =========================================================
# MOVE MODEL TO DEVICE
# =========================================================

model.to(device)

model.eval()


print("CyberShield DistilBERT loaded successfully!")


# =========================================================
# MESSAGE PREDICTION
# =========================================================

def predict_message(message: str):

    # -----------------------------------------------------
    # TOKENIZE
    # -----------------------------------------------------

    inputs = tokenizer(
        message,
        return_tensors="pt",
        truncation=True,
        max_length=128
    )


    # -----------------------------------------------------
    # MOVE INPUT TO DEVICE
    # -----------------------------------------------------

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }


    # -----------------------------------------------------
    # MODEL PREDICTION
    # -----------------------------------------------------

    with torch.no_grad():

        outputs = model(**inputs)


    # -----------------------------------------------------
    # CONVERT LOGITS TO PROBABILITIES
    # -----------------------------------------------------

    probabilities = torch.softmax(
        outputs.logits,
        dim=-1
    )


    # =====================================================
    # MODEL LABEL ASSUMPTION
    #
    # 0 = LEGITIMATE
    # 1 = PHISHING
    # =====================================================

    legitimate_probability = (
        probabilities[0][0].item()
    )

    phishing_probability = (
        probabilities[0][1].item()
    )


    # -----------------------------------------------------
    # PREDICTION
    # -----------------------------------------------------

    prediction = torch.argmax(
        probabilities,
        dim=-1
    ).item()


    # -----------------------------------------------------
    # CLASSIFICATION
    # -----------------------------------------------------

    if prediction == 1:

        classification = (
            "PHISHING / SOCIAL ENGINEERING"
        )

    else:

        classification = "LEGITIMATE"


    # -----------------------------------------------------
    # RETURN
    # -----------------------------------------------------

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