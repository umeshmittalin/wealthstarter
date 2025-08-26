from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass
class Allocation:
    split: Dict[str, float]  # percentages that sum to 1.0
    notes: str

BASE_ALLOCS = {
    "Conservative": {"Equity (India)":0.25, "Equity (International)":0.05, "Debt":0.60, "Gold":0.10},
    "Balanced":     {"Equity (India)":0.45, "Equity (International)":0.10, "Debt":0.35, "Gold":0.10},
    "Aggressive":   {"Equity (India)":0.60, "Equity (International)":0.15, "Debt":0.15, "Gold":0.10},
}

def glide_adjust(base: Dict[str,float], age:int, years_to_goal:int|None=None) -> Dict[str,float]:
    # Simple glide: target equity cap = max(0.3, 1 - age/100)
    eq_cap = max(0.30, 1 - age/100)
    eq_total = base["Equity (India)"] + base["Equity (International)"]
    if eq_total > eq_cap:
        # scale down equities proportionally, shift to Debt
        scale = eq_cap / eq_total
        delta = eq_total - eq_total*scale
        out = base.copy()
        out["Equity (India)"] *= scale
        out["Equity (International)"] *= scale
        out["Debt"] += delta
        base = out
    # Near-goal de-risking
    if years_to_goal is not None and years_to_goal <= 3:
        shift = 0.10  # shift 10% from equities to Debt/Gold
        out = base.copy()
        move_ei = min(shift/2, out["Equity (India)"])
        move_eu = min(shift/2, out["Equity (International)"])
        out["Equity (India)"] -= move_ei
        out["Equity (International)"] -= move_eu
        out["Debt"] += shift*0.7
        out["Gold"] += shift*0.3
        base = out
    # normalize
    s = sum(base.values())
    return {k: v/s for k,v in base.items()}

def recommend(risk_label:str, age:int, years_to_goal:int|None=None) -> Allocation:
    base = BASE_ALLOCS.get(risk_label, BASE_ALLOCS["Balanced"])
    split = glide_adjust(base, age, years_to_goal)
    notes = f"Base {risk_label} allocation with age glide (age={age})."
    if years_to_goal is not None:
        notes += f" De-risked for goal in {years_to_goal} years."
    return Allocation(split=split, notes=notes)

def rebalance_plan(current: Dict[str,float], target: Dict[str,float], corpus: float) -> Dict[str, float]:
    plan = {}
    for k in target.keys():
        curr_amt = corpus * current.get(k,0)
        tgt_amt  = corpus * target[k]
        plan[k] = round(tgt_amt - curr_amt, 2)  # positive = buy, negative = sell
    return plan

def weights_from_amounts(amounts: Dict[str, float]) -> Dict[str, float]:
    total = sum(amounts.values()) or 1.0
    return {k: v/total for k,v in amounts.items()}
