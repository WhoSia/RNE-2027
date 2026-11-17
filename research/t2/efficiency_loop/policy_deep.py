"""Matched attribution and a stronger frozen fixed-time comparison."""
import argparse
from dataclasses import asdict, replace
from itertools import product
import json
from pathlib import Path

from actuated import Observation
from efficiency import evaluate
from field_replay import EVAL, TRAIN
from field_scenarios import case
from optimize import catalog, search
from policy_screen import DETECTORS, FIXED, SYNTHETIC, synthetic
from signal_model import Plan

TRAIN_SEEDS = (801, 812, 823)
EVAL_SEEDS = (907, 918, 929, 940)


def compare(scenario, fixed, seed):
    values = {"fixed": evaluate(fixed,scenario,"fixed")}
    for policy, name in product(("queue","receiving","confirmed"), DETECTORS):
        delay, miss = DETECTORS[name]
        values[f"{policy}/{name}"] = evaluate(fixed,scenario,policy,Observation(delay,miss,seed))
    return values


def deep():
    def summary(row):
        return {name: {"cost":v["cost"],"done":sum(v["completed"]),
                       "pedestrian_area":v["area_by_movement"][6],
                       "blocked":sum(x[2] for x in v["opportunity"].values()),
                       "idle":sum(x[1] for x in v["opportunity"].values()),
                       "max_ped_wait":v["maximum_observed_wait"][6]}
                for name,v in row.items()}

    # Pick an observed failure from the breadth pass and change one dimension at a time.
    original = synthetic("east_platoon","tight",227)
    ablations = []
    for capacity, receiving_green in product((original.link,(10,4,10,4,10,10)), (12,36)):
        s = replace(original, link=capacity, receive_green=receiving_green)
        ablations.append({"capacity":capacity,"receiving_green":receiving_green,
                          "results":summary(compare(s,FIXED,227))})
    return ablations


def external(root):
    trained = {}
    rows = []
    for storage in ("open","tight"):
        training = tuple(synthetic(k,storage,seed) for k,seed in product(SYNTHETIC,TRAIN_SEEDS))
        plans = catalog()
        fit = search(plans,training,first=FIXED)
        trained[storage] = asdict(fit)
        for demand,seed in product(SYNTHETIC,EVAL_SEEDS):
            s = synthetic(demand,storage,seed)
            rows.append({"source":"synthetic","storage":storage,"demand":demand,"seed":seed,
                         "policies":compare(s,fit.plan,seed)})
    initial = Plan((24,12,29,8),False,84)
    field_fit = search(catalog(85),tuple(case(root,b,seed)[0]
                       for b,seed in zip(TRAIN,(31,37,41,43))),first=initial)
    trained["DLR_hybrid"] = asdict(field_fit)
    for block,seed in product(EVAL,(31,37,41,43)):
        s, provenance = case(root,block,seed)
        rows.append({"source":"DLR_hybrid","storage":"default","demand":block,
                     **provenance,"policies":compare(s,field_fit.plan,seed)})
    return trained, rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dlr_root",type=Path)
    parser.add_argument("output",type=Path)
    args = parser.parse_args()
    fits, evaluation = external(args.dlr_root)
    args.output.write_text(json.dumps({"matched_ablation":deep(),"fixed_training":fits,
                                      "evaluation":evaluation},separators=(",",":"))+"\n")
