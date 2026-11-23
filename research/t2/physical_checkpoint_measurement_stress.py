"""PHYS-05b: fixed-policy stress under synthetic detector count noise/dropout.

Input: PHYS-04 144-pair training JSON and PHYS-05 432-pair holdout JSON.
Outcomes, physical trajectories and the trained k=5 neighbor rule remain
unchanged. Only the observation at the decision boundary is corrupted.
This does NOT calibrate real-world sensors or prove safety.
"""
import argparse
import copy
import json
import random
import statistics
from pathlib import Path

from physical_checkpoint_observation_ablation import predict

TRIALS = 8
SCENARIOS = ((0, 0.), (1, 0.), (1, .1), (2, .3))
COUNT_FIELDS = ("outside_A", "outside_B", "approach_A",
                "approach_B", "pocket_vehicles", "receiver_vehicles")
POSITION_FIELDS = ("approach_A_positions", "approach_B_positions",
                   "pocket_positions", "receiver_occupied_cells")


def corrupt(row, amplitude, dropout, trial):
    r = copy.deepcopy(row)
    # Zero-jitter, zero-dropout must preserve the exact observation, including
    # tuple/list container types. Otherwise the control is not an identity.
    if amplitude == 0 and dropout == 0:
        return r
    observed = r["decision_observation"]
    seed = (r["seed"] * 1000003 + r["capacity"] * 1009 +
            int(r["pocket_m"]) * 13 + int(r["b_share"] * 100) * 17 +
            trial * 7919 + amplitude * 104729 + int(dropout * 100) * 1217)
    rng = random.Random(seed)
    limits = {"approach_A": 20, "approach_B": 20,
              "pocket_vehicles": int(r["pocket_m"] / 7),
              "receiver_vehicles": r["capacity"]}
    for key in COUNT_FIELDS:
        value = observed[key] + rng.randint(-amplitude, amplitude) if amplitude else observed[key]
        observed[key] = max(0, min(value, limits.get(key, value)))
    for key in POSITION_FIELDS:
        observed[key] = [x for x in observed[key] if rng.random() >= dropout]
    return r


def experiment(train, holdout):
    if len(train) != 144 or {r["seed"] for r in train} != set(range(8)):
        raise ValueError("training data must contain PHYS-04 seeds 0..7")
    if len(holdout) != 432 or {r["seed"] for r in holdout} != set(range(8, 32)):
        raise ValueError("holdout must contain PHYS-05 seeds 8..31")
    results = {}
    for amplitude, dropout in SCENARIOS:
        name = f"count_jitter{amplitude}_position_dropout{round(dropout*100)}pct"
        records = []
        for trial in range(1 if amplitude == 0 and dropout == 0 else TRIALS):
            savings = {"counts": 0, "positions": 0}
            changes = {"counts": 0, "positions": 0}
            by_seed = {policy: {seed: 0 for seed in range(8, 32)}
                       for policy in savings}
            for row in holdout:
                noisy = corrupt(row, amplitude, dropout, trial)
                for policy in savings:
                    selected = predict(train, noisy, policy, k=5) < 0
                    if selected != row[policy + "_treat"]:
                        changes[policy] += 1
                    saved = -row["delta_p60"] if selected else 0
                    savings[policy] += saved
                    by_seed[policy][row["seed"]] += saved
            records.append({"trial": trial, "total_saved": savings,
                            "decisions_changed_from_clean": changes,
                            "by_seed": by_seed})
        results[name] = {
            "count_error_max_vehicles": amplitude,
            "position_dropout_probability": dropout,
            "trials": len(records),
            "mean_total_savings": {
                policy: statistics.mean(r["total_saved"][policy] for r in records)
                for policy in ("counts", "positions")},
            "min_total_savings": {
                policy: min(r["total_saved"][policy] for r in records)
                for policy in ("counts", "positions")},
            "max_total_savings": {
                policy: max(r["total_saved"][policy] for r in records)
                for policy in ("counts", "positions")},
            "mean_decision_flips": {
                policy: statistics.mean(r["decisions_changed_from_clean"][policy]
                                        for r in records)
                for policy in ("counts", "positions")},
            "individual_trials": records,
        }
    return {
        "status": "SYNTHETIC_DETECTOR_STRESS_NOT_CALIBRATED",
        "model": "frozen k=5 predictor trained on seeds 0..7",
        "heldout_seeds": [8, 31],
        "cases_per_trial": len(holdout),
        "note": "uniform independent integer count jitter and random occupancy omission; outcomes unchanged",
        "scenarios": results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("training_json", type=Path)
    parser.add_argument("holdout_json", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args()
    train = json.loads(args.training_json.read_text(encoding="utf-8"))["pairs"]
    holdout = json.loads(args.holdout_json.read_text(encoding="utf-8"))["cases"]
    args.output_json.write_text(
        json.dumps(experiment(train, holdout), sort_keys=True,
                   ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
