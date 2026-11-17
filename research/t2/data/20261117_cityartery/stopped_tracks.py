"""Estimate sustained low-speed episodes from processed samples, as proxies."""
import argparse
import json
from collections import Counter
from csv import DictReader
from io import TextIOWrapper
from pathlib import Path
from zipfile import ZipFile


def summarize(stream, cutoff_kmh=2.0, min_span_s=2.0, max_gap_s=1.1):
    """Require at least min_span_s of contiguous sampled speeds at/below cutoff."""
    last = {}
    stop_start = {}
    episodes = Counter()
    observed = Counter()
    with_episode = set()
    rows = DictReader(stream)
    for row in rows:
        category = row["Type"].strip()
        key = row["vedio-id"].strip(), row["Track ID-new"].strip()
        t = float(row["Time [s]-new"])
        speed = float(row["Speed [km/h]"])
        if key not in last:
            observed[category] += 1
        elif not 0 < t - last[key] <= max_gap_s:
            stop_start.pop(key, None)
        last[key] = t
        if speed > cutoff_kmh:
            stop_start.pop(key, None)
            continue
        if key not in stop_start:
            stop_start[key] = t
        start = stop_start[key]
        if start is not None and t - start >= min_span_s:
            episodes[category] += 1
            with_episode.add((category, key))
            stop_start[key] = None
    return {"tracks": dict(observed), "episodes": dict(episodes),
            "tracks_with_episode": dict(Counter(category for category, _ in with_episode))}


def audit(path):
    with ZipFile(path) as source:
        members = sorted(n for n in source.namelist() if "/Processed Data/" in n and n.endswith(".csv"))
        if not members:
            raise ValueError("Missing processed trajectory files")
        result = {}
        for name in members:
            with TextIOWrapper(source.open(name), encoding="utf-8-sig", newline="") as stream:
                result[Path(name).name] = summarize(stream)
    return {"cutoff_kmh": 2.0, "minimum_span_s": 2.0, "maximum_sample_gap_s": 1.1,
            "outer_boundary": "recording-local; the start and end may be censored", "files": result}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(audit(args.archive), indent=2, sort_keys=True) + "\n")
