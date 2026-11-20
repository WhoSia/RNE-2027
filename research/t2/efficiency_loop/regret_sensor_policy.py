"""Exact 2-world minimax forecast policy with conditional error at most epsilon.

Regret is relative to the better of two signal phase orders.  The forecast
has two labels: the first world favors left-first (negative delta), and the
second favors through-first (positive delta). Independent of error base rates,
Nature may choose any label-error probability up to epsilon in *each* world.
This model concerns only two synthetic worlds, not a traffic experiment.
"""
from fractions import Fraction
from dataclasses import dataclass
import json
import argparse
from pathlib import Path


@dataclass(frozen=True)
class OptimalPolicy:
    left_on_early: Fraction
    left_on_late: Fraction
    regret: Fraction
    fixed_randomized_regret: Fraction
    fixed_deterministic_regret: int
    forecast_follow_regret: Fraction


def frac_string(x):
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def worst_regret(left_cost, through_cost, error, alpha, beta):
    """Adversarial conditional-error bounds for a binary randomized controller."""
    a, b, e = Fraction(left_cost), Fraction(through_cost), Fraction(error)
    alpha, beta = Fraction(alpha), Fraction(beta)
    if min(a, b) <= 0 or not (0 <= e <= 1) or not (0 <= alpha <= 1 and 0 <= beta <= 1):
        raise ValueError("invalid losses, error bound or policy probabilities")
    if alpha >= beta:
        early = a * (1 - alpha + e * (alpha - beta))
        late = b * (beta + e * (alpha - beta))
    else:
        # The adversary is permitted to make no label errors.
        early = a * (1 - alpha)
        late = b * beta
    return max(early, late)


def optimize(early_delta, late_delta, error):
    """Exact minimax over all randomized policies for the 2-world error set."""
    a, b, e = Fraction(-early_delta), Fraction(late_delta), Fraction(error)
    if min(a, b) <= 0 or not 0 <= e <= 1:
        raise ValueError("strict sign reversal and 0 <= error <= 1 required")
    baseline = a*b/(a+b)  # randomize without any forecast
    if e >= Fraction(1, 2):
        beta = alpha = a/(a+b)
    else:
        A = a*(1-e)+b*e
        B = b*(1-e)+a*e
        d = min(Fraction(1), a/A, b/B)
        beta = (a-A*d)/(a+b)
        alpha = beta+d
    regret = worst_regret(a, b, e, alpha, beta)
    assert 0 <= beta <= alpha <= 1
    assert regret <= baseline
    return OptimalPolicy(alpha, beta, regret, baseline, int(min(a,b)), max(a,b)*e)


def row(early, late, numerator, denominator):
    e = Fraction(numerator, denominator)
    p = optimize(early, late, e)
    return {
        "conditional_error_bound": frac_string(e),
        "p_left_if_early_label": frac_string(p.left_on_early),
        "p_left_if_late_label": frac_string(p.left_on_late),
        "optimal_worst_regret": frac_string(p.regret),
        "fixed_randomized_without_forecast": frac_string(p.fixed_randomized_regret),
        "fixed_deterministic_without_forecast": p.fixed_deterministic_regret,
        "always_follow_label_bound": frac_string(p.forecast_follow_regret),
    }


def report():
    return {
        "scope": "Two synthetic worlds, conditional label error <= epsilon, randomized phase-order policy; no physical intervention",
        "new_seed_337_deltas": [-113, 31],
        "legacy_deltas": [-3, 35],
        "error_values": ["0", "1/10", "1/4", "3/10", "49/100", "1/2"],
        "new_seed_337": [row(-113, 31, n, d) for n,d in ((0,1),(1,10),(1,4),(3,10),(49,100),(1,2))],
        "legacy": [row(-3,35,n,d) for n,d in ((0,1),(1,10),(1,4),(3,10),(49,100),(1,2))],
        "precommitment_required": True,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(report(), ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
