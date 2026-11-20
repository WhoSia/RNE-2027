"""Exact worst-case expected regret under conditional binary forecast error."""
import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path

from daypart_scenarios import worlds
from storage_information import BIN_STARTS, DECISION, SEEDS, decision, matched_storage_cases

MAX_ERROR = Fraction(1, 2)
ERROR_GRID = tuple(Fraction(i, 20) for i in range(11))


def envelope(rows, rule):
    lines = []
    for truth, delta in rows:
        regret = (max(0, -delta), max(0, delta))
        correct = regret[rule[truth]]
        wrong = max(regret[order] for message, order in enumerate(rule) if message != truth)
        lines.append((correct, max(0, wrong - correct)))
    return lines


def improvement_limit(policies, baseline):
    # Strict improvement requires every affine world-loss line below baseline.
    limits = []
    for lines in policies.values():
        if not all(a < baseline for a, _ in lines):
            continue
        limit = min([MAX_ERROR] + [(baseline-a)/b for a, b in lines if b])
        limits.append((limit, all(a+b*limit < baseline for a, b in lines)))
    return max(limits, default=(None, False))


def evaluate(rows, messages=2):
    deltas = [delta for _, delta in rows]
    baseline = decision(deltas)["regret"]
    a, b = max(0, -min(deltas)), max(0, max(deltas))
    mixed = Fraction(a*b, a+b) if a+b else Fraction(0)
    policies = {rule: envelope(rows, rule) for rule in product((0, 1), repeat=messages)}
    limit, inclusive = improvement_limit(policies, Fraction(baseline))
    mixed_limit, mixed_inclusive = improvement_limit(policies, mixed)
    grid = []
    for error in ERROR_GRID:
        losses = {rule: max(a + b*error for a, b in lines) for rule, lines in policies.items()}
        best = min(losses.values())
        grid.append({"error": str(error), "regret": str(best),
                     "rules": [rule for rule, loss in losses.items() if loss == best]})
    return {"baseline_regret": baseline,
            "strict_improvement_error_ceiling": str(limit) if limit is not None else None,
            "ceiling_inclusive": inclusive,
            "mixed_baseline_regret": str(mixed),
            "error_ceiling_vs_mixed_baseline": str(mixed_limit) if mixed_limit is not None else None,
            "mixed_ceiling_inclusive": mixed_inclusive,
            "grid": grid}


def exact_subsets(deltas, closed):
    """Regret when a subset of future orders is known without error."""
    scores = {}
    for size in range(1, len(BIN_STARTS)-closed+1):
        for indices in combinations(range(closed, len(BIN_STARTS)), size):
            groups = defaultdict(list)
            for bits, delta in deltas:
                groups[tuple(bits[i] for i in indices)].append(delta)
            label = "/".join(str(BIN_STARTS[i]) for i in indices)
            scores[label] = max(decision(values)["regret"] for values in groups.values())
    return scores


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
                            "exact_subset_regret": exact_subsets(deltas, closed),
                            "joint_error": {
                                "/".join(str(t) for t in BIN_STARTS[-size:]):
                                    evaluate([(int("".join(map(str, bits[-size:])), 2), d)
                                              for bits, d in deltas], messages=2**size)
                                for size in (2, 3)
                            } if terminal == 60 else None,
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
