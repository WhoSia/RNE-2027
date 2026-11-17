"""Validate the raw Jinju municipal lane-count sample and audit its join keys."""
import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

BASE = ("수집시작일시", "수집종료일시", "수집위치", "차선")
LANE_COLUMNS = tuple(f"{i}차선 {name}" for i in range(1, 7)
                     for name in ("교통량", "차량종류"))


def vector(text, width):
    values = tuple(int(value) for value in text.split("/"))
    if len(values) != width or min(values) < 0:
        raise ValueError(f"Expected {width} nonnegative counts")
    return values


def audit(path):
    file_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    with path.open(encoding="cp949", newline="") as stream:
        reader = csv.reader(stream)
        if tuple(next(reader)) != BASE + LANE_COLUMNS:
            raise ValueError("Unexpected Jinju lane-count headers")
        return {"sha256": file_hash, "encoding": "cp949", **summarize(reader)}


def summarize(rows):
    exact = set()
    site_intervals = Counter()
    duration = Counter()
    locations = Counter()
    by_day = Counter()
    by_start_hour = Counter()
    lane_counts = Counter()
    limits = defaultdict(lambda: [None, None])
    movement_class_differences = 0
    for row in rows:
        if len(row) != 16 or not row[2].strip():
            raise ValueError("Malformed Jinju data row")
        start, end = map(datetime.fromisoformat, row[:2])
        elapsed = int((end - start).total_seconds())
        lanes = int(row[3])
        if not (1 <= lanes <= 6) or elapsed < 0:
            raise ValueError("Invalid observation interval or lane count")
        loc = row[2]
        a, b = limits[loc]
        limits[loc] = [start if a is None else min(a, start), end if b is None else max(b, end)]
        exact.add(tuple(row))
        locations[loc] += 1
        by_day[start.date().isoformat()] += 1
        by_start_hour[start.hour] += 1
        site_intervals[(loc, start, end)] += 1
        duration[elapsed] += 1
        lane_counts[lanes] += 1
        for i in range(6):
            movements, types = row[4 + 2 * i:6 + 2 * i]
            if i < lanes:
                flow = vector(movements, 6)
                classified = vector(types, 7)
                movement_class_differences += sum(flow[:4]) != sum(classified)
            elif movements or types:
                raise ValueError("Unexpected values beyond the reported lane count")
    if not exact:
        raise ValueError("No Jinju observations")
    by_site = {}
    for loc, count in locations.most_common():
        start, end = limits[loc]
        by_site[loc] = {"rows": count, "first_start": str(start), "last_end": str(end)}
    return {"rows": sum(locations.values()), "site_labels": len(locations),
            "exact_duplicate_excess": sum(locations.values()) - len(exact),
            "repeated_site_time_excess": sum(site_intervals.values()) - len(site_intervals),
            "first_start": str(min(a for a, _ in limits.values())),
            "last_end": str(max(b for _, b in limits.values())),
            "recorded_elapsed_seconds": dict(sorted(duration.items())),
            "lane_counts_per_row": dict(sorted(lane_counts.items())),
            "lane_records": sum(n * count for n, count in lane_counts.items()),
            "movement_class_count_differences": movement_class_differences,
            "rows_by_start_date": by_day, "rows_by_start_hour": dict(sorted(by_start_hour.items())),
            "sites": by_site}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(audit(args.csv), ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
