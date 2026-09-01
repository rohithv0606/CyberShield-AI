from services.url_feature_extractor import extract_url_features
test_url = "https://example.com/login?user=test"
features = extract_url_features(test_url)
print("\n========== URL FEATURES ==========\n")
for feature, value in features.items():
    print(f"{feature}: {value}")