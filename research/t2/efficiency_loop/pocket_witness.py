"""Reproduce a policy reversal on identical arrivals with different initial queues."""
import argparse
from dataclasses import replace
import json
from pathlib import Path

from d51_phase_order import Params, phase
from phase_bounds_dp import EMPTY, advance, inventory

DEMAND = ("","T","T","","","T","L","","")
DECISION = 8


def replay(config, arrivals, initial, decision):
    state = initial
    area = 0
    trace = []
    before_pocket = None
    source_waiting_behind_left = 0
    for tick in range(config.horizon_s):
        if tick == decision:
            before_pocket = state[2]
        arrival = arrivals[tick] if tick < len(arrivals) else ""
        green = phase(tick-decision,config) if tick >= decision else "R"
        arriving_source = state[0]+arrival
        blocked = (state[2] == config.left_capacity and arriving_source.startswith("L") and
                   "T" in arriving_source[1:])
        source_waiting_behind_left += blocked
        state = advance(state,arrival,green,config.through_capacity,config.left_capacity,False)
        area += inventory(state)
        trace.append({"t":tick,"arrival":arrival,"green":green,
                      "fifo":state[0],"through":state[1],"left":state[2]})
        if state == EMPTY and tick >= max(decision,len(arrivals)-1):
            return {"pocket_at_decision":before_pocket,"area_vehicle_seconds":area,
                    "source_waiting_behind_left_ticks":source_waiting_behind_left,"trace":trace}
    raise ValueError("Witness did not drain")


def witness():
    config = Params(left_capacity=2,horizon_s=180)
    variants = {}
    for capacity in (2,3):
        for label,initial in (("empty_initial",("",0,0)),("one_left_initial",("",0,1))):
            out = {name:replay(replace(config,left_capacity=capacity,left_first=lead),DEMAND,initial,DECISION)
                   for name,lead in (("lag",False),("lead",True))}
            assert out["lag"]["pocket_at_decision"] == out["lead"]["pocket_at_decision"]
            variants[f"capacity_{capacity}_{label}"] = out
    return {"decision_tick":DECISION,"arrivals":DEMAND,"variants":variants}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output",type=Path)
    parser.add_argument("--trace", action="store_true")
    args = parser.parse_args()
    result = witness()
    if not args.trace:
        result["summary"] = {}
        for name, variants in result.pop("variants").items():
            stats = {plan:{k:v for k,v in run.items() if k != "trace"}
                     for plan,run in variants.items()}
            stats["delta_lead_minus_lag"] = (stats["lead"]["area_vehicle_seconds"]
                                           - stats["lag"]["area_vehicle_seconds"])
            result["summary"][name] = stats
    args.output.write_text(json.dumps(result,indent=2)+"\n")
