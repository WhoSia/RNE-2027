"""Observed discharge and queue exposure within bracketed DLR greens."""
import argparse
from collections import defaultdict
import csv
from hashlib import sha256
import json
from math import ceil, floor
from pathlib import Path

from field_replay import EVAL, TRAIN, load


def audit(root, block):
    hour, minute = int(block[:2]), int(block[2:])
    start = (hour - 12)*3600 + minute*60
    base = root / "week1" / "wide" / block
    queue_path = base / "daylight_queues_1ms.csv"
    queue_rows = defaultdict(dict)
    with queue_path.open(newline="") as stream:
        for row in csv.DictReader(stream):
            tick = int(row["tick"]) - start*2
            lane = int(row["lane"])
            queue_rows[tick][lane] = int(row["count"])
    stops = []
    with (base / "daylight_crossings.csv").open(newline="") as stream:
        for row in csv.DictReader(stream):
            stops.append((float(row["stop"])-start, row["movement"] or "unclassified"))
    _, intervals, gaps, _, hashes = load(root,block)
    hashes[str(queue_path.relative_to(root))] = sha256(queue_path.read_bytes()).hexdigest()
    rows = []
    for index, ((a0,a1,b0,b1),gap) in enumerate(zip(intervals,gaps),1):
        exposure = 0
        through_queue = left_queue = cooccurrence = 0
        for tick in range(ceil(2*a1),floor(2*b0)+1):
            lanes = queue_rows.get(tick,{})
            has_through = any(lanes.get(m,0) for m in (-3,-4))
            has_left = any(lanes.get(m,0) for m in (-1,-2))
            exposure += 1
            through_queue += has_through
            left_queue += has_left
            cooccurrence += has_through and has_left
        certain = sum(a1 <= t <= b0 and m=="through" for t,m in stops)
        possible = sum(a0 <= t <= b1 and m in ("through","unclassified") for t,m in stops)
        assert certain <= possible and cooccurrence <= min(through_queue,left_queue)
        rows.append({"interval":index,"on_bracket_s":[a0,a1],"off_bracket_s":[b0,b1],
                     "max_sample_gap_s":gap,"previous_1_2_rule":gap<=1.2,
                     "discharge_classification_bounds":[certain,possible],
                     "half_second_slots":exposure,"through_queue_detections":through_queue,
                     "left_queue_detections":left_queue,"simultaneous_queue_detections":cooccurrence})
    return {"block":block,"hashes":hashes,"cycles":rows}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("dlr_root",type=Path)
    p.add_argument("output",type=Path)
    a = p.parse_args()
    a.output.write_text(json.dumps([audit(a.dlr_root,b) for b in TRAIN+EVAL],indent=2)+"\n")
