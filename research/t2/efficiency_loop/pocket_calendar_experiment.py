"""Repeat the same pre-decision worlds across finite-pocket service calendars."""
import argparse
import json
from collections import Counter
from itertools import product
from pathlib import Path
from types import SimpleNamespace

from d51_phase_order import Params
from prospective_sensing import PROFILE
from uncertain_pocket_sensing import bounded_error, by_count


CALENDARS = {
    "original": {},
    "clearance": {"intergreen_s": 5},
    "clearance_with_amber": {"intergreen_s": 5, "amber_service_s": 3},
    "clearance_with_headway": {"intergreen_s": 5, "service_headway_s": 2},
    "clearance_amber_headway": {"intergreen_s": 5, "amber_service_s": 3, "service_headway_s": 2},
}
MODES = ("exact", "fullness", "miss_one", "off_by_one")


def union_groups(groups_by_calendar):
    return {
        count: SimpleNamespace(
            low=min(groups[count].low for groups in groups_by_calendar),
            high=max(groups[count].high for groups in groups_by_calendar),
        )
        for count in groups_by_calendar[0]
    }


def record(low, high, groups, capacity):
    lag, lead = max(0, -low), max(0, high)
    return {
        "choice": "lag" if lag < lead else "lead" if lead < lag else "either",
        "delta_bounds": [low, high],
        "regret": min(lag, lead),
        "sensor_regret": {mode: bounded_error(groups, capacity, mode)["worst_regret"] for mode in MODES},
    }


def run_context(capacity, decision, cap, visible):
    rows = {}
    expected_worlds = None
    groups_by_calendar = []
    for key, calendar in CALENDARS.items():
        config = Params(horizon_s=240, left_capacity=capacity, **calendar)
        base, groups = by_count(visible, decision, cap, config)
        signature = base.paths, {count: bound.paths for count, bound in groups.items()}
        if expected_worlds is None:
            expected_worlds = signature
        if signature != expected_worlds:
            raise RuntimeError("A post-decision calendar changed pre-decision compatible worlds")
        rows[key] = record(base.low, base.high, groups, capacity)
        groups_by_calendar.append(groups)
    combined = union_groups(groups_by_calendar)
    low = min(group.low for group in combined.values())
    high = max(group.high for group in combined.values())
    rows["unknown_calendar"] = record(low, high, combined, capacity)
    for name in CALENDARS:
        for mode in MODES:
            if rows["unknown_calendar"]["sensor_regret"][mode] < rows[name]["sensor_regret"][mode]:
                raise RuntimeError("Unknown calendar improved a worst-case sensor regret")
    return rows


def summarize(rows):
    result = {}
    for name in (*CALENDARS, "unknown_calendar"):
        panel = [item[name] for item in rows]
        strict_reversals = sum(
            {row[name]["choice"], row["original"]["choice"]} == {"lead", "lag"} for row in rows
        )
        result[name] = {
            "choices": dict(sorted(Counter(row["choice"] for row in panel).items())),
            "strict_choice_reversals_vs_original": strict_reversals,
            "interval_changed_vs_clearance": sum(
                row[name]["delta_bounds"] != row["clearance"]["delta_bounds"] for row in rows
            ),
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
