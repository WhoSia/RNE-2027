"""Count distinct observed vehicle IDs across the full P37 nighttime block."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from p37_night_routes import (BLOCK_START, CELL_M, EXPECTED_MAP, TRACK_SHA, raster,
                              read_block, route_masks, strip, time_s, verify_bytes)


def coverage(map_path, tracks):
    verify_bytes(map_path, EXPECTED_MAP)
    verify_bytes(tracks, TRACK_SHA)
    roads = ET.parse(map_path)
    _, gate = route_masks(map_path)
    regions = {}
    for road_id in ("101000", "279000"):
        road = roads.find(f"road[@id='{road_id}']")
        length = float(road.attrib["length"])
        for lo, hi in ((0, 8), (8, 20), (20, 30), (30, 40), (40, 50), (length-5, length)):
            name = f"{road_id}/{lo:.1f}-{hi:.1f}"
            regions[name] = set().union(*(raster(strip(road, lane, lo, hi, CELL_M), CELL_M)
                                          for lane in (-1, -2)))
    ids = defaultdict(set)

    def record(vehicle, stamp, zones):
        if len(zones) == 1:
            ids[next(iter(zones))].add(vehicle)

    read_block(tracks, regions, gate, time_s(BLOCK_START), on_detection=record)
    return {zone: len(ids[zone]) for zone in regions}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("map", type=Path)
    parser.add_argument("tracks", type=Path)
    args = parser.parse_args()
    print(json.dumps(coverage(args.map, args.tracks), indent=2))
