import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


# =========================================================
# MODEL LOCATION
# =========================================================

MODEL_PATH = "./ml/message_model/cybershield_distilbert"


# =========================================================
# DEVICE
# =========================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("\n========== DEVICE ==========")
print("Using:", device)

if torch.cuda.is_available():
    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )


# =========================================================
# LOAD MODEL
# =========================================================

print("\n========== LOADING MODEL ==========")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH
)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.to(device)

model.eval()

print("Model loaded successfully!")


# =========================================================
# MESSAGE PREDICTION FUNCTION
# =========================================================

def predict_message(message):

    inputs = tokenizer(
        message,
        return_tensors="pt",
        truncation=True,
        max_length=128
    )

    inputs = {
        key: value.to(device)
        for key, value in inputs.items()
    }

    with torch.no_grad():

        outputs = model(**inputs)

    probabilities = torch.softmax(
        outputs.logits,
        dim=-1
    )

    prediction = torch.argmax(
        probabilities,
        dim=-1
    ).item()

    safe_probability = probabilities[0][0].item()
    phishing_probability = probabilities[0][1].item()

    if prediction == 1:
        classification = "PHISHING / SOCIAL ENGINEERING"
    else:
        classification = "LEGITIMATE"

    return {
        "classification": classification,
        "safe_probability": safe_probability,
        "phishing_probability": phishing_probability
    }


# =========================================================
# TEST MESSAGES
# =========================================================

messages = [

    "Hey, are we meeting at 5 PM today?",

    "URGENT! Your bank account has been suspended. "
    "Click the link immediately and verify your password.",

    "Your Amazon order has been shipped and will arrive tomorrow.",

    "Congratulations! You have won a $1000 prize. "
    "Send your account details to claim it."
]


# =========================================================
# RUN PREDICTIONS
# =========================================================

print("\n")
print("==============================================")
print("          CYBERSHIELD MESSAGE TEST")
print("==============================================")


for message in messages:

    result = predict_message(message)

    print("\nMessage:")
    print(message)

    print("\nPrediction:")
    print(result["classification"])

    print(
        "Safe probability:",
        round(
            result["safe_probability"] * 100,
            2
        ),
        "%"
    )

    print(
        "Phishing probability:",
        round(
            result["phishing_probability"] * 100,
            2
        ),
        "%"
    )

    print("----------------------------------------------")