from urllib.parse import urlparse
import re
def analyze_url(url: str):
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    features = {
        "url_length": len(url),
        "uses_https": parsed.scheme == "https",
        "hostname_length": len(hostname),
        "number_of_dots": hostname.count("."),
        "number_of_hyphens": hostname.count("-"),
        "has_ip_address": False,
        "has_at_symbol": "@" in url,
        "has_suspicious_words": False
    }
    # Check whether hostname is an IP address
    ip_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    if re.match(ip_pattern, hostname):
        features["has_ip_address"] = True
    # Words commonly associated with phishing URLs
    suspicious_words = [
        "login",
        "verify",
        "verification",
        "account",
        "secure",
        "update",
        "password",
        "bank",
        "confirm",
        "wallet"
    ]
    url_lower = url.lower()
    for word in suspicious_words:
        if word in url_lower:
            features["has_suspicious_words"] = True
            break
    return features