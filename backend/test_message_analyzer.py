from services.message_analyzer import analyze_message


message = """
Hey, are we still meeting at the library at 5 PM?
I will bring the project documents.
"""


result = analyze_message(message)


print("\n========== MESSAGE ANALYSIS ==========\n")

print("Risk Score:", result["risk_score"])

print("Classification:", result["classification"])


print("\nReasons:")

for reason in result["reasons"]:
    print("-", reason)


print("\nSignals:")

for signal, values in result["signals"].items():
    print(f"{signal}: {values}")