import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)
# ==========================================
# 1. LOAD DATASET
# ==========================================
DATASET_PATH = "ml/dataset/PhiUSIIL_Phishing_URL_Dataset.csv"
df = pd.read_csv(DATASET_PATH)
print("Dataset loaded!")
print("Shape:", df.shape)
# ==========================================
# 2. SELECT URL-ONLY FEATURES
# ==========================================
features = [
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
X = df[features].copy()
y = df["label"].copy()
# ==========================================
# 3. REMOVE DUPLICATE URLs
# ==========================================
before = len(df)
df = df.drop_duplicates(subset=["URL"]).reset_index(drop=True)
print("\nDuplicate URLs removed:", before - len(df))
# Recreate X and y after removing duplicates
X = df[features].copy()
y = df["label"].copy()

# ==========================================
# 4. EXTRACT DOMAIN
# ==========================================
from urllib.parse import urlparse
def extract_domain(url):
    try:
        domain = urlparse(url).netloc.lower()
        # Remove port if present
        domain = domain.split(":")[0]
        # Remove www.
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except:
        return ""
df["domain_group"] = df["URL"].apply(extract_domain)
print("\nUnique domains:", df["domain_group"].nunique())
# ==========================================
# 5. DOMAIN-BASED SPLIT
# ==========================================
from sklearn.model_selection import GroupShuffleSplit
splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42
)
train_idx, test_idx = next(
    splitter.split(
        X,
        y,
        groups=df["domain_group"]
    )
)
X_train = X.iloc[train_idx]
X_test = X.iloc[test_idx]
y_train = y.iloc[train_idx]
y_test = y.iloc[test_idx]
print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))
# ==========================================
# 6. TRAIN RANDOM FOREST
# ==========================================
print("\nTraining domain-aware model...")
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
print("Training complete!")
# ==========================================
# 7. PREDICTIONS
# ==========================================
y_pred = model.predict(X_test)
# ==========================================
# 8. EVALUATION
# ==========================================
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
print("\n========== DOMAIN-AWARE PERFORMANCE ==========")
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print("\n========== CLASSIFICATION REPORT ==========")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Phishing", "Legitimate"]
    )
)
print("\n========== CONFUSION MATRIX ==========")
print(confusion_matrix(y_test, y_pred))
# ==========================================
# 9. SAVE MODEL
# ==========================================
MODEL_PATH = "ml/models/cybershield_url_model.joblib"
joblib.dump(model, MODEL_PATH)
print("\nModel saved successfully!")
print("Saved to:", MODEL_PATH)