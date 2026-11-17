"""Build a fixed-time, lane-ranked cohort at the first observed green."""
import argparse
import csv
import json
from math import ceil, floor
from pathlib import Path

import pandas as pd

from dlr_green_audit import audit
from dlr_green_service import digest
from dlr_queue_identity import STOP_M, THROUGH_LANES, queue_ids
from field_replay import EVAL, TRAIN


def block_cohort(root, block, *, before_green=False):
    base = root/"week1"/"wide"/block
    cache = base/"east_tracks_working.pkl"
    stops = base/"daylight_crossings.csv"
    offset = (int(block[:2])-12)*3600 + int(block[2:])*60
    source = audit(root,block)
    frame = pd.read_pickle(cache)
    frame = frame[~frame.interpolated & frame.lane.isin(THROUGH_LANES)].copy()
    frame["tick"] = (2*frame.time).round().astype(int)
    frame["error"] = (frame.time-frame.tick/2).abs()
    with stops.open(newline="") as stream:
        crossings = {}
        for row in csv.DictReader(stream):
            crossings.setdefault(int(row["id"]),[]).append(row)
    def snapshot(lo, hi):
        if before_green:
            # Allow the full track-to-grid tolerance before the last non-green sample.
            return floor(2 * (lo - .026))
        return ceil(2 * hi)

    ticks = {snapshot(*(t + offset for t in c["on_bracket_s"])) for c in source["cycles"]}
    sample = frame[(frame.error<=.026) & frame.tick.isin(ticks)]
    sample = sample.loc[sample.groupby(["id","tick"]).error.idxmin()]
    positions = sample.set_index(["tick","id"])
    queues = queue_ids(sample,1,8)
    rows = []
    coverage = []
    for cycle in source["cycles"]:
        lo,hi = [t+offset for t in cycle["on_bracket_s"]]
        end = cycle["off_bracket_s"][0]+offset
        tick = snapshot(lo, hi)
        for lane in THROUGH_LANES:
            members = queues.get((tick,lane),())
            coverage.append({"interval":cycle["interval"],"lane":lane,"queued":len(members)})
            for rank, vehicle in enumerate(members,1):
                start = hi if before_green else tick/2
                events = [c for c in crossings.get(vehicle,()) if start <= float(c["stop"]) <= end]
                event = events[0] if len(events)==1 else None
                p = positions.loc[tick,vehicle]
                rows.append({"interval":cycle["interval"],"lane":lane,"rank":rank,
                             "depth":len(members),"sample_offset_s":tick/2-hi,
                             "front_distance_m":round(STOP_M-p.s-p.dimension_length/2,3),
                             "movement":event["movement"] if event and event["movement"] else "unclassified",
                             "match_count":len(events),
                             "crossing_s_bounds":[float(event["stop"])-hi,float(event["stop"])-lo] if event else None})
    return {"block":block,"inputs":source["hashes"]|{str(cache.relative_to(root)):digest(cache)},
            "coverage":coverage,"rows":rows}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("root",type=Path)
    p.add_argument("output",type=Path)
    p.add_argument("--before-green", action="store_true")
    a=p.parse_args()
    a.output.write_text(json.dumps([block_cohort(a.root,b,before_green=a.before_green) for b in TRAIN+EVAL],indent=2)+"\n")


if __name__=="__main__":
    main()
