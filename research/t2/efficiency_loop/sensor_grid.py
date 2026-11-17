"""Test deterioration with sensing latency and loss on a matched arrival cohort."""
import argparse
from itertools import product
import json
from pathlib import Path
from statistics import mean

from actuated import Observation
from efficiency import evaluate
from field_replay import EVAL
from field_scenarios import case
from policy_deep import EVAL_SEEDS
from policy_screen import synthetic
from signal_model import Plan


def main(root, fitted):
    cases = {k:[] for k in ("open","tight","DLR_hybrid")}
    for storage, kind, seed in product(("open","tight"),("east_platoon","cross_surge"),EVAL_SEEDS):
        cases[storage].append((synthetic(kind,storage,seed),seed))
    for block,seed in product(EVAL,(31,37,41,43)):
        cases["DLR_hybrid"].append((case(root,block,seed)[0],seed))
    grid = []
    for group, inputs in cases.items():
        p = Plan(**(fitted[group]["plan"] | {"greens":tuple(fitted[group]["plan"]["greens"])}))
        base = [evaluate(p,s,"fixed") for s,_ in inputs]
        for delay, loss in product((0,2,4,6,8),(0,.15,.30)):
            result = [evaluate(p,s,"receiving",Observation(delay,loss,seed)) for s,seed in inputs]
            paired = [100*(r["cost"]/f["cost"]-1) for r,f in zip(result,base)]
            grid.append({"group":group,"delay_ticks":delay,"independent_occupancy_miss_probability":loss,
                         "n":len(inputs),"mean_cost_change_pct":mean(paired),
                         "worst_cost_change_pct":max(paired),"wins":sum(x<0 for x in paired),
                         "max_ped_wait_worse":sum(r["maximum_observed_wait"][6] >
                                                 f["maximum_observed_wait"][6] for r,f in zip(result,base))})
    return grid


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("dlr_root",type=Path)
    p.add_argument("fit_file",type=Path)
    p.add_argument("output",type=Path)
    a=p.parse_args()
    fits=json.loads(a.fit_file.read_text())["fixed_training"]
    a.output.write_text(json.dumps(main(a.dlr_root,fits),indent=2)+"\n")
