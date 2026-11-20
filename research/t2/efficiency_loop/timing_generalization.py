"""Evaluate bypass timing on fixed new seeds and across terminal-cost settings."""
import argparse
from collections import Counter
import json
from pathlib import Path

from daypart_scenarios import worlds
from scarce_bypass import DECISION, matched_pocket_windows
from storage_information import SEEDS

NEW_SEEDS = (211, 337, 479, 613)
COUNTS = (1, 2, 6)
PENALTIES = (0, 60, 120)
INTERVAL = (30, 90)


def orientation(first, second, penalty):
    early = first[0] + penalty * first[1]
    late = second[0] + penalty * second[1]
    return 1 if early < 0 < late else -1 if late < 0 < early else 0


def compare(scenario, count):
    windows = {"early": range(DECISION, DECISION + count),
               "late": range(DECISION + 12 - count, DECISION + 12)}
    matched = matched_pocket_windows(scenario, windows)
    counts = Counter(dict.fromkeys((*map(str, PENALTIES), "robust_interval"), 0))
    witness = None
    for a, b in zip(matched["early"], matched["late"], strict=True):
        if a[:1] != b[:1] or a[2:4] != b[2:4]:
            raise AssertionError("The timing comparison altered input or decision state")
        early, late = a[-2:], b[-2:]
        for p in PENALTIES:
            counts[str(p)] += bool(orientation(early, late, p))
        lo, hi = (orientation(early, late, p) for p in INTERVAL)
        if lo and lo == hi:
            counts["robust_interval"] += 1
        if witness is None and orientation(early, late, 60):
            witness = {"bits": a[0], "early_components": early, "late_components": late}
    return {"streams": len(matched["early"]), "strict_reversals": dict(counts), "witness": witness}


def panel(seeds):
    scores = {}
    for count in COUNTS:
        contexts = {f"{seed}/{world.band}/{world.shape}": compare(world.scenario, count)
                    for seed in seeds for world in worlds(seed) if world.receiving == "constrained"}
        totals = Counter()
        for row in contexts.values():
            totals.update(row["strict_reversals"])
        scores[count] = {
            "streams": sum(row["streams"] for row in contexts.values()),
            "contexts_at_primary": sum(row["strict_reversals"]["60"] > 0 for row in contexts.values()),
            "strict_reversals": dict(totals), "contexts": contexts,
        }
    return {"seeds": seeds, "counts": scores}


def report():
    return {"control": panel(SEEDS), "new": panel(NEW_SEEDS), "penalties": PENALTIES,
            "robust_interval": INTERVAL}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(report(), sort_keys=True, separators=(",", ":"))+"\n",
                           encoding="utf-8")
