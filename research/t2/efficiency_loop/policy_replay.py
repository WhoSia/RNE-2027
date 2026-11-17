"""Transfer realized actuated schedules between episodes to isolate feedback."""
import argparse
import json
from pathlib import Path
from statistics import mean

from efficiency import evaluate
from policy_deep import EVAL_SEEDS
from policy_screen import synthetic
from signal_model import Plan, run


def transfer(fit_path):
    fits = json.loads(fit_path.read_text())["fixed_training"]
    rows = []
    for storage in ("open", "tight"):
        cfg = fits[storage]["plan"]
        plan = Plan(**(cfg | {"greens":tuple(cfg["greens"])}))
        for demand in ("east_platoon","cross_surge","turn_surge"):
            scenarios = [synthetic(demand,storage,seed) for seed in EVAL_SEEDS]
            closed = [evaluate(plan,s,"receiving",trace=True) for s in scenarios]
            schedules = [tuple(r[2] for r in c["trace"]) for c in closed]
            for i,s in enumerate(scenarios):
                self_cost = run(plan,s,controller=lambda t,*_: schedules[i][t]).cost
                if self_cost != closed[i]["cost"]:
                    raise AssertionError("open-loop replay changed the realized policy outcome")
                donor_costs = [run(plan,s,controller=lambda t,*_: schedule[t]).cost
                               for j,schedule in enumerate(schedules) if j != i]
                rows.append({"storage":storage,"demand":demand,"seed":EVAL_SEEDS[i],
                             "closed":self_cost,"fixed":run(plan,s).cost,"donor_costs":donor_costs,
                             "mean_donor_cost":mean(donor_costs)})
    return rows


if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("fit_file",type=Path)
    p.add_argument("output",type=Path)
    a=p.parse_args()
    a.output.write_text(json.dumps(transfer(a.fit_file),indent=2)+"\n")
