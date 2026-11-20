"""Exact worst-case expected regret under conditional binary forecast error."""
import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from daypart_scenarios import worlds
from storage_information import BIN_STARTS, DECISION, SEEDS, decision, matched_storage_cases

MAX_ERROR = Fraction(1, 2)
ERROR_GRID = tuple(Fraction(i, 20) for i in range(11))
RULES = tuple(product((0, 1), repeat=2))  # 0=through first, 1=left first


def envelope(rows, rule):
    lines = []
    for truth, delta in rows:
        regret = (max(0, -delta), max(0, delta))
        correct, wrong = regret[rule[truth]], regret[rule[1-truth]]
        lines.append((correct, max(0, wrong - correct)))
    return lines


def evaluate(rows):
    baseline = decision([delta for _, delta in rows])["regret"]
    policies = {rule: envelope(rows, rule) for rule in RULES}
    # Strict improvement requires every affine world-loss line below baseline.
    ceilings = []
    for lines in policies.values():
        if all(a < baseline for a, _ in lines):
            ceilings.append(min([MAX_ERROR] + [Fraction(baseline-a, b) for a, b in lines if b]))
    grid = []
    for error in ERROR_GRID:
        losses = {rule: max(a + b*error for a, b in lines) for rule, lines in policies.items()}
        best = min(losses.values())
        grid.append({"error": str(error), "regret": str(best),
                     "rules": [rule for rule, loss in losses.items() if loss == best]})
    return {"baseline_regret": baseline,
            "strict_improvement_error_ceiling": str(max(ceilings)) if ceilings else None,
            "grid": grid}


def report():
    closed = sum(start + 2 <= DECISION for start in BIN_STARTS)
    ambiguous = []
    group_counts = defaultdict(int)
    for seed in SEEDS:
        for world in worlds(seed):
            if world.receiving != "constrained":
                continue
            for storage, _, _, rows in matched_storage_cases(world.scenario):
                groups = defaultdict(list)
                for bits, _, pocket, link, area, remaining in rows:
                    groups[bits[:closed], pocket, link].append((bits, area, remaining))
                for terminal in (0, 60, 120):
                    group_counts[terminal] += len(groups)
                    for info, outcomes in groups.items():
                        deltas = [(bits, area + terminal*remaining) for bits, area, remaining in outcomes]
                        values = [delta for _, delta in deltas]
                        if min(values) >= 0 or max(values) <= 0:
                            continue
                        ambiguous.append({
                            "context": [seed, world.band, world.shape, storage],
                            "terminal": terminal, "info": info, "worlds": len(values),
                            "bounds": [min(values), max(values)],
                            "forecasts": {str(BIN_STARTS[i]): evaluate([(bits[i], d) for bits, d in deltas])
                                          for i in range(closed, len(BIN_STARTS))},
                        })
    return {"decision_tick": DECISION, "counts_by_terminal": dict(group_counts),
            "ambiguous_groups": ambiguous}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(report(), sort_keys=True, separators=(",", ":"))+"\n",
                           encoding="utf-8")
