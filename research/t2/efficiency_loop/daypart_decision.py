"""Train daypart plans, then run an independent synthetic policy comparison."""
import argparse
import json
from dataclasses import asdict
from pathlib import Path

from daypart_scenarios import BASELINE, COUNTS, plans, worlds
from optimize import oracle_offsets, search
from receiving_diagnostics import assess

TRAIN_SEED = 17
EVALUATION_SEED = 23


def fit(catalog, fit_worlds):
    fit_worlds = tuple(fit_worlds)
    scenarios = tuple(w.scenario for w in fit_worlds)
    offsets, _ = oracle_offsets(catalog, scenarios, fast=True)
    strategies = {
        "fixed_baseline": dict.fromkeys(COUNTS, BASELINE),
        "pooled_minimax_cost": dict.fromkeys(COUNTS, search(catalog, scenarios, fast=True).plan),
        "pooled_minimax_regret": dict.fromkeys(
            COUNTS, search(catalog, scenarios, offsets, fast=True).plan
        ),
        "band_minimax_regret": {},
    }
    for band in COUNTS:
        pairs = [(w.scenario, off) for w, off in zip(fit_worlds, offsets) if w.band == band]
        band_worlds, band_offsets = zip(*pairs)
        strategies["band_minimax_regret"][band] = search(
            catalog, band_worlds, band_offsets, fast=True
        ).plan
    return strategies


def experiment():
    catalog = plans()
    strategies = fit(catalog, worlds(TRAIN_SEED))
    evaluation = tuple(worlds(EVALUATION_SEED))
    offsets, _ = oracle_offsets(catalog, (w.scenario for w in evaluation), fast=True)
    rows = {}
    for w, best in zip(evaluation, offsets):
        outputs = {}
        for policy, band_plans in strategies.items():
            outcome = assess(band_plans[w.band], w.scenario)
            outputs[policy] = {**outcome, "regret": outcome["cost"] - best}
        rows[w.scenario.name] = {"catalog_oracle_cost": best, "policies": outputs}
    summary = {}
    for policy in strategies:
        policy_rows = [r["policies"][policy] for r in rows.values()]
        summary[policy] = {f"worst_{k}": max(r[k] for r in policy_rows)
                           for k in policy_rows[0]}
        summary[policy]["sum_cost"] = sum(r["cost"] for r in policy_rows)
    return {
        "evidence": "synthetic paired worlds",
        "train_seed": TRAIN_SEED,
        "evaluation_seed": EVALUATION_SEED,
        "catalog_size": len(catalog),
        "plans": {k: {band: asdict(plan) for band, plan in v.items()}
                  for k, v in strategies.items()},
        "summary": summary,
        "worlds": rows,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(experiment(), indent=2) + "\n", encoding="utf-8")
