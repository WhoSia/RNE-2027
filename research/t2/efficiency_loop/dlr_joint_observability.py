"""Audit simultaneous detections and stop-reference crossings in open K047 blocks."""
import argparse
from collections import Counter, defaultdict
import csv
from dataclasses import dataclass
from datetime import timedelta
from itertools import groupby, pairwise
import json
from math import cos, floor, sin
from pathlib import Path
import xml.etree.ElementTree as ET

from dlr_followers import CELL_M, TICKS_PER_S, green_clock
from dlr_path_cases import CLOCK
from dlr_path_geometry import bounds, pose, strip
from dlr_path_screen import EXPECTED_MAP, ORIGIN, raster, sha
from dlr_review_replay import STOP_S, time_s

BLOCKS = ("120000", "123000", "130000")
BLOCK_SECONDS = 900
SLOT_SECONDS = .5
FRAME_TOLERANCE_S = .026
MAX_GATE_GAP_S = .1
ZONES = {
    "near_stop": ("100000", (-3, -4), 135, 155),
    "taper_through": ("100000", (-3,), 80, 105),
    "taper_left_bay": ("100000", (-1, -2), 80, 105),
    "connector_entry": ("300016", (-1, -2), 0, 8),
    "receiver_entry": ("101000", (-1, -2), 0, 8),
}
OUTPUT_KEYS = (
    "selected_frames", "near_stop_slow", "taper_both_detected",
    "receiver_slow", "connector_slow", "connector_and_receiver_slow",
    "near_stop_and_receiver_slow", "all_zone_presence",
    "crossing_candidate_in_slot", "all_zone_presence_and_crossing",
)


@dataclass(frozen=True)
class Gate:
    x: float
    y: float
    ux: float
    uy: float
    lanes: tuple

    def project(self, x, y):
        dx, dy = x - self.x, y - self.y
        return dx*self.ux + dy*self.uy, -dx*self.uy + dy*self.ux


def load_geometry(map_path):
    if sha(map_path) != EXPECTED_MAP:
        raise ValueError("Unrecognized K047 map")
    root = ET.parse(map_path)
    roads = {road.get("id"): road for road in root.findall("./road")}
    regions = {name: set().union(*(raster(strip(roads[road], lane, a, b, CELL_M), CELL_M)
                                 for lane in lanes))
               for name, (road, lanes, a, b) in ZONES.items()}
    # A raster cell shared by the two taper masks cannot provide positive
    # evidence of distinct adjacent lane occupancy.
    overlap = regions["taper_through"] & regions["taper_left_bay"]
    for name in ("taper_through", "taper_left_bay"):
        regions[name].difference_update(overlap)
    approach = roads["100000"]
    x, y, heading = pose(approach, STOP_S)
    axis = Gate(x, y, cos(heading), sin(heading), ())
    lanes = tuple(sorted(axis.project(px, py)[1] for px, py in bounds(approach, lane, STOP_S))
                  for lane in (-3, -4))
    return regions, Gate(x, y, axis.ux, axis.uy, lanes)


def gate_crossing(seq, lanes, start):
    """Return first positive same-track bracket and its containing slot."""
    for (t0, a, l0), (t1, b, l1) in pairwise(seq):
        if not (0 < round(t1-t0, 6) <= MAX_GATE_GAP_S and a <= 0 < b):
            continue
        lateral = l0 - a/(b-a)*(l1-l0)
        if sum(lo < lateral < hi for lo, hi in lanes) != 1:
            continue
        k = floor((t0-start)/SLOT_SECONDS)
        return k if k == floor((t1-start)/SLOT_SECONDS) else None, (t0, t1)
    return None


def frame_slot(stamp, start):
    k = round((stamp-start)/SLOT_SECONDS)
    error = abs(stamp-start-k*SLOT_SECONDS)
    if 0 <= k < int(BLOCK_SECONDS/SLOT_SECONDS) and error <= FRAME_TOLERANCE_S:
        return k, error
    return None


def read_block(track, regions, gate, start):
    frames = {}
    gate_tracks = defaultdict(list)
    last_stamp = -float("inf")
    with track.open(newline="", encoding="utf-8-sig") as stream:
        for t, rows in groupby(csv.DictReader(stream), key=lambda row: row["timestamp"]):
            stamp = time_s(t)
            if stamp <= last_stamp:
                raise ValueError("Trajectory timestamps must be strictly ordered by frame")
            last_stamp = stamp
            if not start <= stamp < start+BLOCK_SECONDS:
                continue
            slot = frame_slot(stamp, start)
            present, slow = set(), set()
            observed = False
            for row in rows:
                if row["interpolated"].strip().lower() != "false":
                    continue
                observed = True
                if sum(float(row["classifications_"+k]) for k in ("car", "van", "truck")) < .5:
                    continue
                x = float(row["center_easting"])-ORIGIN[0]
                y = float(row["center_northing"])-ORIGIN[1]
                along, across = gate.project(x,y)
                if abs(along) <= 8 and abs(across) < 22:
                    gate_tracks[row["id"]].append((stamp,along,across))
                if slot is None:
                    continue
                cell = (floor(x/CELL_M), floor(y/CELL_M))
                zones = {name for name,cells in regions.items() if cell in cells}
                present.update(zones)
                if zones and float(row["velocity_magnitude"]) <= 2:
                    slow.update(zones)
            if slot is not None and observed:
                k, error = slot
                if k not in frames or error < frames[k][0]:
                    frames[k] = error, stamp, present, slow
    return frames, gate_tracks


def features(present, slow, crossings):
    return {
        "selected_frames": True,
        "near_stop_slow": "near_stop" in slow,
        "taper_both_detected": {"taper_through", "taper_left_bay"} <= present,
        "receiver_slow": "receiver_entry" in slow,
        "connector_slow": "connector_entry" in slow,
        "connector_and_receiver_slow": {"connector_entry", "receiver_entry"} <= slow,
        "near_stop_and_receiver_slow": {"near_stop", "receiver_entry"} <= slow,
        "all_zone_presence": ZONES.keys() <= present,
        "crossing_candidate_in_slot": bool(crossings),
        "all_zone_presence_and_crossing": ZONES.keys() <= present and bool(crossings),
    }


def audit_block(track, signal, regions, gate, start):
    frames, gate_tracks = read_block(track, regions, gate, start)
    events = Counter()
    boundary = 0
    duplicate_stamps = 0
    for seq in gate_tracks.values():
        if any(a[0] == b[0] for a, b in pairwise(seq)):
            duplicate_stamps += 1
            continue
        candidate = gate_crossing(seq, gate.lanes, start)
        if candidate is None:
            continue
        k, _ = candidate
        if k is None:
            boundary += 1
        else:
            events[k] += 1
    clocks = [green_clock(signal, head) for head in (3,4)]
    table = Counter()
    totals = Counter(dict.fromkeys(OUTPUT_KEYS, 0))
    green = totals.copy()
    witnesses = {}
    for k, (_, stamp, present, slow) in sorted(frames.items()):
        h3,h4 = (clock(round(stamp*TICKS_PER_S)) for clock in clocks)
        table[h3+"/"+h4] += 1
        f = features(present, slow, events[k])
        totals.update(f)
        if h3 == "green":
            green.update(f)
            for label in ("near_stop_and_receiver_slow", "connector_and_receiver_slow",
                          "all_zone_presence", "all_zone_presence_and_crossing"):
                if f[label] and label not in witnesses:
                    witnesses[label] = {
                        "frame_utc": (CLOCK+timedelta(seconds=stamp)).isoformat(),
                        "head_4": h4, "crossings_in_slot": events[k],
                        "positive_zones": sorted(present), "slow_zones": sorted(slow),
                    }
    return {
        "track_sha256": sha(track), "signal_sha256": sha(signal),
        "expected_halfsecond_slots": int(BLOCK_SECONDS/SLOT_SECONDS),
        "all_selected_frames": dict(totals), "head_3_bracketed_green": dict(green),
        "head_3_4_joint": dict(table), "first_green_witnesses": witnesses,
        "crossing_candidates": sum(events.values())+boundary,
        "crossing_straddled_slot": boundary,
        "crossing_without_retained_frame": sum(n for k,n in events.items() if k not in frames),
        "tracks_excluded_for_duplicate_gate_timestamp": duplicate_stamps,
    }


def report(root):
    map_path = root/"map.xodr"
    regions, gate = load_geometry(map_path)
    blocks = {}
    for start_clock in BLOCKS:
        start_t = CLOCK.replace(hour=int(start_clock[:2]), minute=int(start_clock[2:4]))
        stem = f"{start_t:%y%m%d-%H%M%S}_{start_t+timedelta(seconds=BLOCK_SECONDS):%y%m%d-%H%M%S}"
        blocks[start_clock] = audit_block(root/f"trajectories_{stem}.csv",
                                          root/f"traffic-lights_{stem}.csv",
                                          regions, gate, (start_t-CLOCK).total_seconds())
    return {"map_sha256": EXPECTED_MAP, "date": "2023-09-24", "windows_utc": list(BLOCKS),
            "field_permissions": "Approach heads only; lane-control mapping and sensor coverage unresolved",
            "blocks": blocks}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(report(args.data), sort_keys=True, indent=2)+"\n",
                           encoding="utf-8")
