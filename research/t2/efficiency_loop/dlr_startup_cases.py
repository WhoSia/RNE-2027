"""Trace the initially queued vehicles in the longest screening candidates."""
import argparse
import csv
import json
from pathlib import Path

import pandas as pd

from dlr_green_audit import audit
from dlr_queue_identity import THROUGH_LANES, queue_ids


def investigate(root, candidates, *, fixed_start=False):
    result = []
    for row in candidates:
        block, idx = row["block"], row["interval"]
        offset = (int(block[:2])-12)*3600+int(block[2:])*60
        g = audit(root,block)["cycles"][idx-1]
        a0,a1 = (v+offset for v in g["on_bracket_s"])
        path = root/"week1"/"wide"/block
        frame = pd.read_pickle(path/"east_tracks_working.pkl")
        frame = frame[~frame.interpolated & frame.time.between(a0-1,a1+8)].copy()
        frame["tick"]=(2*frame.time).round().astype(int)
        frame["error"]=(frame.time-frame.tick/2).abs()
        sample=frame[frame.error<=.026]
        sample=sample.loc[sample.groupby(["id","tick"]).error.idxmin()]
        queues=queue_ids(sample[sample.lane.isin(THROUGH_LANES)],1,8)
        if fixed_start:
            from math import ceil
            first_tick = ceil(2*a1)
            members = {ids[0]:lane for (t,lane),ids in queues.items() if t==first_tick}
        else:
            members={v:lane for (t,lane),ids in queues.items() if a1<=t/2<a1+2.5 for v in ids}
        with (path/"daylight_crossings.csv").open(newline="") as f:
            stops={int(r["id"]):r for r in csv.DictReader(f)}
        tracks=[]
        for v,lane in sorted(members.items()):
            t=frame[(frame.id==v) & (frame.time>=a1)].sort_values("time")
            moving=t[t.velocity_magnitude>2]
            crossing=stops.get(v)
            tracks.append({"lane":lane,"last_sample_s":round(t.time.max()-a1,3),
                           "first_sample_over_2ms_s":round(moving.time.iloc[0]-a1,3) if len(moving) else None,
                           "motion_to_crossing_s":round(float(crossing["stop"])-moving.time.iloc[0],3)
                           if crossing and len(moving) and float(crossing["stop"])>=moving.time.iloc[0] else None,
                           "stop_crossing_s":round(float(crossing["stop"])-a1,3) if crossing else None,
                           "movement":crossing["movement"] if crossing and crossing["movement"] else "unclassified"})
        if not fixed_start:
            for item in tracks:
                item.pop("motion_to_crossing_s")
        result.append({"block":block,"interval":idx,"onset_uncertainty_s":round(a1-a0,3),"tracks":tracks})
    return result


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("root",type=Path)
    p.add_argument("summary",type=Path)
    p.add_argument("output",type=Path)
    p.add_argument("--paired",action="store_true")
    a=p.parse_args()
    rows=json.loads(a.summary.read_text())
    if a.paired:
        a.output.write_text(json.dumps(investigate(a.root,[r for r in rows["pairs"]
                             if r["block"]=="1230"],fixed_start=True),indent=2)+"\n")
        raise SystemExit(0)
    longest=max(r["longest_no_through_or_unknown_run_slots"] for r in rows)
    a.output.write_text(json.dumps(investigate(a.root,[r for r in rows
                      if r["longest_no_through_or_unknown_run_slots"]==longest]),indent=2)+"\n")
