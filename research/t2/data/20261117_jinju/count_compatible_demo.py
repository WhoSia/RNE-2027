"""Illustrate unobserved arrival orders compatible with one Jinju count pair."""
import argparse
import csv
import json
from collections import Counter
from dataclasses import replace
from datetime import datetime
from itertools import product
from pathlib import Path

from d51_phase_order import Params, Vehicle, simulate
from jinju_audit import vector


def select_record(path):
    with path.open(encoding="cp949", newline="") as stream:
        rows = list(csv.reader(stream))[1:]
    location_n = Counter(row[2] for row in rows)
    key_n = Counter(tuple(row[:3]) for row in rows)
    candidates = []
    for row in rows:
        start, end, site, lanes = row[:4]
        if key_n[tuple(row[:3])] != 1:
            continue
        a, b = map(datetime.fromisoformat, (start, end))
        if (b - a).total_seconds() != 14:
            continue
        for lane in range(1, int(lanes) + 1):
            moves, classes = row[2 + 2 * lane:4 + 2 * lane]
            if vector(moves, 6) == (1, 1, 0, 0, 0, 0) and sum(vector(classes, 7)) == 2:
                candidates.append((-location_n[site], start, lane, site, end))
    _, start, lane, site, end = min(candidates)
    return {"site": site, "start": start, "end": end, "lane": lane,
            "through_count": 1, "left_count": 1}


def counts_window(start):
    cases = []
    for t, left in product(range(start, start + 14), repeat=2):
        pair = ((t, "T"), (left, "L"))
        orders = (pair, pair[::-1]) if t == left else (tuple(sorted(pair)),)
        for order in orders:
            vehicles = tuple(Vehicle(tick, movement, i) for i, (tick, movement) in enumerate(order))
            config = Params(horizon_s=240, left_capacity=1, intergreen_s=5)
            outcomes = [simulate(vehicles, replace(config, left_first=lead)) for lead in (False, True)]
            if any(out.unserved for out in outcomes):
                raise RuntimeError("All vehicles must complete")
            lag, lead = [round(out.mean_vehicle_delay_s * len(vehicles)) for out in outcomes]
            cases.append((lead - lag, order, lag, lead))
    low, high = min(cases), max(cases)
    return {"sequences": len(cases), "lead_minus_lag_bounds_s": [low[0], high[0]],
            "low_witness": low, "high_witness": high,
            "minimax_regret_s": {"lag": max(0, -low[0]), "lead": max(0, high[0])}}


def experiment(path):
    return {"observed_record": select_record(path),
            "assumption": "matched hypothetical arrivals, no signal-clock join",
            "synthetic_window_start_s": {start: counts_window(start) for start in (0, 8, 26)}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(experiment(args.csv), ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
