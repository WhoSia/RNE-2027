"""Cross pocket and receiving capacities with matched daypart demand."""
import argparse
import json
from collections import Counter
from dataclasses import asdict, replace
from itertools import product
from pathlib import Path

from daypart_scenarios import BASELINE, worlds
from green_service_diagnosis import measure

SEEDS = (17, 83)
POCKETS = (1, 5)
RECEIVING = (2, 12)


def change_storage(scenario, pocket, receiving):
    bay = list(scenario.bay)
    link = list(scenario.link)
    for through in (0, 2):
        bay[through + 1] = pocket
        link[through] = receiving
    return replace(scenario, bay=tuple(bay), link=tuple(link))


def experiment():
    result = {}
    witnesses = {}
    for seed in SEEDS:
        for world in worlds(seed):
            if world.receiving != "constrained":
                continue
            for left_first in (False, True):
                plan = replace(BASELINE, left_first=left_first)
                key = f"{seed}/{world.band}/{world.shape}/{int(left_first)}"
                cases = {}
                for pocket, receiving in product(POCKETS, RECEIVING):
                    scenario = change_storage(world.scenario, pocket, receiving)
                    outcome, counts, examples = measure(plan, scenario)
                    tag = f"{pocket}/{receiving}"
                    for label, row in examples.items():
                        witnesses.setdefault(label, {"run": key, "capacities": tag, **asdict(row)})
                    cases[tag] = {
                        "counts": dict(counts),
                        "cost": outcome.cost,
                        "finished": sum(outcome.completed),
                    }
                result[key] = cases
    summaries = {}
    ranks = Counter()
    for pocket, receiving in product(POCKETS, RECEIVING):
        tag = f"{pocket}/{receiving}"
        counts = Counter()
        for cases in result.values():
            counts.update(cases[tag]["counts"])
        summaries[tag] = dict(counts)
        for key, cases in result.items():
            if not key.endswith("/0"):
                continue
            difference = result[key[:-1] + "1"][tag]["cost"] - cases[tag]["cost"]
            ranks[tag, "left_first" if difference < 0 else "through_first" if difference > 0 else "tie"] += 1
    rank_by_capacity = {tag: {order: count for (cell, order), count in ranks.items() if cell == tag}
                        for tag in summaries}
    return {"seeds": SEEDS, "counts_by_capacity": summaries,
            "preferred_order_by_capacity": rank_by_capacity,
            "first_witnesses": witnesses, "runs": result}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    report = experiment()
    runs = report.pop("runs")
    header = json.dumps(report, sort_keys=True, indent=2).removesuffix("\n}")
    rows = ",\n".join(f"    {json.dumps(key)}: {json.dumps(run, sort_keys=True)}"
                       for key, run in sorted(runs.items()))
    args.output.write_text(header + ',\n  "runs": {\n' + rows + "\n  }\n}\n", encoding="utf-8")
