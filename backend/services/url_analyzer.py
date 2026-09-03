from urllib.parse import urlparse
import re


# =========================================================
# URL ANALYZER
# Features MUST match the Random Forest training features
# =========================================================

def analyze_url(url: str):

    parsed = urlparse(url)

    hostname = parsed.hostname or ""

    # -----------------------------------------------------
    # Basic URL information
    # -----------------------------------------------------

    url_length = len(url)

    domain_length = len(hostname)

    # -----------------------------------------------------
    # Check if hostname is an IPv4 address
    # -----------------------------------------------------

    ip_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"

    is_domain_ip = 1 if re.match(
        ip_pattern,
        hostname
    ) else 0

    # -----------------------------------------------------
    # TLD
    # -----------------------------------------------------

    if "." in hostname:

        tld = hostname.rsplit(".", 1)[-1]

    else:

        tld = ""

    tld_length = len(tld)

    # -----------------------------------------------------
    # Number of subdomains
    #
    # example:
    # www.google.com
    # google.com = main domain
    # www = subdomain
    #
    # therefore:
    # dots - 1
    # -----------------------------------------------------

    no_of_subdomain = max(
        hostname.count(".") - 1,
        0
    )

    # -----------------------------------------------------
    # Obfuscation
    #
    # %20
    # %3A
    # %2F
    # etc.
    # -----------------------------------------------------

    obfuscated_matches = re.findall(
        r"%[0-9a-fA-F]{2}",
        url
    )

    no_of_obfuscated_char = len(
        obfuscated_matches
    )

    has_obfuscation = (
        1
        if no_of_obfuscated_char > 0
        else 0
    )

    # -----------------------------------------------------
    # Obfuscation ratio
    # -----------------------------------------------------

    if url_length > 0:

        obfuscation_ratio = (
            no_of_obfuscated_char / url_length
        )

    else:

        obfuscation_ratio = 0

    # -----------------------------------------------------
    # Letters
    # -----------------------------------------------------

    no_of_letters = sum(
        1
        for char in url
        if char.isalpha()
    )

    # -----------------------------------------------------
    # Digits
    # -----------------------------------------------------

    no_of_digits = sum(
        1
        for char in url
        if char.isdigit()
    )

    # -----------------------------------------------------
    # Equals
    # -----------------------------------------------------

    no_of_equals = url.count("=")

    # -----------------------------------------------------
    # Question marks
    # -----------------------------------------------------

    no_of_qmark = url.count("?")

    # -----------------------------------------------------
    # Ampersands
    # -----------------------------------------------------

    no_of_ampersand = url.count("&")

    # -----------------------------------------------------
    # Other special characters
    #
    # Count non-alphanumeric characters
    # except =, ?, and &
    #
    # Those three have their own features.
    # -----------------------------------------------------

    no_of_other_special_chars = sum(

        1

        for char in url

        if not char.isalnum()
        and char not in ["=", "?", "&"]

    )

    # =====================================================
    # RETURN FEATURES
    #
    # EXACT names expected by Random Forest
    # =====================================================

    features = {

        "URLLength": url_length,

        "DomainLength": domain_length,

        "IsDomainIP": is_domain_ip,

        "TLDLength": tld_length,

        "NoOfSubDomain": no_of_subdomain,

        "HasObfuscation": has_obfuscation,

        "NoOfObfuscatedChar": no_of_obfuscated_char,

        "ObfuscationRatio": obfuscation_ratio,

        "NoOfLettersInURL": no_of_letters,

        "NoOfDegitsInURL": no_of_digits,

        "NoOfEqualsInURL": no_of_equals,

        "NoOfQMarkInURL": no_of_qmark,

        "NoOfAmpersandInURL": no_of_ampersand,

        "NoOfOtherSpecialCharsInURL": no_of_other_special_chars

    }

    return features