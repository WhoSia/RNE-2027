"""Replay the predecision grid against the exhaustive fixed-plan reference."""
import argparse
from itertools import product
import json
from pathlib import Path
import runpy
from statistics import median
from time import perf_counter

from d51_phase_order import Params
from sensing import MOVEMENT, PRESENCE, compare
from timing_bounds import exact


def inputs():
    config = Params(left_capacity=1, horizon_s=180)
    initial = (("",0,0), ("",0,1))
    fixed = ((1,1),(2,0),(2,0),(1,1))
    yield from ((3,fixed,config,d,partition,b,initial)
                for d,partition,b in product((4,8,12),(PRESENCE,MOVEMENT),(1,2)))
    options = ((1,1),(2,0),(0,2),(1,0),(0,1))
    for bins, decision in product(product(options,repeat=3),(4,8,9)):
        if exact(3,bins,config,initial=initial,decision_tick=decision).regret > 0:
            yield 3,bins,config,decision,MOVEMENT,2,initial


def audit(reference, runs):
    cases = list(inputs())
    methods = {"exhaustive": reference, "pruned": compare}
    times = {k: [] for k in methods}
    outputs = {}
    for i in range(runs):
        order = tuple(methods) if i % 2 == 0 else tuple(reversed(methods))
        for name in order:
            start = perf_counter()
            outputs[name] = [methods[name](*case) for case in cases]
            times[name].append(perf_counter()-start)
    calls = {}
    for name, rows in outputs.items():
        calls[name] = sum(row.pop("exact_dp_calls") for row in rows)
    pruned = sum(row.pop("pruned_fixed_plans") for row in outputs["pruned"])
    if outputs["pruned"] != outputs["exhaustive"]:
        raise ValueError("Pruning changed a decision or an evidence bound")
    return {"grid_cases": len(cases), "same_reported_answers": True, "exact_dp_calls": calls,
            "fixed_plans_cut_short": pruned, "wall_seconds": times,
            "median_wall_seconds": {name: median(values) for name, values in times.items()}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("reference", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--runs", type=int, default=4)
    args = parser.parse_args()
    if args.runs < 1:
        parser.error("--runs must be positive")
    result = audit(runpy.run_path(str(args.reference))["compare"], args.runs)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
