DISCLAIMER = (
    "This tool is for educational purposes only and does not provide investment advice. "
    "Please consult a SEBI-registered Investment Adviser for personalised advice. "
    "All outputs are hypothetical and may differ from actual market outcomes."
)

GUARDRAILS = [
    "Do not recommend specific securities or funds by name when user is unverified.",
    "Always capture risk profile and investment horizon before suggesting allocation.",
    "Flag if user is within 12 months of a goal: reduce equity tilt.",
    "Never promise returns; show ranges based on historical assumptions."
]
