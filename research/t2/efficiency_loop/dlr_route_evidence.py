"""Check same-ID paths and raw signal codes around mapped K047 crossings."""
import argparse
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict
import csv
from datetime import timedelta
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from dlr_followers import CELL_M, TICKS_PER_S, green_clock
from dlr_joint_observability import BLOCKS, BLOCK_SECONDS, gate_crossing, load_geometry, read_block
from dlr_path_cases import CLOCK
from dlr_path_geometry import bounds, strip
from dlr_path_screen import EXPECTED_MAP, raster, sha
from dlr_review_replay import STOP_S, time_s

BANDS = ("0–8", "8–24", "24–40", "40–52", "52–end")
BOUNDARIES = (0, 8, 24, 40, 52)
WEST = "west_receiver"
SOUTH = "south_receiver"
ROUTE_SECONDS = 20
DOCUMENT_MD5 = "fa7f80c57c85d58c02ac71a3c100e102"


def regions_and_gates(map_path):
    masks, gate = load_geometry(map_path)
    roads = {road.attrib["id"]: road for road in ET.parse(map_path).getroot().findall("road")}
    connector = roads["300016"]
    endpoints = (*BOUNDARIES, float(connector.attrib["length"]))
    regions = {
        name: set().union(*(raster(strip(connector, lane, low, high, CELL_M), CELL_M)
                            for lane in (-1, -2)))
        for name, low, high in zip(BANDS, endpoints[:-1], endpoints[1:], strict=True)
    }
    regions[WEST] = masks["receiver_entry"]
    regions[SOUTH] = set().union(*(raster(strip(roads["279000"], lane, 5, 20, CELL_M), CELL_M)
                                   for lane in (-1, -2)))
    shared = {cell for cell, count in Counter(
        cell for name in (*BANDS, WEST) for cell in regions[name]
    ).items() if count > 1}
    for name in (*BANDS, WEST):
        regions[name].difference_update(shared)
    left = tuple(sorted(gate.project(x, y)[1] for x, y in bounds(roads["100000"], -2, STOP_S)))
    return regions, gate, (left,)


def read_signals(path):
    clocks = defaultdict(list)
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            group = int(row["id"])
            if group in (3, 4):
                clocks[group].append((time_s(row["timestamp"]), int(row["state"])))
    for group in (3, 4):
        samples = sorted(clocks[group])
        times, codes = zip(*samples, strict=True)
        if len(set(times)) != len(times):
            raise ValueError(f"Duplicate signal timestamps in group {group}")
        clocks[group] = times, codes
    return clocks


def bracket_code(clock, lo, hi, max_gap=1.25):
    times, codes = clock
    before = bisect_right(times, lo) - 1
    after = bisect_left(times, hi)
    if before < 0 or after == len(times) or after != before + 1:
        return "missing_or_transition"
    if times[after] - times[before] > max_gap or codes[before] != codes[after]:
        return "missing_or_transition"
    return str(codes[before])


def has_sequence(hits, names, lo, hi):
    """Each subsequent band needs its own strictly later positive sample."""
    for name in names:
        samples = hits.get(name, ())
        index = bisect_right(samples, lo)
        if index == len(samples) or samples[index] > hi:
            return False
        lo = samples[index]
    return True


def movement_report(gate_tracks, hits, lanes, start, clocks, head, route, exit_name):
    tally = Counter()
    mapped_codes = Counter()
    other_codes = Counter()
    exit_codes = Counter()
    for track, samples in gate_tracks.items():
        if any(a[0] == b[0] for a, b in zip(samples, samples[1:])):
            continue
        crossing = gate_crossing(samples, lanes, start)
        if crossing is None:
            continue
        _, (lo, hi) = crossing
        tally["lane_gate_candidates"] += 1
        mapped = bracket_code(clocks[head], lo, hi)
        mapped_codes[mapped] += 1
        other_codes[bracket_code(clocks[7-head], lo, hi)] += 1
        track_hits = hits.get(track, {})
        deadline = hi + ROUTE_SECONDS
        for name in (*route, exit_name):
            tally[f"hit_{name}"] += has_sequence(track_hits, (name,), lo, deadline)
        if has_sequence(track_hits, (exit_name,), lo, deadline):
            exit_codes[mapped] += 1
        if route:
            tally["ordered_connector"] += has_sequence(track_hits, route, lo, deadline)
            tally["ordered_connector_and_receiver"] += has_sequence(
                track_hits, (*route, exit_name), lo, deadline
            )
    return {
        "counts": dict(tally),
        "mapped_group_codes": dict(mapped_codes),
        "other_group_codes": dict(other_codes),
        "exit_confirmed_mapped_codes": dict(exit_codes),
    }


def block_report(track, signal, regions, gate, left_lanes, start):
    hits = defaultdict(lambda: defaultdict(list))

    def on_detection(track_id, stamp, zones):
        for zone in zones:
            hits[track_id][zone].append(stamp)

    frames, gate_tracks = read_block(track, regions, gate, start, on_detection=on_detection)
    signal_clocks = read_signals(signal)
    group_3 = green_clock(signal)
    presence = {key: Counter() for key in ("all", "green_3")}
    slow = {key: Counter() for key in presence}
    for _, stamp, detected, low_speed in frames.values():
        exposures = ("all", "green_3") if group_3(round(stamp*TICKS_PER_S)) == "green" else ("all",)
        for key in exposures:
            presence[key].update(detected)
            slow[key].update(low_speed)
    return {
        "track_sha256": sha(track),
        "signal_sha256": sha(signal),
        "straight": movement_report(gate_tracks, hits, gate.lanes, start, signal_clocks, 3, BANDS, WEST),
        "left_lane_minus_2": movement_report(gate_tracks, hits, left_lanes, start, signal_clocks, 4, (), SOUTH),
        "straight_band_frames": {
            key: {band: {"center": presence[key][band], "slow_center": slow[key][band]}
                  for band in (*BANDS, WEST)}
            for key in presence
        },
    }


def report(root):
    regions, gate, left_lanes = regions_and_gates(root/"map.xodr")
    blocks = {}
    for name in BLOCKS:
        start = CLOCK.replace(hour=int(name[:2]), minute=int(name[2:4]))
        stamp = f"{start:%y%m%d-%H%M%S}_{start+timedelta(seconds=BLOCK_SECONDS):%y%m%d-%H%M%S}"
        blocks[name] = block_report(root/f"trajectories_{stamp}.csv", root/f"traffic-lights_{stamp}.csv",
                                    regions, gate, left_lanes, (start-CLOCK).total_seconds())
    return {"map_sha256": EXPECTED_MAP, "documentation_md5": DOCUMENT_MD5, "blocks": blocks}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(report(args.data), sort_keys=True, indent=2)+"\n",
                           encoding="utf-8")
