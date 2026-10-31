"""Bounded bypass thought experiment for v0.9, paired 8-seed grid.

The lookahead is an abstract queue reordering option; it is NOT an
implementation of geographic multi-lane maneuvers or real driver behavior.
"""
from __future__ import annotations
from dataclasses import replace
from statistics import mean
import json,sys
from pathlib import Path
from world_contact_v09 import Params,demand,run

LENGTHS=(14,28,42,70)
POLICIES=(("fifo",1),("window",2),("window",4),("window",8),("bypass",999))

def execute():
    raw=[]
    for seed in range(8):
        base=Params(seed=seed)
        arrival=demand(base)
        for length in LENGTHS:
            for policy,window in POLICIES:
                c=replace(base,bay_length_m=length,feeder_policy=policy,bypass_window=window)
                y=run(c,arrival)
                raw.append({"seed":seed,"bay_m":length,"policy":policy,
                            "lookahead":window,"through_exits":y["exits_S"],
                            "left_exits":y["exits_L"],"outside":y["still_outside"],
                            "bypassed_head_positions":y["bypassed_head_vehicles"]})
    means=[]
    for policy,window in POLICIES:
        for length in LENGTHS:
            group=[r for r in raw if (r["policy"],r["lookahead"],r["bay_m"])==(policy,window,length)]
            means.append({"policy":policy,"lookahead":window,"bay_m":length,"n":len(group),
                          "mean_through":mean(r["through_exits"] for r in group),
                          "mean_left":mean(r["left_exits"] for r in group),
                          "mean_outside":mean(r["outside"] for r in group),
                          "mean_bypassed_head_positions":mean(r["bypassed_head_positions"] for r in group)})
    return {"world_status":"SYNTHETIC_NOT_FIELD_VALIDATED","n":len(raw),
            "rows":raw,"means":means,
            "interpretation":"Lookahead modifies virtual queue order, not a physically feasible lane-change path."}

if __name__=="__main__":
    p=Path(sys.argv[1] if len(sys.argv)>1 else "research/t2/results/window_sensitivity_v09.json")
    p.parent.mkdir(parents=True,exist_ok=True)
    d=execute();p.write_text(json.dumps(d,indent=2)+"\n")
    print("simulations",d["n"],"condition means",len(d["means"]))
