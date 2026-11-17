"""Separate mapped corridor overlap from detected vehicle centers."""
import argparse
from collections import defaultdict
import csv
from datetime import datetime
from hashlib import file_digest
import json
from math import ceil, floor
from pathlib import Path

from dlr_path_geometry import corridors

ORIGIN = (604763, 5792795)
EXPECTED_MAP = "256115a13cd29cb1d36cbbf110a4dbfa104ec2bdb680e3af1505a53f4ded30c4"


def sha(path):
    with path.open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def raster(polygon, spacing):
    rows = set()
    for j in range(floor(min(y for _, y in polygon)/spacing),
                   ceil(max(y for _, y in polygon)/spacing)):
        y = (j+.5)*spacing
        cuts = []
        for (ax, ay), (bx, by) in zip(polygon, polygon[1:]+polygon[:1]):
            if min(ay, by) <= y < max(ay, by):
                cuts.append(ax + (bx-ax)*(y-ay)/(by-ay))
        cuts.sort()
        for west, east in zip(cuts[::2], cuts[1::2], strict=True):
            rows.update((i, j) for i in range(ceil(west/spacing-.5), ceil(east/spacing-.5)))
    return rows


def masks(map_path, spacing, sample_step=.25):
    strips = corridors(map_path, sample_step)
    cells = {name: set().union(*(raster(p, spacing) for p in paths))
             for name, paths in strips.items()}
    cells["east_left_through_overlap"] = cells["left_connector"] & cells["through_connector"]
    return cells


def map_report(map_path):
    actual = sha(map_path)
    if actual != EXPECTED_MAP:
        raise ValueError("Unrecognized K047 map")
    return {"map_sha256": actual, "area_m2": {
        str(spacing): {key: round(len(mask)*spacing**2, 4) for key, mask in
                       masks(map_path, spacing, spacing).items()}
        for spacing in (.5, .25, .125, .0625)
    }}


def track_report(map_path, trajectory):
    if sha(map_path) != EXPECTED_MAP:
        raise ValueError("Unrecognized K047 map")
    spacing = .25
    regions = masks(map_path, spacing, spacing)
    present = defaultdict(set)
    slow = defaultdict(set)
    available_ticks = set()
    tracked = defaultdict(set)
    with trajectory.open(newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            if row["interpolated"].strip().lower() != "false":
                continue
            stamp = datetime.fromisoformat(row["timestamp"])
            second = stamp.replace(microsecond=0)
            available_ticks.add(second)
            if sum(float(row[f"classifications_{kind}"]) for kind in ("car", "truck", "van")) < .5:
                continue
            cell = (floor((float(row["center_easting"])-ORIGIN[0])/spacing),
                    floor((float(row["center_northing"])-ORIGIN[1])/spacing))
            for name, area in regions.items():
                if cell in area:
                    present[name].add(second)
                    tracked[name].add(row["id"])
                    if float(row["velocity_magnitude"]) <= 2:
                        slow[name].add(second)
    return {"trajectory_sha256": sha(trajectory),
            "seconds_with_any_noninterpolated_raw_row": len(available_ticks),
            "corridors": {name: {"seconds_with_center_detection": len(present[name]),
                                 "seconds_with_slow_center_detection": len(slow[name]),
                                 "distinct_ids_with_center_detection": len(tracked[name])}
                          for name in regions}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("map", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--tracks", type=Path, nargs="*", default=())
    args = parser.parse_args()
    result = map_report(args.map)
    result["track_screen"] = {track.name: track_report(args.map, track) for track in args.tracks}
    args.output.write_text(json.dumps(result, indent=2) + "\n")
