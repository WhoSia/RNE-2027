"""Build blinded K047 review replays from hash-verified native CSV files."""
import argparse
from collections import defaultdict
import csv
from datetime import datetime, timedelta
import json
from math import cos, floor, radians
from pathlib import Path
import xml.etree.ElementTree as ET

from dlr_followers import CELL_M, TICKS_PER_S, approach_lookup
from dlr_path_cases import CLOCK
from dlr_path_geometry import bounds, corridors, pocket_screen_strips, strip
from dlr_path_screen import EXPECTED_MAP, ORIGIN, masks, raster, sha

FOLLOWUP_S = 90
STOP_S = 155.566906348012


def time_s(text):
    return (datetime.fromisoformat(text) - CLOCK).total_seconds()


def source_for(stamp, report):
    matches = []
    for name in report:
        first, last = name.removeprefix("trajectories_").removesuffix(".csv").split("_")
        date0, time0 = first.split("-")
        date1, time1 = last.split("-")
        start = datetime.strptime(date0+time0+"+0000", "%y%m%d%H%M%S%z")
        end = datetime.strptime(date1+time1+"+0000", "%y%m%d%H%M%S%z")
        if start <= stamp < end:
            matches.append((name, (end-CLOCK).total_seconds()))
    if len(matches) != 1:
        raise ValueError(f"No unique trajectory source for {stamp}")
    return matches[0]


def geometry(map_path):
    approach = ET.parse(map_path).find("./road[@id='100000']")
    polygons = corridors(map_path, .5)
    polygons.update(pocket_screen_strips(map_path, .5))
    polygons["approach"] = [strip(approach,lane,80,155.9,.5) for lane in (-1,-2,-3,-4)]
    stop = [point for lane in (-1,-2,-3,-4) for point in bounds(approach,lane,STOP_S)]
    all_points = [point for stripes in polygons.values() for stripe in stripes for point in stripe]
    xs, ys = zip(*all_points)
    return {"polygons":polygons,"stop":[stop[0],stop[-1]],
            "extent":[min(xs)-7,min(ys)-7,max(xs)+7,max(ys)+7]}


def read_tracks(path, clips, extent):
    out = defaultdict(list)
    xmin,ymin,xmax,ymax = extent
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            if row["interpolated"].strip().lower() != "false":
                continue
            x = float(row["center_easting"])-ORIGIN[0]
            y = float(row["center_northing"])-ORIGIN[1]
            if not (xmin <= x <= xmax and ymin <= y <= ymax):
                continue
            stamp = time_s(row["timestamp"])
            for case, (a,b) in clips.items():
                if a <= stamp <= b:
                    out[case].append((stamp,row["id"],x,y,float(row["yaw"]),
                                      float(row["dimension_length"]),float(row["dimension_width"]),
                                      float(row["velocity_magnitude"]),
                                      sum(float(row["classifications_"+k]) for k in
                                          ("car","van","truck")) >= .5))
    return out


def locate_pair(rows, case, lookup):
    tick = round(time_s(case["focus_start_utc"])*TICKS_PER_S)
    requested = (float(case["leader_s_m"]),float(case["follower_s_m"]))
    candidates = defaultdict(list)
    for stamp,ident,x,y,yaw,_,_,speed,motor in rows:
        if round(stamp*TICKS_PER_S) != tick or speed > 2 or not motor:
            continue
        label = lookup.get((floor(x/CELL_M),floor(y/CELL_M)))
        if label is None:
            continue
        lane,s,heading = label
        if lane == int(case["lane"]) and s in requested and cos(radians(yaw)-heading) >= cos(radians(35)):
            candidates[s].append(ident)
    found = [candidates[s] for s in requested]
    if any(len(ids) != 1 for ids in found) or found[0][0] == found[1][0]:
        raise ValueError(f"Pair identity failed to reopen uniquely for {case['case']}")
    return tuple(ids[0] for ids in found)


def signal_samples(path):
    samples = defaultdict(list)
    with path.open(newline="",encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            head = int(row["id"])
            if head in (3,4,8,9):
                samples[head].append((time_s(row["timestamp"]),int(row["state"])))
    return {k: sorted(v) for k,v in samples.items()}


def pack(rows, case, pair, signal, clip):
    focus = time_s(case["focus_start_utc"])
    a,b = clip
    names = {pair[0]:"A",pair[1]:"B"}
    frames = defaultdict(dict)
    targets = defaultdict(list)
    for stamp,ident,x,y,yaw,length,width,speed,motor in rows:
        if not motor and ident not in names:
            continue
        if ident not in names:
            names[ident] = f"V{len(names)-1}"
        name = names[ident]
        ms = round((stamp-focus)*1000)
        point = [name,round(x,2),round(y,2),round(yaw,1),round(length,2),round(width,2),round(speed,2),ms]
        if ident in pair:
            targets[name].append(point[1:])
        # Context display samples come from an explicit 100 ms bin. Keep the closest point per ID.
        bin_ms = round(ms/100)*100
        previous = frames[bin_ms].get(name)
        if previous is None or abs(ms-bin_ms) < abs(previous[-1]-bin_ms):
            frames[bin_ms][name] = point
    return {"case":case["case"],"lane":int(case["lane"]),"focus_utc":case["focus_start_utc"],
            "focus_end_ms":round((time_s(case["focus_end_utc"])-focus)*1000),
            "clip_start_ms":round((a-focus)*1000),"clip_end_ms":round((b-focus)*1000),
            "frames":[[k,list(v.values())] for k,v in sorted(frames.items())],
            "target_samples":{k:sorted(v,key=lambda p:p[-1]) for k,v in targets.items()},
            "heads":{k:[[round((t-focus)*1000),code] for t,code in v if a-2 <= t <= b+2]
                     for k,v in signal.items()}}


def terminal_zone(rows, track, lookup, regions):
    stamp,_,x,y,*_ = max((p for p in rows if p[1] == track),key=lambda p:p[0])
    cell = floor(x/CELL_M),floor(y/CELL_M)
    zones = [name for name,members in regions.items() if name != "east_left_through_overlap" and cell in members]
    if cell in lookup:
        zones.append("east_approach")
    return stamp,zones or ["outside_mapped_corridors"]


def build(data_root, sheet_path, manifest_path):
    map_path = data_root/"map.xodr"
    if sha(map_path) != EXPECTED_MAP:
        raise ValueError("Unrecognized K047 map")
    report = json.loads(manifest_path.read_text())
    grouped = defaultdict(list)
    with sheet_path.open(newline="",encoding="utf-8") as stream:
        for case in csv.DictReader(stream):
            focus = datetime.fromisoformat(case["focus_start_utc"])
            name,end = source_for(focus,report)
            window_start = time_s(case["replay_from_utc"])
            window_end = min((focus+timedelta(seconds=FOLLOWUP_S)-CLOCK).total_seconds(),end)
            grouped[name].append((case,(window_start,window_end)))
    survey = geometry(map_path)
    lookup = approach_lookup(map_path)
    regions = masks(map_path,CELL_M)
    regions["south_exit"] = set().union(*(raster(stripe,CELL_M)
                                          for stripe in pocket_screen_strips(map_path)["south_exit"]))
    results = []
    endpoints = {}
    identities = defaultdict(list)
    inputs = {map_path.name:EXPECTED_MAP,sheet_path.name:sha(sheet_path),manifest_path.name:sha(manifest_path)}
    for name, cases in grouped.items():
        track = data_root/name
        signal = data_root/name.replace("trajectories_","traffic-lights_")
        for path, k in ((track,"trajectory_sha256"),(signal,"signal_sha256")):
            actual = sha(path)
            if actual != report[name][k]:
                raise ValueError(f"Source does not match recorded SHA-256 for {path.name}")
            inputs[path.name] = actual
        raw = read_tracks(track,{c["case"]:w for c,w in cases},survey["extent"])
        signals = signal_samples(signal)
        for case, w in cases:
            rows = raw[case["case"]]
            pair = locate_pair(rows,case,lookup)
            results.append(pack(rows,case,pair,signals,w))
            identities[name,pair].append(case["case"])
            focus = time_s(case["focus_start_utc"])
            endpoints[case["case"]] = {}
            for track, role in zip(pair,("A","B"),strict=True):
                stamp,zones = terminal_zone(rows,track,lookup,regions)
                endpoints[case["case"]][role] = {"last_visible_ms":round((stamp-focus)*1000),
                                                "last_visible_zones":zones}
    payload = {"geometry":survey,"cases":sorted(results,key=lambda c:c["case"]),"input_hashes":inputs}
    audit = {"case_count":len(results),"all_pairs_reopened_uniquely":True,
             "same_pair_groups":[c for c in identities.values() if len(c)>1],
             "last_visible_observations":endpoints,"input_hashes":inputs}
    return payload,audit


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data",type=Path)
    parser.add_argument("sheet",type=Path)
    parser.add_argument("manifest",type=Path)
    parser.add_argument("output",type=Path)
    parser.add_argument("--audit", type=Path)
    args = parser.parse_args()
    payload,audit = build(args.data,args.sheet,args.manifest)
    args.output.write_text(json.dumps(payload,separators=(",",":"))+"\n")
    if args.audit:
        args.audit.write_text(json.dumps(audit,indent=2)+"\n")
