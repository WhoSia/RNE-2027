"""Measure downstream observation reach on the five frozen nighttime crossings."""
import argparse
from bisect import bisect_right
from collections import defaultdict
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from p37_night_routes import (BLOCK_START, CELL_M, EAST_GROUP_BY_LANE, EXPECTED_MAP,
                              ROUTES, TRACK_SHA, load_p34, raster, read_block,
                              route_masks, strip, time_s, verify_bytes)


def analyse(archive, map_path, track_path):
    verify_bytes(map_path, EXPECTED_MAP)
    verify_bytes(track_path, TRACK_SHA)
    regions, gate = route_masks(map_path)
    roads = ET.parse(map_path)
    paths = {}
    for group, road_id in ((3, "101000"), (4, "279000")):
        road = roads.find(f"road[@id='{road_id}']")
        end = float(road.attrib["length"])
        paths[group] = list(ROUTES[group])
        for label, lo, hi in (("mid", 30, 40), ("last5", end - 5, end)):
            name = f"{road_id}_{label}"
            regions[name] = set().union(*(raster(strip(road, lane, lo, hi, CELL_M), CELL_M)
                                          for lane in (-1, -2)))
            paths[group].append(name)
    hits = defaultdict(lambda: defaultdict(list))

    def record(vehicle, stamp, zones):
        if len(zones) == 1:
            hits[vehicle][next(iter(zones))].append(stamp)

    read_block(track_path, regions, gate, time_s(BLOCK_START), on_detection=record)
    rows = []
    for event in load_p34(archive)["crossings"]:
        if event["road_id"] != "100000" or event["source_arm"] != "East":
            continue
        group = EAST_GROUP_BY_LANE.get(event["map_lane_id"])
        if group is None:
            continue
        start = time_s(event["bracket_end_utc"])
        last = start
        observed = {}
        for zone in paths[group]:
            samples = hits[event["id"]][zone]
            index = bisect_right(samples, last)
            if index == len(samples) or samples[index] > start + 40:
                break
            last = samples[index]
            observed[zone] = round(last - start, 6)
        direct_hits = {}
        for zone in paths[group][-2:]:
            samples = hits[event["id"]][zone]
            i = bisect_right(samples, start)
            direct_hits[zone] = i < len(samples) and samples[i] <= start + 40
        rows.append(dict(direct_downstream_hits=direct_hits, id=event["id"], group=group, crossing_end=event["bracket_end_utc"],
                         seconds_after_crossing=observed))
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("archive", "map", "tracks"):
        parser.add_argument(arg, type=Path)
    args = parser.parse_args()
    print(json.dumps(analyse(args.archive, args.map, args.tracks), indent=2))
