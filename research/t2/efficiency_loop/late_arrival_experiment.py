"""Paired D51 comparison of the two phase orders at late arrival boundaries."""
import argparse
import json
from collections import Counter
from dataclasses import replace
from itertools import product
from math import isclose
from pathlib import Path

from d51_phase_order import Params, Vehicle, simulate

WINDOWS = {"early_edge": range(8, 19), "late_edge": range(26, 36)}
PATTERNS = {
    "left": ((0, "L"),),
    "left_then_through": ((0, "L"), (1, "T")),
    "two_left_then_through": ((-1, "L"), (0, "L"), (1, "T")),
}
COLUMNS = ("window", "arrival_s", "pattern", "left_capacity", "headway_s",
           "lag_no_amber", "lead_no_amber", "lag_amber", "lead_amber",
           "contrast_no_amber", "contrast_amber", "classification")


def classification(before, after):
    if before == after:
        return "unchanged"
    if before * after < 0:
        return "strict_reversal"
    if before == 0 or after == 0:
        return "tie_transition"
    return "same_sign_change"


def cost(vehicles, params):
    outcome = simulate(vehicles, params)
    if outcome.unserved or outcome.completed_through + outcome.completed_left != len(vehicles):
        raise RuntimeError("Every arm must serve the same arrivals before the horizon")
    delay = outcome.mean_vehicle_delay_s * len(vehicles)
    integer_delay = round(delay)
    if not isclose(delay, integer_delay, rel_tol=0, abs_tol=1e-9):
        raise RuntimeError("D51 total delay must be integral")
    return integer_delay


def experiment():
    rows = []
    counts = Counter()
    by_window = {name: Counter() for name in WINDOWS}
    by_pattern = {name: Counter() for name in PATTERNS}
    by_headway = {value: Counter() for value in (1, 2)}
    for window, ticks in WINDOWS.items():
        for arrival, pattern, capacity, headway in product(ticks, PATTERNS, (1, 3), (1, 2)):
            vehicles = tuple(Vehicle(arrival + offset, movement, i)
                             for i, (offset, movement) in enumerate(PATTERNS[pattern]))
            settings = Params(horizon_s=240, intergreen_s=5, left_capacity=capacity,
                              service_headway_s=headway)
            costs = tuple(cost(vehicles, replace(settings, amber_service_s=amber, left_first=lead))
                          for amber, lead in product((0, 3), (False, True)))
            before, after = costs[1] - costs[0], costs[3] - costs[2]
            category = classification(before, after)
            counts[category] += 1
            by_window[window][category] += 1
            by_pattern[pattern][category] += 1
            by_headway[headway][category] += 1
            rows.append((window, arrival, pattern, capacity, headway, *costs, before, after, category))
    return {"total": dict(counts), "by_window": by_window, "by_pattern": by_pattern,
            "by_headway": by_headway, "columns": COLUMNS, "rows": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    report = experiment()
    rows = report.pop("rows")
    header = json.dumps(report, indent=2)[:-2]
    payload = ",\n".join("    " + json.dumps(row) for row in rows)
    args.output.write_text(header + ',\n  "rows": [\n' + payload + "\n  ]\n}\n",
                           encoding="utf-8")
