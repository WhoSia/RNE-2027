"""Audit what changes when the discrete cycle length is also a decision."""
import argparse
from dataclasses import asdict, replace
import json
from pathlib import Path

from experiments import generated
from optimize import catalog, search


def main():
    base = generated()
    rows = []
    for horizon, penalty in ((336, 0), (336, 60), (336, 120), (240, 60)):
        cases = tuple(replace(s, terminal=penalty, horizon=horizon,
                              arrivals=tuple((t,m) for t,m in s.arrivals if t<horizon))
                      for s in base)
        candidates = tuple(p for cycle in (72,84,96) for p in catalog(cycle))
        winner = search(candidates,cases)
        by_cycle = {cycle: search(catalog(cycle),cases) for cycle in (72,84,96)}
        assert (winner.value,winner.plan) == min((x.value,x.plan) for x in by_cycle.values())
        rows.append({"horizon":horizon,"terminal_penalty":penalty,"candidates":len(candidates),
                     "winner":asdict(winner),"winner_cycle":winner.plan.cycle,
                     "per_cycle":{cycle:asdict(x) for cycle,x in by_cycle.items()}})
    return rows


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("output",type=Path)
    a=p.parse_args()
    a.output.write_text(json.dumps(main(),indent=2)+"\n")
