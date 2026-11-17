"""Audit the delivered trajectory clocks and identifiers; export aggregates only."""
import argparse
from collections import Counter
from csv import DictReader
from io import TextIOWrapper
import json
from math import isfinite
from pathlib import Path
from zipfile import ZipFile


def processed(stream):
    rows = DictReader(stream, skipinitialspace=True)
    fields = {"Track ID-new", "vedio-id", "Time [s]", "Time [s]-new",
              "Type", "x_sumo", "y_sumo", "Speed [km/h]", "lane_id"}
    if not fields.issubset(rows.fieldnames or ()):
        raise ValueError("Processed file has an unexpected schema")
    last = {}
    classes = Counter()
    tracks = Counter()
    gaps = Counter()
    lanes = set()
    clocks_disagree = missing_gates = 0
    first_time, final_time = float("inf"), float("-inf")
    for row in rows:
        key = row["vedio-id"].strip(), row["Track ID-new"].strip()
        kind = row["Type"].strip()
        time, old = (float(row[name]) for name in ("Time [s]-new", "Time [s]"))
        coordinates = tuple(float(row[name]) for name in ("x_sumo", "y_sumo", "Speed [km/h]"))
        if not all(key) or not kind or not all(map(isfinite, (time, old, *coordinates))):
            raise ValueError("Missing or nonfinite processed-track field")
        classes[kind] += 1
        lanes.add(row["lane_id"].strip())
        clocks_disagree += abs(time - old) > 1e-6
        missing_gates += all((row.get(name) or "").strip() in ("", "-")
                             for name in ("Entry Gate", "Exit Gate"))
        if key in last:
            previous, previous_kind = last[key]
            if kind != previous_kind or time <= previous:
                raise ValueError("Track identity or within-track clock is inconsistent")
            gaps[round(time - previous, 6)] += 1
        else:
            tracks[kind] += 1
        last[key] = time, kind
        first_time, final_time = min(time, first_time), max(time, final_time)
    if not last:
        raise ValueError("Empty processed file")
    return {"sample_rows": sum(classes.values()), "recording_scoped_tracks": sum(tracks.values()),
            "track_types": dict(tracks), "video_ids": sorted({key[0] for key in last}),
            "lane_codes_seen": len(lanes), "new_clock_seconds": [first_time, final_time],
            "within_track_gap_s": dict(sorted(gaps.items())), "clock_disagreement_rows": clocks_disagree,
            "rows_with_both_gates_missing": missing_gates}


def audit(path):
    with ZipFile(path) as source:
        members = sorted(n for n in source.namelist() if "/Processed Data/" in n and n.endswith(".csv"))
        if not members:
            raise ValueError("Missing processed trajectory files")
        result = {}
        for name in members:
            with TextIOWrapper(source.open(name), encoding="utf-8-sig", newline="") as stream:
                result[Path(name).name] = processed(stream)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(audit(args.archive), indent=2, sort_keys=True) + "\n")
