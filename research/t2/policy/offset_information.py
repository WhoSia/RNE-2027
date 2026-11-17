"""Use the D48 exact offset sweep to value extra corridor information."""
import argparse
import json
from itertools import product
from pathlib import Path

from finite_storage_offset_v1 import Config, platoons, sweep

COUNTS = ((12, 6), (9, 9), (6, 12))
WEST_ONSETS = (0, 14)
STORAGE = ((3, 12), (12, 3))
TRAVEL_TIMES = (8, 16)
CYCLE = 60


def worlds():
    for counts, storage, onset, travel in product(COUNTS, STORAGE, WEST_ONSETS, TRAVEL_TIMES):
        east, west = (platoons(3, count, phase_s=phase)
                      for count, phase in zip(counts, (0, onset)))
        cfg = Config(travel_s=travel, horizon_s=1200,
                     east_link_capacity=storage[0], west_link_capacity=storage[1])
        results = sweep(east, west, cfg)
        name = f"{counts[0]}-{counts[1]}/{storage[0]}-{storage[1]}/{onset}/{travel}"
        if any(r.total_unserved or r.total_arrivals != len(east) + len(west) for r in results):
            raise RuntimeError(f"Failed to clear the matched demand in {name}")
        yield {"id": name, "counts": counts, "storage": storage, "west_onset_s": onset,
               "travel_s": travel, "costs": tuple(round(r.mean_delay_s * r.total_completed)
                                                for r in results),
               "blocked_green_s": tuple(r.blocked_green_seconds for r in results)}


def choose(rows, observed, regret):
    groups = {}
    for row in rows:
        key = tuple(row[name] for name in observed)
        groups.setdefault(key, []).append(row)
    decisions = {}
    for group in groups.values():
        reference = [(row["costs"], min(row["costs"]) if regret else 0) for row in group]
        value, offset = min((max(costs[o] - baseline for costs, baseline in reference), o)
                            for o in range(CYCLE))
        decisions.update((row["id"], offset) for row in group)
    return decisions


def experiment():
    rows = tuple(worlds())
    policies = {
        "zero_offset": dict.fromkeys((r["id"] for r in rows), 0),
        "pooled_minimax_cost": choose(rows, (), False),
        "pooled_minimax_regret": choose(rows, (), True),
        "counts": choose(rows, ("counts",), True),
        "counts_storage": choose(rows, ("counts", "storage"), True),
        "counts_storage_onset": choose(rows, ("counts", "storage", "west_onset_s"), True),
    }
    summary = {}
    for label, decisions in policies.items():
        costs, regrets, blocked = [], [], []
        for row in rows:
            offset = decisions[row["id"]]
            score = row["costs"][offset]
            costs.append(score)
            regrets.append(score - min(row["costs"]))
            blocked.append(row["blocked_green_s"][offset])
        summary[label] = {"worst_cost_s": max(costs), "worst_regret_s": max(regrets),
                          "sum_cost_s": sum(costs), "worst_blocked_green_s": max(blocked),
                          "distinct_offsets": sorted(set(decisions.values()))}
    return {"offsets_s": list(range(CYCLE)), "summary": summary, "decisions": policies, "worlds": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    report = experiment()
    worlds = report.pop("worlds")
    header = json.dumps(report, indent=2)[:-2]
    rows = ",\n".join("    " + json.dumps(row, separators=(",", ":")) for row in worlds)
    args.output.write_text(header + ',\n  "worlds": [\n' + rows + "\n  ]\n}\n", encoding="utf-8")
