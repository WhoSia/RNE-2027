"""PHYS-05: leave-one-demand-seed-out observation ablation (synthetic only).

Input: JSON from physical_checkpoint_capacity_screen.py.
Fixed decision rule: five nearest cases from OTHER seeds by scaled
squared Euclidean distance; choose intervention only if mean train delta < 0.
The outcome is never used for the held-out seed's decision.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

LEVELS = ("geometry", "counts", "positions")


def features(row, level):
    o = row["decision_observation"]
    v = [row["capacity"] / 8., row["pocket_m"] / 70., row["b_share"]]
    if level in ("counts", "positions"):
        v += [o["outside_A"] / 120., o["outside_B"] / 120.,
              o["approach_A"] / 20., o["approach_B"] / 20.,
              o["pocket_vehicles"] / 10., o["receiver_vehicles"] / 8.]
    if level == "positions":
        for attr, low, high in (("approach_A_positions", -20, -1),
                                ("approach_B_positions", -20, -1),
                                ("pocket_positions", -10, -1),
                                ("receiver_occupied_cells", 0, 7)):
            occupied = set(o[attr])
            length = high - low + 1
            v.extend([.5 / math.sqrt(length) if x in occupied else 0.
                      for x in range(low, high + 1)])
    return tuple(v)


def predict(train, row, level, k=5):
    point = features(row, level)
    distances = []
    for other in train:
        f = features(other, level)
        distance = sum((a-b)**2 for a, b in zip(point, f))
        distances.append((distance, other["seed"], other["capacity"],
                          other["pocket_m"], other["b_share"], other["delta_p60"]))
    nearest = sorted(distances)[:k]
    return sum(z[-1] for z in nearest) / len(nearest)


def experiment(rows):
    assert len(rows) == 144
    assert len({(r["capacity"], r["seed"], r["pocket_m"], r["b_share"])
                for r in rows}) == 144
    predictions = []
    for testseed in range(8):
        train = [r for r in rows if r["seed"] != testseed]
        test = [r for r in rows if r["seed"] == testseed]
        assert len(train) == 126 and len(test) == 18
        for r in test:
            delta = r["delta_p60"]
            x = {"seed": testseed, "capacity": r["capacity"],
                 "pocket_m": r["pocket_m"], "b_share": r["b_share"],
                 "delta_p60": delta,
                 "oracle_best_cost_reduction": max(-delta, 0),
                 "baseline_cost_reduction": 0,
                 "always_treat_cost_reduction": -delta}
            for level in LEVELS:
                estimate = predict(train, r, level)
                x[level + "_prediction_delta"] = estimate
                x[level + "_treat"] = estimate < 0
                x[level + "_cost_reduction"] = -delta if estimate < 0 else 0
            predictions.append(x)
    summary = {}
    for name in ("baseline", "always_treat") + LEVELS:
        values = [r[name + "_cost_reduction"] for r in predictions]
        summary[name] = {
            "total_saved_vs_always_baseline": sum(values),
            "mean_saved_per_pair": sum(values) / len(values),
            "count_treatment_selected": sum(r.get(name + "_treat",
                                                 name == "always_treat")
                                            for r in predictions),
            "total_regret_vs_hindsight_oracle":
                sum(r["oracle_best_cost_reduction"] - saved
                    for r, saved in zip(predictions, values)),
            "folds": [{"held_out_seed": seed,
                       "total_saved": sum(r[name + "_cost_reduction"]
                                          for r in predictions if r["seed"] == seed)}
                      for seed in range(8)]}
    oracle = sum(r["oracle_best_cost_reduction"] for r in predictions)
    summary["hindsight_oracle"] = {
        "total_saved_vs_always_baseline": oracle,
        "mean_saved_per_pair": oracle / len(predictions),
        "total_regret_vs_hindsight_oracle": 0}
    return {"experiment": "PHYS-05-cross-seed-observation-ablation",
            "limitations": "synthetic, no field detector noise/calibration, correlated geometry repetitions",
            "cross_validation": "8 leave-one-seed-out folds; 18 test and 126 train cases per fold",
            "model": "five nearest neighbors, squared scaled distance, fixed unweighted delta mean",
            "feature_levels": LEVELS, "summary": summary,
            "out_of_fold_predictions": predictions}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    raw = json.loads(args.input.read_text(encoding="utf-8"))
    out = experiment(raw["pairs"])
    blob = (json.dumps(out, sort_keys=True, ensure_ascii=False, indent=2) + "\n").encode()
    args.output.write_bytes(blob)
    print(json.dumps(out["summary"], indent=2))
    print("sha256", hashlib.sha256(blob).hexdigest())
