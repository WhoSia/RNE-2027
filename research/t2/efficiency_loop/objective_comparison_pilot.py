"""Paired objective comparison motivated by the Tan et al. full article."""
import argparse
import json
from collections import Counter
from itertools import product
from pathlib import Path

from d51_phase_order import Params
from forecast_objectives import evaluate
from prospective_sensing import PROFILE
from uncertain_pocket_sensing import by_count


def pilot():
    summary = {}
    for capacity, amber in product((1, 3), (0, 3)):
        differences = Counter()
        witness = None
        worlds = 0
        p = Params(left_capacity=capacity, horizon_s=240, intergreen_s=5, amber_service_s=amber)
        for decision, visible in product((6, 8), product(PROFILE, repeat=2)):
            record = evaluate(visible, decision, 2, p)
            b, _ = by_count(visible, decision, 2, p)
            if (record["worlds"], record["delta_bounds"]) != (b.paths, [b.low, b.high]):
                raise RuntimeError("The enumerator and exact DP disagree")
            absolute, regret = record["absolute_choice"], record["regret_choice"]
            differences["same" if absolute == regret else
                        "tie_disagreement" if "either" in (absolute, regret) else "opposite"] += 1
            worlds += b.paths
            if {absolute, regret} == {"lag", "lead"} and witness is None:
                witness = {"decision": decision, "visible_counts": visible, **record}
        summary[f"capacity-{capacity}_amber-{amber}"] = {
            "contexts": sum(differences.values()), "world_evaluations": worlds,
            "comparisons": dict(sorted(differences.items())), "first_opposite_witness": witness,
        }
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(pilot(), indent=2) + "\n", encoding="utf-8")
