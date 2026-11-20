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


def compare_context(scenario):
    baseline = {}
    scores = {}
    for depth in DEPTHS:
        depth_scores = {}
        for name, _, _, rows in matched_storage_cases(scenario, bypass_depth=depth):
            by_stream = {row[0]: (row[1], row[2:4]) for row in rows}
            if depth == 0:
                baseline[name] = by_stream
            original = baseline[name]
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
    return scores


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
                row = context[depth][storage]
                count.update({key: row[key] for key in metrics})
                count["ambiguous_groups"] += len(row["ambiguous"])
            totals[depth][storage] = dict(count)
    return {"decision_tick": DECISION, "terminal": 60, "depths": DEPTHS,
            "totals": totals, "contexts": contexts}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(report(), sort_keys=True, separators=(",", ":"))+"\n",
                           encoding="utf-8")
