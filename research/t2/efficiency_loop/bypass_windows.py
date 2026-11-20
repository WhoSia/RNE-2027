"""Equal-count schedules and information value for intermittent overtaking."""
import argparse
from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path

from daypart_scenarios import worlds
from storage_information import BIN_STARTS, CAPACITIES, DECISION, SEEDS, decision, matched_storage_cases

CLOSED = sum(start + 2 <= DECISION for start in BIN_STARTS)
WINDOWS = {
    "early": tuple(range(DECISION, DECISION + 6)),
    "late": tuple(range(DECISION + 6, DECISION + 12)),
    "alternating": tuple(range(DECISION, DECISION + 12, 2)),
}
INSTRUMENTS = ("none", "open_at_decision", "window", "future_arrivals", "both")


def information_scores(rows, windows=WINDOWS):
    partitions = {name: defaultdict(list) for name in INSTRUMENTS}
    for label, starts, delta in rows:
        keys = (None, DECISION in windows[label], label, starts, (label, starts))
        for table, key in zip(partitions.values(), keys, strict=True):
            table[key].append(delta)
    result = {name: max(decision(values)["regret"] for values in table.values())
              for name, table in partitions.items()}
    assert result["both"] == 0
    assert result["window"] <= result["open_at_decision"] <= result["none"]
    assert result["future_arrivals"] <= result["none"]
    return result


def compare_storage(models, windows=WINDOWS):
    groups = defaultdict(list)
    reversals = {}
    for first, second in combinations(windows, 2):
        a, b = models[first], models[second]
        if a.keys() != b.keys():
            raise AssertionError("Unequal arrival enumeration")
        switches = [(bits, a[bits][0], b[bits][0]) for bits in a
                    if a[bits][0] * b[bits][0] < 0]
        reversals[f"{first}/{second}"] = {
            "count": len(switches),
            "changed": sum(a[bits][0] != b[bits][0] for bits in a),
            "ties_changed": sum((a[bits][0] == 0) != (b[bits][0] == 0) for bits in a),
            "witness": max(switches, key=lambda row: min(abs(row[1]), abs(row[2])),
                           default=None),
        }
    for label, rows in models.items():
        for bits, (delta, pocket, receiver) in rows.items():
            if (pocket, receiver) != models["early"][bits][1:]:
                raise AssertionError("A future schedule altered the pre-decision observation")
            groups[bits[:CLOSED], pocket, receiver].append((label, bits[CLOSED:], delta))
    regrets = [information_scores(rows, windows) for rows in groups.values()]
    counts = {name: sum(record[name] > 0 for record in regrets) for name in INSTRUMENTS}
    maxima = {name: max(record[name] for record in regrets) for name in INSTRUMENTS}
    return {"groups": len(groups), "ambiguous": counts, "max_regret": maxima,
            "equal_count_reversals": reversals}


def compare_context(scenario):
    variants = defaultdict(dict)
    for label, ticks in WINDOWS.items():
        for storage, _, _, rows in matched_storage_cases(scenario, bypass_depth=1,
                                                          bypass_ticks=ticks):
            variants[storage][label] = {bits: (delta, pocket, receiver)
                                        for bits, delta, pocket, receiver, _, _ in rows}
    return {name: compare_storage(models) for name, models in variants.items()}


def report():
    cases = {f"{seed}/{w.band}/{w.shape}": compare_context(w.scenario)
             for seed in SEEDS for w in worlds(seed) if w.receiving == "constrained"}
    totals = {}
    for storage in CAPACITIES:
        rows = [context[storage] for context in cases.values()]
        counts, reversals = Counter(), Counter()
        for row in rows:
            counts.update(row["ambiguous"])
            reversals.update({pair: v["count"] for pair, v in row["equal_count_reversals"].items()})
        totals[storage] = {
            "groups": sum(row["groups"] for row in rows),
            "ambiguous": dict(counts), "equal_count_reversals": dict(reversals),
            "max_regret": {name: max(row["max_regret"][name] for row in rows)
                           for name in INSTRUMENTS},
        }
    return {"windows": WINDOWS, "terminal": 60, "contexts": cases, "totals": totals}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(report(), sort_keys=True, separators=(",", ":"))+"\n",
                           encoding="utf-8")
