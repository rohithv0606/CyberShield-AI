from urllib.parse import urlparse
import re
import ipaddress


def extract_url_features(url: str) -> dict:

    # ==========================================
    # BASIC URL INFORMATION
    # ==========================================

    parsed = urlparse(url)

    domain = parsed.netloc

    # Remove username/password if present
    if "@" in domain:
        domain = domain.split("@")[-1]

    # Remove port
    domain = domain.split(":")[0]

    # Remove www.
    if domain.startswith("www."):
        domain = domain[4:]


    # ==========================================
    # 1. URL LENGTH
    # ==========================================

    url_length = len(url)


    # ==========================================
    # 2. DOMAIN LENGTH
    # ==========================================

    domain_length = len(domain)


    # ==========================================
    # 3. IS DOMAIN IP
    # ==========================================

    try:
        ipaddress.ip_address(domain)
        is_domain_ip = 1
    except ValueError:
        is_domain_ip = 0


    # ==========================================
    # 4. TLD LENGTH
    # ==========================================

    if "." in domain:
        tld = domain.split(".")[-1]
        tld_length = len(tld)
    else:
        tld_length = 0


    # ==========================================
    # 5. NUMBER OF SUBDOMAINS
    # ==========================================

    domain_parts = domain.split(".")

    if len(domain_parts) >= 2:
        no_of_subdomain = max(len(domain_parts) - 2, 0)
    else:
        no_of_subdomain = 0


    # ==========================================
    # 6. OBFUSCATION DETECTION
    # ==========================================

    has_obfuscation = int(
        bool(re.search(r"%[0-9a-fA-F]{2}", url))
        or "\\" in url
    )


    # ==========================================
    # 7. NUMBER OF OBFUSCATED CHARACTERS
    # ==========================================

    no_of_obfuscated_char = len(
        re.findall(r"%[0-9a-fA-F]{2}", url)
    )


    # ==========================================
    # 8. OBFUSCATION RATIO
    # ==========================================

    if url_length > 0:
        obfuscation_ratio = (
            no_of_obfuscated_char / url_length
        )
    else:
        obfuscation_ratio = 0


    # ==========================================
    # 9. NUMBER OF LETTERS
    # ==========================================

    no_of_letters = sum(
        char.isalpha() for char in url
    )


    # ==========================================
    # 10. NUMBER OF DIGITS
    # ==========================================

    no_of_digits = sum(
        char.isdigit() for char in url
    )


    # ==========================================
    # 11. NUMBER OF =
    # ==========================================

    no_of_equals = url.count("=")


    # ==========================================
    # 12. NUMBER OF ?
    # ==========================================

    no_of_qmark = url.count("?")


    # ==========================================
    # 13. NUMBER OF &
    # ==========================================

    no_of_ampersand = url.count("&")


    # ==========================================
    # 14. OTHER SPECIAL CHARACTERS
    # ==========================================

    special_chars = re.findall(
        r"[^a-zA-Z0-9]",
        url
    )

    no_of_other_special_chars = len(special_chars)


    # ==========================================
    # RETURN FEATURES
    # ==========================================

    return {
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