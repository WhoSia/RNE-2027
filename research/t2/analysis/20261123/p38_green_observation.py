"""Screen nighttime green windows for simultaneous positive queue proxies."""
from collections import Counter
from pathlib import Path
import argparse
import json
from math import floor

from dlr_joint_observability import SLOT_SECONDS, gate_crossing, load_geometry, read_block
from dlr_route_evidence import bracket_code
from dlr_review_replay import time_s
from p35_observation_timing import read_signals, verify_bytes
from p37_night_routes import BLOCK_START, TRACK_SHA


def screen(map_path, trajectories, signals):
    verify_bytes(trajectories, TRACK_SHA)
    heads, _, _ = read_signals(signals)
    times, codes = zip(*[(time_s(t.isoformat()), code) for t, code in heads[3]])
    start = time_s(BLOCK_START)
    regions, gate = load_geometry(map_path)
    frames, tracks = read_block(trajectories, regions, gate, start)
    crossing_slots = set()
    ambiguous_slots = set()
    for samples in tracks.values():
        event = gate_crossing(samples, gate.lanes, start)
        if event is None:
            continue
        slot, (lower, upper) = event
        if slot is None:
            ambiguous_slots.update(floor((t-start)/SLOT_SECONDS) for t in (lower, upper))
        else:
            crossing_slots.add(slot)

    counts = Counter()
    for slot in range(1800):
        lower = start + slot * SLOT_SECONDS
        if bracket_code((times, codes), lower, lower + SLOT_SECONDS) != "5":
            continue
        counts["green_bracket_slots"] += 1
        if slot in crossing_slots:
            counts["detected_crossing"] += 1
            continue
        if slot in ambiguous_slots:
            counts["ambiguous_crossing_time"] += 1
            continue
        frame = frames.get(slot)
        if frame is None:
            counts["no_selected_frame"] += 1
            continue
        counts["frame_without_detected_crossing"] += 1
        _, _, _, slow = frame
        upstream = "near_stop" in slow
        receiver = "receiver_wider" in slow
        counts[f"slow_upstream_{int(upstream)}_receiver_{int(receiver)}"] += 1
    return dict(counts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("map", "trajectories", "signals"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    print(json.dumps(screen(args.map, args.trajectories, args.signals), indent=2, sort_keys=True))
