"""Find slow inner-through-lane tracks later seen on the east-left route."""
import argparse
from collections import defaultdict
import csv
from datetime import datetime
import json
from math import floor
from pathlib import Path

from dlr_path_cases import CLOCK
from dlr_path_geometry import pocket_screen_strips
from dlr_path_screen import EXPECTED_MAP, ORIGIN, masks, raster, sha


def scan(root_map, track):
    if sha(root_map) != EXPECTED_MAP:
        raise ValueError("Unrecognized K047 map")
    spacing = .25
    regions = masks(root_map, spacing)
    regions.update({k: set().union(*(raster(p, spacing) for p in v))
                    for k,v in pocket_screen_strips(root_map).items()})
    entries = defaultdict(lambda: defaultdict(list))
    control_places = ("inner_through_at_taper", "inner_through_at_stop")
    controls = {place: {"any": set(), "slow": set()} for place in control_places}
    with track.open(newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            if row["interpolated"].strip().lower() != "false":
                continue
            if sum(float(row[f"classifications_{kind}"]) for kind in ("car","truck","van")) < .5:
                continue
            cell = (floor((float(row["center_easting"])-ORIGIN[0])/spacing),
                    floor((float(row["center_northing"])-ORIGIN[1])/spacing))
            for key, levels in controls.items():
                if cell in regions[key]:
                    levels["any"].add(row["id"])
                    if float(row["velocity_magnitude"]) <= 2:
                        levels["slow"].add(row["id"])
            for key in ("inner_through_at_taper", "left_connector", "south_exit"):
                if cell not in regions[key]:
                    continue
                if key == "inner_through_at_taper" and float(row["velocity_magnitude"]) > 2:
                    continue
                stamp = (datetime.fromisoformat(row["timestamp"]) - CLOCK).total_seconds()
                entries[row["id"]][key].append(stamp)
    confirmed = []
    observed_approach = 0
    for zones in entries.values():
        approach = zones["inner_through_at_taper"]
        left = zones["left_connector"]
        south = zones["south_exit"]
        if not approach:
            continue
        observed_approach += 1
        first = min(approach)
        # Five track samples in each downstream corridor following the upstream event.
        # These are screening criteria, not manually verified movement/obstruction labels.
        confirmed_left = sorted(t for t in left if first < t <= first + 90)
        if len(confirmed_left) >= 5 and sum(confirmed_left[0] < t <= first+90 for t in south) >= 5:
            confirmed.append([round(first, 3), round(confirmed_left[0], 3)])
    return {"sha256": sha(track), "slow_tracks_in_scan_band": observed_approach,
            "later_east_left_candidates": sorted(confirmed),
            "track_detection_controls": {place: {speed: len(ids) for speed, ids in levels.items()}
                                         for place, levels in controls.items()}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("map", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("tracks", type=Path, nargs="+")
    args = parser.parse_args()
    report = {track.name: scan(args.map, track) for track in args.tracks}
    args.output.write_text(json.dumps(report, indent=2) + "\n")
