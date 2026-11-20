"""Compare early and late masks at several fixed opportunity counts."""
import argparse
from collections import Counter
import json
from pathlib import Path

from bypass_windows import DECISION, INSTRUMENTS, compare_storage
from daypart_scenarios import worlds
from storage_information import SEEDS, matched_storage_cases

COUNTS = (1, 2, 3, 4, 6)


def matched_pocket_windows(scenario, windows):
    return {
        label: next(rows for name, _, _, rows in matched_storage_cases(
            scenario, bypass_depth=1, bypass_ticks=ticks
        ) if name == "pocket")
        for label, ticks in windows.items()
    }


def assess_world(scenario, windows):
    models = {
        label: {bits: (delta, pocket, receiver)
                for bits, delta, pocket, receiver, _, _ in rows}
        for label, rows in matched_pocket_windows(scenario, windows).items()
    }
    return compare_storage(models, windows)

def report():
    result = {}
    for count in COUNTS:
        windows = {"early": tuple(range(DECISION, DECISION + count)),
                   "late": tuple(range(DECISION + 12 - count, DECISION + 12))}
        cases = {f"{seed}/{world.band}/{world.shape}": assess_world(world.scenario, windows)
                 for seed in SEEDS for world in worlds(seed) if world.receiving == "constrained"}
        ambiguous = Counter()
        metrics = Counter()
        for row in cases.values():
            ambiguous.update(row["ambiguous"])
            metrics.update({key: value for key, value in row["equal_count_reversals"]["early/late"].items()
                            if key != "witness"})
        result[count] = {
            "windows": windows, "ambiguous": dict(ambiguous), "matched": dict(metrics),
            "max_regret": {name: max(row["max_regret"][name] for row in cases.values())
                           for name in INSTRUMENTS},
            "contexts": cases,
        }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(report(), sort_keys=True, separators=(",", ":"))+"\n",
                           encoding="utf-8")
