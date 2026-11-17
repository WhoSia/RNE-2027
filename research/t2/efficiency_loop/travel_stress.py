"""Matched travel-time stress, including the simulator's optimized path."""
import argparse
from dataclasses import replace
from itertools import product
import json
from pathlib import Path

from efficiency import evaluate
from policy_screen import synthetic, FIXED
from signal_model import run


def main():
    rows = []
    for demand, storage, seed, seconds in product(("east_platoon","cross_surge"),
            ("open","tight"), (227,449,671), (1,5,10)):
        s = replace(synthetic(demand,storage,seed),travel=(seconds,)*6)
        fixed = run(FIXED,s)
        fast = run(FIXED,s,fast=True)
        assert fixed == replace(fast,ticks=fixed.ticks)
        rows.append({"demand":demand,"storage":storage,"seed":seed,"travel_s":seconds,
                     "policies":{p:evaluate(FIXED,s,p) for p in ("fixed","queue","receiving")}})
    return rows


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("output",type=Path)
    a=p.parse_args()
    a.output.write_text(json.dumps(main(),separators=(",",":"))+"\n")
