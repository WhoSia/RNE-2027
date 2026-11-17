"""Screen DLR green termination using camera-derived queue presence.

This is not loop detector occupancy. An empty slot is no detection in the
derived table. The red window starts at the first explicitly red sample.
"""
import argparse
import csv
import json
from datetime import datetime
from math import ceil, floor
from pathlib import Path

from dlr_green_audit import audit
from field_replay import EVAL, ORIGIN, TRAIN


def screen(root, block):
    start = (int(block[:2])-12)*3600 + int(block[2:])*60
    with (root/"day"/f"day{block}_signals.csv").open(newline="") as stream:
        signals = [(datetime.fromisoformat(r["timestamp"])-ORIGIN).total_seconds()-start
                   for r in csv.DictReader(stream) if r["id"]=="3" and r["state"]=="3"]
    path = root/"week1"/"wide"/block/"daylight_queues_1ms.csv"
    with path.open(newline="") as stream:
        q = {int(r["tick"])-2*start for r in csv.DictReader(stream)
             if int(r["lane"]) in (-3,-4) and int(r["count"]) > 0}
    source = audit(root,block)
    result = []
    skipped = []
    for green in source["cycles"]:
        a0,a1 = green["on_bracket_s"]
        b0,b1 = green["off_bracket_s"]
        r0 = min((t for t in signals if b0 <= t < b1+6),default=None)
        if r0 is None:
            skipped.append({"interval":green["interval"],"reason":"no red sample near green end"})
            continue
        green_slots = range(max(ceil(2*a1),floor(2*b0)-9),floor(2*b0)+1)
        red_slots = range(ceil(2*r0),ceil(2*r0)+10)
        if red_slots[-1] >= 1800:
            skipped.append({"interval":green["interval"],"reason":"red window crosses block end"})
            continue
        g = sum(t in q for t in green_slots)
        r = sum(t in q for t in red_slots)
        result.append({"interval":green["interval"],"green_tail_detected":g,
                       "green_tail_slots":len(green_slots),"early_red_detected":r,
                       "early_red_slots":10,"red_first_s":r0,
                       "old_gap_rule":green["previous_1_2_rule"],
                       "classified_green_departures":green["discharge_classification_bounds"][0]})
    return {"block":block,"input_sha256":source["hashes"],"skipped":skipped,"rows":result}


if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("root",type=Path)
    p.add_argument("out",type=Path)
    a=p.parse_args()
    a.out.write_text(json.dumps([screen(a.root,b) for b in TRAIN+EVAL],indent=2)+"\n")
