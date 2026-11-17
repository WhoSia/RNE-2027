"""Evaluate bounded count errors together with flagged erasure."""

import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from d51_phase_order import Params
from prospective_sensing import PROFILE
from uncertain_pocket_sensing import ACTIONS, bounded_error, by_count, reading_support


def joint_policy(groups, capacity, mode, upper):
    """Return optimal regret and a deterministic reader with one fallback."""
    if not 0 <= upper <= 1:
        raise ValueError("Erasure probability must be between zero and one")
    preimages = {}
    for count, bounds in groups.items():
        for reading in reading_support(count, capacity, mode):
            preimages.setdefault(reading, []).append(bounds)

    candidates = []
    for fallback in ACTIONS:
        readable = {}
        worst = 0
        for reading, possible in sorted(preimages.items()):
            positive = max(0, max(bounds.high for bounds in possible))
            negative = max(0, -min(bounds.low for bounds in possible))
            scores = []
            for choice in ACTIONS:
                weights = (
                    int(choice == "lead"),
                    (1 - upper) * (choice == "lead") + upper * (fallback == "lead"),
                )
                score = max(max(weight * positive, (1 - weight) * negative) for weight in weights)
                scores.append((score, choice))
            score, readable[reading] = min(scores)
            worst = max(worst, score)
        candidates.append((worst, fallback, readable))
    regret, fallback, readable = min(candidates, key=lambda case: case[:2])
    return regret, {"fallback": fallback, "readable": readable}


def grid():
    modes = ("exact", "fullness", "miss_one", "off_by_one")
    limits = (Fraction(0), Fraction(1, 10), Fraction(1, 4), Fraction(1, 2), Fraction(1))
    rows = []
    for capacity, decision, cap, visible in product(
        (1, 2, 3, 4), (6, 8), (2, 3), product(PROFILE, repeat=2)
    ):
        base, groups = by_count(visible, decision, cap, Params(left_capacity=capacity, horizon_s=180))
        reading_results = {}
        for mode in modes:
            readable_regret = bounded_error(groups, capacity, mode)["worst_regret"]
            results = {}
            for upper in limits:
                value, policy = joint_policy(groups, capacity, mode, upper)
                assert max(readable_regret, upper * base.regret) <= value
                assert value <= (1 - upper) * readable_regret + upper * base.regret
                assert (value < base.regret) == (upper < 1 and readable_regret < base.regret)
                results[str(upper)] = {"regret": str(value), "policy": policy}
            reading_results[mode] = results
        rows.append({
            "capacity": capacity,
            "decision": decision,
            "future_cap": cap,
            "visible_counts": visible,
            "unmeasured_regret": base.regret,
            "modes": reading_results,
        })
    summary = {}
    for capacities in ((1, 2), (3, 4)):
        selected = [row for row in rows if row["capacity"] in capacities]
        table = {}
        for mode in modes:
            table[mode] = {}
            for upper in map(str, limits):
                reductions = [
                    row["unmeasured_regret"] - Fraction(row["modes"][mode][upper]["regret"])
                    for row in selected
                ]
                table[mode][upper] = {
                    "improved_contexts": sum(reduction > 0 for reduction in reductions),
                    "maximum_reduction": str(max(reductions)),
                }
        summary["-".join(map(str, capacities))] = table
    return {"scope": "Synthetic D51 grid. Erasure bounds are assumed.", "summary": summary, "rows": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(grid(), separators=(",", ":")) + "\n", encoding="utf-8")
