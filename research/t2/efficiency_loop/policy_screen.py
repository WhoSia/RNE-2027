"""Breadth pass with frozen policies, seed sets, and paired scenario conditions."""
import argparse
from dataclasses import replace
from itertools import product
import json
from pathlib import Path
from random import Random

from actuated import Observation
from efficiency import evaluate
from field_replay import EVAL
from field_scenarios import case
from signal_model import Plan, Scenario

FIXED = Plan((24,16,20,12),False,0)
DEFAULT = Plan((28,12,20,12),False,0)
FIELD = Plan((24,12,29,8),False,84)
SYNTHETIC = {
    "light": (.045,.018,.045,.018,.035,.035,.035),
    "balanced": (.16,.06,.15,.05,.14,.13,.10),
    "turn_surge": (.22,.16,.12,.07,.10,.09,.07),
    "cross_surge": (.08,.03,.10,.03,.20,.19,.13),
    "east_platoon": (.18,.06,.15,.05,.14,.13,.10),
}
STORAGE = {
    "open": ((10,4,10,4,10,10),36),
    "tight": ((3,2,3,2,4,4),12),
}
DETECTORS = {"exact": (0,0), "late": (6,0), "lossy": (0,.30), "late_lossy": (6,.30)}
SEEDS = (116, 227, 338, 449, 560, 671)


def synthetic(kind, storage, seed):
    rng = Random(seed)
    arrivals = []
    for t,m in product(range(420),range(7)):
        rate = SYNTHETIC[kind][m]
        if kind == "east_platoon" and m in (0,1):
            rate *= 3 if t % 84 < 24 else .20
        if rng.random() < rate:
            arrivals.append((t,m))
    links, green = STORAGE[storage]
    return Scenario(f"{kind}/{storage}/{seed}",420,tuple(arrivals),link=links,receive_green=green,
                    receive_offset=seed % 36)


def paired(s, fixed, seed, details, *, detectors=DETECTORS):
    fixed_values = evaluate(fixed,s,"fixed")
    alternatives = {f"{mode}/{name}": evaluate(fixed,s,mode,Observation(delay,miss,seed))
                    for name,(delay,miss) in detectors.items() for mode in ("queue","receiving")}
    return details | {"total_arrivals":len(s.arrivals),"fixed":fixed_values,
                      "alternate_fixed":evaluate(DEFAULT,s,"fixed"),"policies":alternatives}


def main(root):
    rows = [paired(synthetic(kind,storage,seed),FIXED,seed,
                   {"source":"synthetic","demand":kind,"storage":storage,"seed":seed})
            for kind,storage,seed in product(SYNTHETIC,STORAGE,SEEDS)]
    for block,seed in product(EVAL, (11,19,23,29)):
        s, d = case(root,block,seed)
        rows.append(paired(s,FIELD,seed,{"source":"DLR_hybrid","demand":block,"storage":"default",
                                        **d}))
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dlr_root",type=Path)
    parser.add_argument("output",type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(main(args.dlr_root),separators=(",",":"))+"\n")
