"""Stress the seeded daypart finding without changing its chosen policies."""
import argparse
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

from daypart_decision import EVALUATION_SEED, TRAIN_SEED, fit
from daypart_scenarios import plans, worlds
from optimize import oracle_offsets
from signal_model import run

STRESS_SEEDS = (101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157)


def stress():
    assert not {TRAIN_SEED, EVALUATION_SEED}.intersection(STRESS_SEEDS)
    catalog = plans()
    policies = fit(catalog, worlds(TRAIN_SEED))
    results = {}
    for seed in STRESS_SEEDS:
        cases = tuple(worlds(seed))
        best, _ = oracle_offsets(catalog, (w.scenario for w in cases), fast=True)
        trials = {}
        for label, band_plans in policies.items():
            costs = [run(band_plans[w.band], w.scenario, fast=True).cost for w in cases]
            trials[label] = {"worst_cost": max(costs), "sum_cost": sum(costs),
                             "worst_regret": max(c - b for c, b in zip(costs, best))}
        results[seed] = trials
    comparison = {}
    for left, right in combinations(policies, 2):
        tallies = {m: Counter() for m in next(iter(results.values()))[left]}
        for trial in results.values():
            for metric, counts in tallies.items():
                a, b = trial[left][metric], trial[right][metric]
                counts[left if a < b else right if b < a else "tie"] += 1
        comparison[f"{left} vs {right}"] = tallies
    return {"fitted_seed": TRAIN_SEED, "original_evaluation_seed": EVALUATION_SEED,
            "seeds": STRESS_SEEDS, "worlds_per_seed": len(cases),
            "seed_results": results, "pairwise_counts": comparison}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(stress(), indent=2) + "\n", encoding="utf-8")
