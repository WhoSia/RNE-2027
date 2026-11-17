"""Repeat the same pre-decision worlds across finite-pocket service calendars."""
import argparse
import json
from collections import Counter
from itertools import product
from pathlib import Path

from d51_phase_order import Params
from prospective_sensing import PROFILE, decision_record
from uncertain_pocket_sensing import bounded_error, by_count


CALENDARS = {
    "original": {},
    "clearance": {"intergreen_s": 5},
    "clearance_with_amber": {"intergreen_s": 5, "amber_service_s": 3},
    "clearance_with_headway": {"intergreen_s": 5, "service_headway_s": 2},
    "clearance_amber_headway": {"intergreen_s": 5, "amber_service_s": 3, "service_headway_s": 2},
}
MODES = ("exact", "fullness", "miss_one", "off_by_one")


def run_context(capacity, decision, cap, visible):
    rows = {}
    expected_worlds = None
    for key, calendar in CALENDARS.items():
        config = Params(horizon_s=240, left_capacity=capacity, **calendar)
        base, groups = by_count(visible, decision, cap, config)
        signature = base.paths, {count: bound.paths for count, bound in groups.items()}
        if expected_worlds is None:
            expected_worlds = signature
        if signature != expected_worlds:
            raise RuntimeError("A post-decision calendar changed pre-decision compatible worlds")
        rows[key] = {
            "choice": decision_record(base)["minimax_choice"],
            "delta_bounds": [base.low, base.high],
            "regret": base.regret,
            "sensor_regret": {mode: bounded_error(groups, capacity, mode)["worst_regret"] for mode in MODES},
        }
    return rows


def summarize(rows):
    result = {}
    for name in CALENDARS:
        panel = [item[name] for item in rows]
        strict_reversals = sum(
            {row[name]["choice"], row["original"]["choice"]} == {"lead", "lag"} for row in rows
        )
        result[name] = {
            "choices": dict(sorted(Counter(row["choice"] for row in panel).items())),
            "strict_choice_reversals_vs_original": strict_reversals,
            "positive_baseline_regret": sum(row["regret"] > 0 for row in panel),
            "sensor_improved": {mode: sum(row["sensor_regret"][mode] < row["regret"] for row in panel)
                                for mode in MODES},
            "max_reduction": {mode: max(row["regret"] - row["sensor_regret"][mode] for row in panel)
                              for mode in MODES},
        }
    return result


def experiment():
    panels = {}
    for capacities in ((1, 2), (3, 4)):
        rows = [run_context(capacity, decision, cap, visible) for capacity, decision, cap, visible in
                product(capacities, (6, 8), (2, 3), product(PROFILE, repeat=2))]
        panels["-".join(map(str, capacities))] = {"contexts": len(rows), "calendars": summarize(rows)}
    return {"configurations": CALENDARS, "capacity_panels": panels}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(experiment(), indent=2) + "\n", encoding="utf-8")
