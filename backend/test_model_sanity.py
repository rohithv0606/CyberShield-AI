import pandas as pd
import joblib


# ==========================================
# LOAD DATASET
# ==========================================

DATASET_PATH = "ml/dataset/PhiUSIIL_Phishing_URL_Dataset.csv"

df = pd.read_csv(DATASET_PATH)


# ==========================================
# FEATURES USED BY OUR MODEL
# ==========================================

FEATURES = [
    "URLLength",
    "DomainLength",
    "IsDomainIP",
    "TLDLength",
    "NoOfSubDomain",
    "HasObfuscation",
    "NoOfObfuscatedChar",
    "ObfuscationRatio",
    "NoOfLettersInURL",
    "NoOfDegitsInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL"
]


# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load(
    "ml/models/cybershield_url_model.joblib"
)


# ==========================================
# SHOW LABEL DISTRIBUTION
# ==========================================

print("\n========== LABEL DISTRIBUTION ==========\n")

print(df["label"].value_counts())

print("\n0 = Phishing")
print("1 = Legitimate")


# ==========================================
# TEST REAL DATASET ROWS
# ==========================================

print("\n========== MODEL SANITY TEST ==========\n")


sample = df.sample(
    10,
    random_state=42
)


X_sample = sample[FEATURES]

predictions = model.predict(X_sample)


for i, (index, row) in enumerate(sample.iterrows()):

    actual = int(row["label"])
    predicted = int(predictions[i])

    actual_name = (
        "PHISHING"
        if actual == 0
        else "LEGITIMATE"
    )

    predicted_name = (
        "PHISHING"
        if predicted == 0
        else "LEGITIMATE"
    )

    print(f"\nURL: {row['URL']}")
    print(f"Actual    : {actual_name}")
    print(f"Predicted : {predicted_name}")