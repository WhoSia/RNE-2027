"""Run the controller on a hybrid stress test with DLR east-gate cohorts."""
import argparse
from collections import Counter
from dataclasses import asdict, replace
import csv
from hashlib import file_digest
from itertools import product
import json
from pathlib import Path
from random import Random

from field_replay import TRAIN, EVAL
from optimize import catalog, search
from signal_model import Plan, Scenario, run

START = 120
HORIZON = 420
OTHER_RATES = (.14, .06, .12, .10, .08)


def east_gate(root, block):
    hour, minute = int(block[:2]), int(block[2:])
    start = (hour - 12) * 3600 + minute * 60 + START
    path = root / "week1" / "wide" / block / "daylight_crossings.csv"
    with path.open("rb") as stream:
        checksum = file_digest(stream, "sha256").hexdigest()
    selected = []
    counts = Counter()
    with path.open(newline="") as stream:
        for row in csv.DictReader(stream):
            if not row["arrival"]:
                continue
            t = float(row["arrival"]) - start
            if not 0 <= t < HORIZON:
                continue
            kind = row["movement"] or "unclassified"
            counts[kind] += 1
            if kind in ("through","left"):
                selected.append((int(t), int(kind == "left")))
    return selected, dict(counts), checksum


def case(root, block, seed):
    east, counts, sha = east_gate(root, block)
    rng = Random(seed)
    other = [(t, m) for t,m in product(range(HORIZON), range(2,7))
             if rng.random() < OTHER_RATES[m-2]]
    arrivals = tuple(sorted(east + other, key=lambda a:a[0]))
    return Scenario(block, HORIZON, arrivals), {
        "east_classes": counts, "east_TL": len(east), "east_rows_sha256": sha,
        "generated_other_movements": len(other), "seed": seed,
    }


def main(root):
    plans = catalog(cycle=85)
    baseline = Plan((28,12,21,12), False, 0)
    # Same random streams for each day block isolate changes in the east cohort.
    training = [case(root,b,seed)[0] for b,seed in zip(TRAIN,(11,19,23,29))]
    solution = search(plans, training, first=baseline)
    rows = []
    for block in TRAIN + EVAL:
        seeds = (11,19,23,29) if block in EVAL else (dict(zip(TRAIN,(11,19,23,29)))[block],)
        for seed in seeds:
            s, detail = case(root,block,seed)
            normal = run(baseline,s)
            winner = run(solution.plan,s)
            if block in EVAL:
                oracle = search(plans,(s,),first=solution.plan,relax=True)
                detail["perfect_information_cost"] = oracle.value
            rows.append({"block":block,"role":"evaluation" if block in EVAL else "training",
                         **detail, "baseline":asdict(normal), "fixed_training_plan":asdict(winner)})
    return {"cycle": 85, "plans":len(plans), "best_training":asdict(solution), "blocks":rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(main(args.input),indent=2) + "\n")
