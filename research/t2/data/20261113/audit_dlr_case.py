"""Audit DLR-UT 1.3.1 CSV and OpenDRIVE files without inventing ground truth.

Run: python audit_dlr_case.py --volume traffic-volume_*.csv --signals traffic-lights_*.csv --xodr bs-inner-ring-road-ut.xodr
Volume CSV contains publisher-derived counts, not independent annotation.
Numeric signal-state codes are deliberately left uninterpreted.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import xml.etree.ElementTree as ET

def parse_iso_timestamp(value: str) -> datetime:
    t = datetime.fromisoformat(value)
    if t.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return t.astimezone(timezone.utc)

def audit_volume(path: str | Path) -> dict:
    path = Path(path)
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or reader.fieldnames[0] != "timestamp":
            raise ValueError("expected timestamp in first column")
        movements = reader.fieldnames[1:]
        times, totals = [], Counter()
        rows = 0
        for row in reader:
            if None in row or any(row[k] is None for k in reader.fieldnames):
                raise ValueError("malformed CSV record")
            t = parse_iso_timestamp(row["timestamp"])
            times.append(t)
            for movement in movements:
                val = int(row[movement])
                if val < 0:
                    raise ValueError("negative count")
                totals[movement] += val
            rows += 1
        if not 0 < rows <= 900:
            raise ValueError(f"15-minute publisher series has impossible row count: {rows}")
        if len(set(times)) != rows or any(b-a != timedelta(seconds=1) for a,b in zip(times,times[1:])):
            raise ValueError("volume timestamps should be unique, consecutive seconds")
        return {"filename":path.name, "rows":rows,"expected_rows":900,"partial_window":rows<900,"coverage_ratio":rows/900,"movement_columns":len(movements),
                "start_utc":times[0].isoformat(), "end_utc":times[-1].isoformat(),
                "total_publisher_volume":sum(totals.values()),
                "movements":dict(sorted(totals.items()))}

def nearest_second(t: datetime) -> datetime:
    return (t + timedelta(microseconds=500000)).replace(microsecond=0)

def audit_signals(path: str | Path) -> dict:
    path = Path(path)
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != ["timestamp","id","state"]:
            raise ValueError("unexpected signal schema")
        moments = defaultdict(dict)
        codes = Counter()
        records = 0
        for row in reader:
            t = parse_iso_timestamp(row["timestamp"])
            i = int(row["id"])
            if i in moments[t]:
                raise ValueError("duplicate signal head at same timestamp")
            moments[t][i] = row["state"]
            codes[row["state"]] += 1
            records += 1
    if not moments:
        raise ValueError("empty signal file")
    if any(set(states) != set(range(1,31)) for states in moments.values()):
        raise ValueError("expected all 30 heads for each sampled timestamp")
    distinct_times = sorted(moments)
    floor_bins = Counter(t.replace(microsecond=0) for t in distinct_times)
    rounded_bins = Counter(nearest_second(t) for t in distinct_times)
    return {"filename":path.name, "head_count":30, "records":records,
            "sample_instants":len(moments),
            "signal_state_codes_uninterpreted":dict(sorted(codes.items())),
            "floor_colliding_second_buckets":sum(n>1 for n in floor_bins.values()),
            "nearest_second_colliding_buckets":sum(n>1 for n in rounded_bins.values()),
            "nearest_second_unique_bins":len(rounded_bins),
            "min_utc":distinct_times[0].isoformat(),"max_utc":distinct_times[-1].isoformat()}

def audit_xodr(path: str | Path) -> dict:
    root = ET.parse(path).getroot()
    if root.tag != "OpenDRIVE":
        raise ValueError("expected OpenDRIVE root")
    header = root.find("header")
    return {"filename":Path(path).name,
            "version":header.attrib.get("version") if header is not None else None,
            "roads":len(root.findall("road")),
            "junctions":len(root.findall("junction")),
            "junction_connections":len(root.findall("./junction/connection")),
            "lane_sections":len(root.findall(".//laneSection")),
            "lane_nodes":len(root.findall(".//laneSection/*/lane")),
            "road_signal_elements":len(root.findall(".//road/signals/signal")),
            "warning":"Road signal objects are not necessarily a mapping to DLR-UT signal-head IDs 1..30."}

def run(volume_paths,signal_paths,xodr_path):
    volumes=[audit_volume(p) for p in volume_paths]
    signals=[audit_signals(p) for p in signal_paths]
    return {"dataset":"DLR-UT v1.3.1","volume_blocks":volumes,
            "signal_blocks":signals,
            "xodr":audit_xodr(xodr_path) if xodr_path else None,
            "publisher_volume_sum":sum(b["total_publisher_volume"] for b in volumes),
            "limitations":["not independent vehicle counts",
                           "numeric signal-state codes need authoritative interpretation",
                           "head ID to road movement mapping unverified",
                           "movement-column schemas can change between volume files"]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--volume",nargs="+",required=True)
    p.add_argument("--signals",nargs="+",required=True)
    p.add_argument("--xodr")
    p.add_argument("--output",default="dlr_audit.json")
    args=p.parse_args()
    result=run(args.volume,args.signals,args.xodr)
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps({"publisher_volume_sum":result["publisher_volume_sum"],
                       "signal_instants":[s["sample_instants"] for s in result["signal_blocks"]]},indent=2))

if __name__=="__main__":
    main()
