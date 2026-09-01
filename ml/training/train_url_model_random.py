import pandas as pd
from sklearn.model_selection import train_test_split
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
# 2. SELECT FEATURES
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
X = df[features]
# UCI:
# 1 = legitimate
# 0 = phishing
y = df["label"]
print("\nFeatures used:")
print(features)
print("\nTarget distribution:")
print(y.value_counts())
# ==========================================
# 3. TRAIN / TEST SPLIT
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)
print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))
# ==========================================
# 4. CREATE MODEL
# ==========================================
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)
# ==========================================
# 5. TRAIN MODEL
# ==========================================
print("\nTraining model...")
model.fit(X_train, y_train)
print("Training complete!")
# ==========================================
# 6. MAKE PREDICTIONS
# ==========================================
y_pred = model.predict(X_test)
# ==========================================
# 7. EVALUATE MODEL
# ==========================================
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
print("\n========== MODEL PERFORMANCE ==========")
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
# 8. FEATURE IMPORTANCE
# ==========================================
importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})
importance = importance.sort_values(
    by="importance",
    ascending=False
)
print("\n========== FEATURE IMPORTANCE ==========")
print(importance)