"""Follow arrival-order ambiguity under a bounded relaxation of approach FIFO."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

from daypart_scenarios import worlds
from storage_information import BIN_STARTS, CAPACITIES, DECISION, SEEDS, decision, matched_storage_cases

DEPTHS = (0, 1, 3)
CLOSED = sum(t + 2 <= DECISION for t in BIN_STARTS)


def summarize(rows):
    groups = defaultdict(list)
    for bits, delta, pocket, link, _, _ in rows:
        groups[bits[:CLOSED], pocket, link].append((bits, delta))
    ambiguous = {}
    for key, compatible in sorted(groups.items()):
        record = decision([delta for _, delta in compatible])
        if record["regret"]:
            lo, hi = (pick(compatible, key=lambda row: row[1]) for pick in (min, max))
            label = "".join(map(str, key[0])) + f"/{key[1]}/{key[2]}"
            ambiguous[label] = record | {"witness": (lo, hi)}
    return {"groups": len(groups), "ambiguous": ambiguous}


def access_uncertainty(models):
    """Check whether the whole arrival stream resolves unknown bypass access."""
    incompatible = []
    for bits in models[0]:
        rows = [(depth, *model[bits]) for depth, model in models.items()]
        states = defaultdict(list)
        for depth, delta, state in rows:
            states[state].append((depth, delta))
        for state, candidates in states.items():
            low, high = (pick(candidates, key=lambda pair: pair[1]) for pick in (min, max))
            if low[1] < 0 < high[1]:
                incompatible.append({"arrivals": bits, "occupancy": state,
                                     "lower": low, "upper": high,
                                     "regret": min(-low[1], high[1])})
                break
    return {"incompatible_streams": len(incompatible),
            "witness": max(incompatible, key=lambda row: row["regret"], default=None)}


def compare_context(scenario):
    scores = {}
    models_by_storage = defaultdict(dict)
    for depth in DEPTHS:
        depth_scores = {}
        for name, _, _, rows in matched_storage_cases(scenario, bypass_depth=depth):
            by_stream = {row[0]: (row[1], row[2:4]) for row in rows}
            models_by_storage[name][depth] = by_stream
            original = models_by_storage[name][0]
            if original.keys() != by_stream.keys():
                raise AssertionError("Overtaking changed the compared arrival streams")
            depth_scores[name] = summarize(rows) | {
                "changed_cost_difference": sum(delta != original[bits][0]
                                               for bits, (delta, _) in by_stream.items()),
                "strict_phase_reversals": sum(delta * original[bits][0] < 0
                                              for bits, (delta, _) in by_stream.items()),
                "changed_observation": sum(state != original[bits][1]
                                           for bits, (_, state) in by_stream.items()),
            }
        scores[depth] = depth_scores
    return {"depths": scores, "unknown_access": {
        name: access_uncertainty(models) for name, models in models_by_storage.items()
    }}


def report():
    contexts = {f"{seed}/{world.band}/{world.shape}": compare_context(world.scenario)
                for seed in SEEDS for world in worlds(seed) if world.receiving == "constrained"}
    metrics = ("groups", "strict_phase_reversals", "changed_cost_difference", "changed_observation")
    totals = {}
    for depth in DEPTHS:
        totals[depth] = {}
        for storage in CAPACITIES:
            count = Counter()
            for context in contexts.values():
                row = context["depths"][depth][storage]
                count.update({key: row[key] for key in metrics})
                count["ambiguous_groups"] += len(row["ambiguous"])
            totals[depth][storage] = dict(count)
    access_totals = {
        name: sum(c["unknown_access"][name]["incompatible_streams"] for c in contexts.values())
        for name in CAPACITIES
    }
    return {"decision_tick": DECISION, "terminal": 60, "depths": DEPTHS,
            "totals": totals, "unknown_access_totals": access_totals, "contexts": contexts}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(report(), sort_keys=True, separators=(",", ":"))+"\n",
                           encoding="utf-8")
