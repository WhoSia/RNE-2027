"""Join east stopped queue observations, stopline events and west outlet tracks."""
import argparse
import csv
from hashlib import file_digest
import json
from math import ceil, floor
from pathlib import Path

import pandas as pd

from dlr_green_audit import audit
from field_replay import EVAL, ORIGIN, TRAIN

CONFIG = Path(__file__).with_name("dlr_west_outlet.json")


def digest(path):
    with path.open("rb") as stream:
        return file_digest(stream,"sha256").hexdigest()


def outlet(path, cfg):
    cols = ["timestamp","id","center_easting","center_northing","velocity_magnitude",
            "interpolated","classifications_car","classifications_van","classifications_truck"]
    f = pd.read_csv(path,usecols=cols)
    x,y,ux,uy,lanes = cfg["gate"]
    dx = f.center_easting-cfg["utm_origin"][0]-x
    dy = f.center_northing-cfg["utm_origin"][1]-y
    longitudinal = dx*ux+dy*uy
    lateral = -dx*uy+dy*ux
    on_road = pd.Series(False,index=f.index)
    for a,b in lanes:
        on_road |= lateral.between(a,b,inclusive="left")
    mask = on_road & ~f.interpolated & longitudinal.between(-6,8,inclusive="left")
    probability = f[cols[-3:]].sum(axis=1)
    f = f[mask & (probability>=.5)].copy()
    f["distance"] = longitudinal.loc[f.index]
    f["time"] = (pd.to_datetime(f.timestamp,utc=True,format="mixed")-pd.Timestamp(ORIGIN)).dt.total_seconds()
    f["tick"] = (f.time*2).round().astype(int)
    f["error"] = (f.time-f.tick/2).abs()
    f = f[f.error<=.026]
    return f.loc[f.groupby(["tick","id"]).error.idxmin()]


def count_events(events, t, end):
    return sum(t <= event < min(t+2,end) for event in events)


def block_rows(root, block, cfg):
    offset = (int(block[:2])-12)*3600+int(block[2:])*60
    base = root/"week1"/"wide"/block
    raw = root/"day"/f"day{block}_tracks.csv"
    west = outlet(raw,cfg)
    queue = {}
    with (base/"daylight_queues_1ms.csv").open(newline="") as stream:
        for r in csv.DictReader(stream):
            queue.setdefault(int(r["tick"]),{})[int(r["lane"])] = int(r["count"])
    with (base/"daylight_crossings.csv").open(newline="") as stream:
        crossings = list(csv.DictReader(stream))
    through = [float(r["stop"]) for r in crossings if r["movement"]=="through"]
    unknown = through+[float(r["stop"]) for r in crossings if not r["movement"]]
    audited = audit(root,block)
    rows = []
    masks = {}
    controls = {}
    for low,high in cfg["windows_m"]:
        window = west[west.distance.between(low,high,inclusive="left")]
        controls[f"{low}:{high}"] = {"vehicle_ticks":len(window),"distinct_tracks":int(window.id.nunique()),
                                   "sampled_ticks":int(window.tick.nunique()),
                                   "slow_ticks_2ms":int(window.loc[window.velocity_magnitude<=2,"tick"].nunique())}
        masks[f"{low}:{high}@any"] = set(window.tick)
        for v in (.5,1,2):
            masks[f"{low}:{high}@{v}"] = set(west.loc[west.distance.between(
                low,high,inclusive="left") & (west.velocity_magnitude<=v),"tick"])
    for g in audited["cycles"]:
        a = g["on_bracket_s"][1]+offset
        b = g["off_bracket_s"][0]+offset
        for tick in range(ceil(2*a),floor(2*b)-3):
            lanes = queue.get(tick,{})
            if not any(lanes.get(i,0) for i in (-3,-4)):
                continue
            rows.append({"interval":g["interval"],"from_first_green_s":round(tick/2-a,3),
                         "through_2s":count_events(through,tick/2,b),
                         "through_or_unknown_2s":count_events(unknown,tick/2,b),
                         "left_lane_queue":any(lanes.get(i,0) for i in (-1,-2)),
                         "west_slow":{key:tick in ticks for key,ticks in masks.items()}})
    return {"block":block,"input_sha256":audited["hashes"]|{str(raw.relative_to(root)):digest(raw)},
            "outlet_positive_controls":controls,"rows":rows}


def main(root):
    cfg=json.loads(CONFIG.read_text())
    if digest(root/"map.xodr") != cfg["map_sha256"]:
        raise ValueError("OpenDRIVE map differs from the pinned geometry")
    return {"config_sha256":digest(CONFIG),"blocks":[block_rows(root,b,cfg) for b in TRAIN+EVAL]}


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("root",type=Path)
    p.add_argument("output",type=Path)
    a=p.parse_args()
    a.output.write_text(json.dumps(main(a.root),indent=2)+"\n")
