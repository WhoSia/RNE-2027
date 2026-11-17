"""Footprint screen for the five previously selected 12:30 UTC intervals."""
import argparse
import csv
from datetime import datetime, timezone
import json
from math import cos, hypot, radians, sin
from pathlib import Path

from dlr_path_screen import EXPECTED_MAP, ORIGIN, masks, sha
from dlr_timeline_review import CASES

CLOCK = datetime(2023, 9, 24, 12, 30, tzinfo=timezone.utc)


def vehicle_cells(x, y, yaw_deg, length, width, cells):
    angle = radians(yaw_deg)
    c, s = cos(angle), sin(angle)
    radius = hypot(length, width) / 2
    for px, py in cells:
        dx, dy = px-x, py-y
        if abs(dx) <= radius and abs(dy) <= radius:
            if abs(c*dx+s*dy) <= length/2 and abs(-s*dx+c*dy) <= width/2:
                yield px, py


def screen(map_path, trajectory, audit, signal):
    if sha(map_path) != EXPECTED_MAP:
        raise ValueError("Unrecognized K047 map")
    old = next(b for b in json.loads(audit.read_text()) if b["block"] == "1230")
    signal_sha = sha(signal)
    if old["hashes"]["day/day1230_signals.csv"] != signal_sha:
        raise ValueError("Signal file does not reproduce the archived time reference")
    starts = {c["interval"]: c["on_bracket_s"][1] for c in old["cycles"] if c["interval"] in CASES.values()}
    spacing = .25
    regions = masks(map_path, spacing)
    overlap = [((i+.5)*spacing,(j+.5)*spacing) for i,j in regions["east_left_through_overlap"]]
    rows = {k: [] for k in starts}
    with trajectory.open(newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            if row["interpolated"].strip().lower() != "false":
                continue
            actual = (datetime.fromisoformat(row["timestamp"]) - CLOCK).total_seconds()
            case = next((k for k, t in starts.items() if t-2 <= actual <= t+6), None)
            if case is None:
                continue
            if sum(float(row[f"classifications_{kind}"]) for kind in ("car", "truck", "van")) < .5:
                continue
            x = float(row["center_easting"])-ORIGIN[0]
            y = float(row["center_northing"])-ORIGIN[1]
            footprint = set(vehicle_cells(x,y,float(row["yaw"]),float(row["dimension_length"]),
                                          float(row["dimension_width"]), overlap))
            if footprint:
                rows[case].append((actual, row["id"], float(row["velocity_magnitude"])))
    return {"signal_sha256": signal_sha, "track_sha256": sha(trajectory),
            "spatial_cell_m": spacing, "window_s": [-2,6],
            "cases": {k: {"footprint_samples": len(events), "distinct_track_ids": len({i for _,i,_ in events}),
                          "slow_footprint_samples_2ms": sum(v <= 2 for _,_,v in events),
                          "first_and_last_s": [round(f(t for t,_,_ in events)-starts[k],3)
                                               for f in (min,max)] if events else None}
                      for k,events in rows.items()}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for name in ("map", "trajectory", "audit", "signal", "output"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    report = screen(args.map, args.trajectory, args.audit, args.signal)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
