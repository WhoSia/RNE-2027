"""Check whether initial phase alone changes an otherwise identical comparison."""
import argparse
import json
from itertools import product
from pathlib import Path

from efficiency import evaluate
from policy_deep import EVAL_SEEDS
from policy_screen import synthetic
from signal_model import Plan


def main(fit_path):
    fits = json.loads(fit_path.read_text())["fixed_training"]
    rows = []
    for storage,demand,seed in product(("open","tight"),
                                       ("east_platoon","cross_surge","turn_surge"),EVAL_SEEDS):
        cfg=fits[storage]["plan"]
        plan=Plan(**(cfg | {"greens":tuple(cfg["greens"])}))
        s=synthetic(demand,storage,seed)
        fixed=evaluate(plan,s,"fixed")["cost"]
        costs=[evaluate(plan,s,"receiving",start_stage=i)["cost"] for i in range(4)]
        rows.append({"storage":storage,"demand":demand,"seed":seed,"fixed":fixed,
                     "start_stage_costs":costs})
    return rows


if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("fit_file",type=Path)
    p.add_argument("output",type=Path)
    a=p.parse_args()
    a.output.write_text(json.dumps(main(a.fit_file),indent=2)+"\n")
