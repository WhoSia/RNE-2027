"""Compute a policy frontier under a single demand and receiving condition."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path

from efficiency import evaluate
from optimize import catalog
from policy_screen import FIXED, synthetic


def main():
    s = synthetic("east_platoon","tight",227)
    plans = sorted(catalog())
    points = {}
    for plan in plans:
        out = evaluate(plan,s,"fixed")
        metrics = out["cost"], out["maximum_observed_wait"][6]
        points.setdefault(metrics,plan)
    nondominated = []
    minimum_wait = float("inf")
    for (cost,wait), plan in sorted(points.items()):
        if wait < minimum_wait:
            nondominated.append({"cost":cost,"pedestrian_wait_s":wait,"plan":asdict(plan)})
            minimum_wait = wait
    base = {k:evaluate(FIXED,s,k) for k in ("fixed","queue","receiving","confirmed")}
    return {"scenario":s.name,"fixed_candidates":len(plans),"frontier":nondominated,
            "reference_policies":{k:{"cost":v["cost"],"pedestrian_wait_s":v["maximum_observed_wait"][6],
                                     "pedestrian_area":v["area_by_movement"][6],
                                     "pedestrian_remaining":v["remaining"][6]}
                                  for k,v in base.items()}}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("output",type=Path)
    a=p.parse_args()
    a.output.write_text(json.dumps(main(),indent=2)+"\n")
