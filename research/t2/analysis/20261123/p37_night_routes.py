"""Check P36 movement hypotheses against direct nighttime trajectory samples."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from dlr_path_geometry import strip
from dlr_joint_observability import read_block
from dlr_path_screen import EXPECTED_MAP, raster
from dlr_route_evidence import BANDS, CELL_M, SOUTH, WEST, has_sequence, regions_and_gates
from dlr_review_replay import time_s
from p35_observation_timing import load_p34, verify_bytes
from p36_crosswalk_transfer import EAST_GROUP_BY_LANE

LEFT_CONNECTOR = "left_connector"
ROUTES = {3: (*BANDS, WEST), 4: (LEFT_CONNECTOR, SOUTH)}


def route_masks(map_path):
    regions, gate, _ = regions_and_gates(map_path)
    left = ET.parse(map_path).getroot().find("road[@id='300015']")
    length = float(left.attrib["length"])
    regions[LEFT_CONNECTOR] = set().union(*(
        raster(strip(left, lane, 0, length, CELL_M), CELL_M) for lane in (-1, -2)
    ))
    counts = Counter(cell for cells in regions.values() for cell in cells)
    for cells in regions.values():
        cells.difference_update(cell for cell, count in counts.items() if count > 1)
    return regions, gate


TRACK_SHA = "6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50"
WINDOWS = (10, 20, 40)
BLOCK_START = "2023-09-24T23:30:00+00:00"


def count_routes(candidates, detections):
    totals = {}
    for group, expected in ROUTES.items():
        events = [(event, key) for event, key in candidates if key == group]
        other = ROUTES[7 - group]
        windows = {}
        for seconds in WINDOWS:
            counts = Counter(dict.fromkeys(("expected_only", "alternative_only", "both", "neither"), 0))
            for event, _ in events:
                hits = detections.get(event["id"], {})
                start = time_s(event["bracket_end_utc"])
                stop = start + seconds
                found = has_sequence(hits, expected, start, stop)
                alternate = has_sequence(hits, other, start, stop)
                status = ("both" if alternate else "expected_only") if found else (
                    "alternative_only" if alternate else "neither"
                )
                counts[status] += 1
            windows[seconds] = dict(counts)
        totals[group] = {"candidates": len(events), "windows_seconds": windows}
    return totals


def analyse(archive, map_path, track_path):
    verify_bytes(map_path, EXPECTED_MAP)
    verify_bytes(track_path, TRACK_SHA)
    geometry = load_p34(archive)
    candidates = [
        (event, EAST_GROUP_BY_LANE[event["map_lane_id"]])
        for event in geometry["crossings"]
        if event["road_id"] == "100000" and event["source_arm"] == "East"
        and event["map_lane_id"] in EAST_GROUP_BY_LANE
    ]
    selected_ids = {event["id"] for event, _ in candidates}
    detections = defaultdict(lambda: defaultdict(list))

    def on_detection(track_id, stamp, zones):
        if track_id in selected_ids:
            for zone in zones:
                detections[track_id][zone].append(stamp)

    regions, gate = route_masks(map_path)
    read_block(track_path, regions, gate, time_s(BLOCK_START), on_detection=on_detection)
    return {
        "source_sha256": {"map": EXPECTED_MAP, "trajectories": TRACK_SHA},
        "groups": count_routes(candidates, detections),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ("p34_zip", "map", "trajectories"):
        parser.add_argument(argument, type=Path)
    args = parser.parse_args()
    print(json.dumps(analyse(args.p34_zip, args.map, args.trajectories), indent=2, sort_keys=True))
