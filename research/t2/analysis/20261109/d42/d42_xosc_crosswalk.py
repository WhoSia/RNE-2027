"""DLR UT 2023-09-24 12:00–12:15: 20 Hz CSV to derived XOSC full-vertex audit.

This is a *source transformation contract*, not independent sensor validation.
Pinned source file hashes and actually executed tests are in D42_REAL15_XOSC_COORDINATE_CROSSWALK.md.
"""
import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pandas as pd

UTM_LOCAL_ORIGIN = (604763.0, 5792795.0)
UTC_FRAME_ZERO = pd.Timestamp("2023-09-24 12:00:00.016482+00:00")


def crosswalk(csv_path, xosc_path):
    df = pd.read_csv(csv_path, usecols=["timestamp", "id", "center_easting", "center_northing"])
    df["t"] = pd.to_datetime(df.timestamp, utc=True, format="mixed")
    groups = {str(k): g.sort_values("t") for k, g in df.groupby("id")}
    count = vertex_count = 0
    unknown, different, matched = [], [], set()
    max_x = max_y = max_t = 0.0
    rms_x = rms_y = 0.0
    for event, el in ET.iterparse(xosc_path, events=("end",)):
        if el.tag != "Trajectory":
            continue
        name = el.attrib["name"].removesuffix("Trajectory")
        vertices = list(el.iter("Vertex"))
        if name not in groups:
            unknown.append(name)
            el.clear()
            continue
        g = groups[name]
        if len(g) != len(vertices):
            different.append({"id": name, "raw": len(g), "xosc": len(vertices)})
            el.clear()
            continue
        t = np.array([float(v.attrib["time"]) for v in vertices])
        world = [v.find("Position/WorldPosition") for v in vertices]
        x = np.array([float(w.attrib["x"]) for w in world])
        y = np.array([float(w.attrib["y"]) for w in world])
        dt = np.abs((g.t - UTC_FRAME_ZERO).dt.total_seconds().to_numpy() - t)
        dx = np.abs(g.center_easting.to_numpy() - UTM_LOCAL_ORIGIN[0] - x)
        dy = np.abs(g.center_northing.to_numpy() - UTM_LOCAL_ORIGIN[1] - y)
        max_t = max(max_t, float(dt.max()))
        max_x = max(max_x, float(dx.max()))
        max_y = max(max_y, float(dy.max()))
        rms_x += float(np.sum(dx * dx))
        rms_y += float(np.sum(dy * dy))
        count += 1
        vertex_count += len(vertices)
        matched.add(name)
        el.clear()
    return {
        "matched_track_ids": count,
        "matched_vertices": vertex_count,
        "raw_track_ids": len(groups),
        "xosc_unknown_track_ids": unknown,
        "csv_ids_not_matched_to_xosc": sorted(set(groups) - matched),
        "different_length_tracks": different,
        "utm_local_origin_m": list(UTM_LOCAL_ORIGIN),
        "csv_frame_zero_utc": str(UTC_FRAME_ZERO),
        "max_timestamp_error_s": max_t,
        "max_easting_error_m": max_x,
        "max_northing_error_m": max_y,
        "rms_easting_error_m": float((rms_x / vertex_count) ** .5) if vertex_count else None,
        "rms_northing_error_m": float((rms_y / vertex_count) ** .5) if vertex_count else None,
    }


def accepted(result, coordinate_tolerance_m=.001, time_tolerance_s=1e-9):
    return (
        result["matched_track_ids"] == result["raw_track_ids"]
        and not result["xosc_unknown_track_ids"]
        and not result["csv_ids_not_matched_to_xosc"]
        and not result["different_length_tracks"]
        and result["max_easting_error_m"] <= coordinate_tolerance_m
        and result["max_northing_error_m"] <= coordinate_tolerance_m
        and result["max_timestamp_error_s"] <= time_tolerance_s
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    p.add_argument("--xosc", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    result = crosswalk(Path(args.csv), Path(args.xosc))
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    assert accepted(result), "XOSC and CSV correspondence failed"
