from dataclasses import dataclass

@dataclass
class RiskResult:
    score: int
    label: str

QUESTIONS = [
    ("How would you react to a 15% fall in your portfolio?", {"Sell":0,"Hold":2,"Buy more":4}),
    ("Investment horizon for majority of funds?", {"<3 years":0,"3-7 years":2,">7 years":4}),
    ("Income stability?", {"Unstable":0,"Moderately stable":2,"Very stable":4}),
    ("Experience with market products?", {"None":0,"Some":2,"Extensive":4}),
    ("Primary goal?", {"Capital preservation":0,"Wealth growth":2,"Aggressive growth":4}),
    ("Volatility comfort?", {"Low":0,"Medium":2,"High":4}),
]

def score_answers(answers: list[str]) -> RiskResult:
    # answers are option labels in the order of QUESTIONS
    score = 0
    for (q, opts), ans in zip(QUESTIONS, answers):
        score += list(opts.values())[list(opts.keys()).index(ans)]
    if score <= 6:
        label = "Conservative"
    elif score <= 12:
        label = "Balanced"
    else:
        label = "Aggressive"
    return RiskResult(score, label)
