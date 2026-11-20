"""Paired phase-order effects and pre-decision occupancy information."""
import argparse
from collections import defaultdict
from dataclasses import replace
from itertools import product
import json
from pathlib import Path

from daypart_scenarios import BASELINE, worlds
from green_service_experiment import SEEDS, change_storage
from signal_model import calendar, masks, run

DECISION = BASELINE.cycle
BIN_STARTS = tuple(range(DECISION - 6, DECISION + 6, 2))
CAPACITIES = {
    "unbound": (False, False),
    "pocket": (True, False),
    "receiver": (False, True),
    "both": (True, True),
}
EDGES = (
    ("unbound", "pocket"), ("unbound", "receiver"),
    ("pocket", "both"), ("receiver", "both"),
)
ORDERS = tuple(replace(BASELINE, left_first=first) for first in (False, True))
INSTRUMENTS = ("baseline", "pocket_full", "receiver_full", "both_fullness", "both_counts")


def paired_bins(arrivals, orders):
    background = [row for row in arrivals
                  if not (row[1] in (0, 1) and BIN_STARTS[0] <= row[0] < BIN_STARTS[-1] + 2)]
    added = [(start + offset, first ^ offset)
             for start, first in zip(BIN_STARTS, orders, strict=True)
             for offset in (0, 1)]
    return tuple(sorted(background + added, key=lambda row: row[0]))


def compare_orders(scenario):
    schedules = [masks(DECISION, calendar(plan, scenario.headway)) for plan in ORDERS]
    states, costs = [], []
    for schedule in schedules:
        def controller(tick, bay, link, pedestrians):
            if tick == DECISION:
                states.append((bay, link, pedestrians))
            active = schedules[0] if tick < DECISION else schedule
            return active[tick % DECISION]

        costs.append(run(BASELINE, scenario, controller=controller).cost)
    if len(states) != 2 or states[0] != states[1]:
        raise AssertionError("The phase alternatives diverged before the decision")
    bay, link, _ = states[0]
    return costs[1] - costs[0], bay[1], link[0]


def decision(values):
    low, high = min(values), max(values)
    left, through = max(0, high), max(0, -low)
    return {
        "bounds": [low, high],
        "worlds": len(values),
        "regret": min(left, through),
        "minimax_order": ("left_first" if left < through else
                          "through_first" if through < left else "either"),
    }


def partition(rows, pocket_limit, link_limit):
    groups = {name: defaultdict(list) for name in INSTRUMENTS}
    for _, delta, pocket, link in rows:
        pf = int(pocket == pocket_limit)
        lf = int(link == link_limit)
        for name, key in zip(INSTRUMENTS, ("all", str(pf), str(lf), f"{pf}/{lf}", f"{pocket}/{link}"),
                             strict=True):
            groups[name][key].append(delta)
    instruments = {}
    for name, branches in groups.items():
        decisions = {key: decision(values) for key, values in sorted(branches.items())}
        if sum(row["worlds"] for row in decisions.values()) != len(rows):
            raise AssertionError("Different instruments received different compatible worlds")
        instruments[name] = {"branches": decisions,
                             "regret": max(row["regret"] for row in decisions.values())}
    r = {name: info["regret"] for name, info in instruments.items()}
    assert r["both_counts"] <= r["both_fullness"] <= min(r["pocket_full"], r["receiver_full"])
    assert max(r["pocket_full"], r["receiver_full"]) <= r["baseline"]
    return instruments


def build_context(scenario):
    streams = {bits: paired_bins(scenario.arrivals, bits)
               for bits in product((0, 1), repeat=len(BIN_STARTS))}
    unbound = max(map(len, streams.values())) + 1
    by_storage = {}
    for name, (finite_pocket, finite_link) in CAPACITIES.items():
        pocket_limit = 1 if finite_pocket else unbound
        link_limit = 2 if finite_link else unbound
        fixed = change_storage(scenario, pocket_limit, link_limit)
        rows = []
        for bits, arrivals in streams.items():
            current = replace(fixed, arrivals=arrivals)
            delta, pocket, link = compare_orders(current)
            rows.append((bits, delta, pocket, link))
        instruments = partition(rows, pocket_limit, link_limit)
        low = min(rows, key=lambda row: row[1])
        high = max(rows, key=lambda row: row[1])
        by_storage[name] = (rows, {
            "instruments": instruments,
            "extreme_worlds": (low, high),
        })
    reversals = {}
    for first, second in EDGES:
        left, right = by_storage[first][0], by_storage[second][0]
        opposite = [(a[0], a[1], b[1]) for a, b in zip(left, right, strict=True)
                    if a[1] * b[1] < 0]
        reversals[f"{first}->{second}"] = {
            "strict_reversals": len(opposite), "witness": next(iter(opposite), None)
        }
    return {"storage": {name: out for name, (_, out) in by_storage.items()}, "edges": reversals}


def report():
    contexts = {
        f"{seed}/{world.band}/{world.shape}": build_context(world.scenario)
        for seed in SEEDS for world in worlds(seed) if world.receiving == "constrained"
    }
    edges = {f"{a}->{b}": sum(context["edges"][f"{a}->{b}"]["strict_reversals"]
                              for context in contexts.values()) for a, b in EDGES}
    summaries = {}
    for storage in CAPACITIES:
        panels = [context["storage"][storage]["instruments"] for context in contexts.values()]
        summaries[storage] = {
            instrument: {
                "positive_regret_contexts": sum(p[instrument]["regret"] > 0 for p in panels),
                "strict_improvement_contexts": sum(p[instrument]["regret"] < p["baseline"]["regret"]
                                                  for p in panels),
                "max_regret_reduction": max(p["baseline"]["regret"] - p[instrument]["regret"]
                                            for p in panels),
            } for instrument in INSTRUMENTS
        }
    return {"decision_tick": DECISION, "mixed_bin_starts": BIN_STARTS,
            "models_per_context": (2**len(BIN_STARTS)) * len(CAPACITIES) * len(ORDERS),
            "edge_reversals": edges, "sensor_summary": summaries, "contexts": contexts}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(report(), ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":")) + "\n", encoding="utf-8")
