"""D42 raw DLR signal/traffic-volume co-time audit.

No mapping of integer light states to color. Missing signal observation
is not filled by nearest-neighbor copying. This module is offline-only.
Inputs are original DLR UT v1.3.1 CSVs.
"""
from collections import Counter
from csv import DictReader
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json

def parse_utc(text: str) -> datetime:
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError("timestamp missing time zone")
    return parsed.astimezone(timezone.utc)

def categorical_signal_gate(path: Path) -> dict:
    by_head = {}
    codes = Counter()
    with path.open(newline="", encoding="utf-8") as file:
        for row in DictReader(file):
            t = parse_utc(row["timestamp"])
            head = int(row["id"])
            state = int(row["state"])
            by_head.setdefault(head, []).append((t, state))
            codes[state] += 1
    gaps = []
    transitions = Counter()
    crossing_gap = 0
    for head, observations in sorted(by_head.items()):
        observations.sort()
        for (t0, s0), (t1, s1) in zip(observations, observations[1:]):
            delta = (t1 - t0).total_seconds()
            if delta <= 0:
                raise ValueError("nonincreasing light timestamp")
            if delta > 1.5:
                gaps.append({"head": head, "before": t0.isoformat(),
                             "after": t1.isoformat(), "gap_s": delta})
            if s0 != s1:
                transitions[(s0,s1)] += 1
                if delta > 1.5:
                    crossing_gap += 1
    return {"heads": len(by_head), "rows": sum(map(len, by_head.values())),
            "unique_timestamps": len({t for observations in by_head.values() for t, _ in observations}),
            "states": dict(sorted(codes.items())), "gaps": gaps,
            "transition_count": sum(transitions.values()),
            "transition_across_gaps": crossing_gap,
            "transitions": {f"{a}->{b}": n for (a,b),n in sorted(transitions.items())}}

def volume_gate(path: Path) -> dict:
    total = 0
    per_movement = Counter()
    seen = set()
    with path.open(newline="", encoding="utf-8") as file:
        for row in DictReader(file):
            t = parse_utc(row["timestamp"])
            if t in seen:
                raise ValueError("duplicate volume timestamp")
            seen.add(t)
            for key, value in row.items():
                if key == "timestamp": continue
                n = int(value)
                if n < 0: raise ValueError("negative traffic count")
                per_movement[key] += n
                total += n
    return {"seconds":len(seen),"movements":len(per_movement),
            "observed_count_cell_sum":total,"per_movement":dict(per_movement)}

def main(signal_path: str, volume_path: str):
    light = categorical_signal_gate(Path(signal_path))
    counts = volume_gate(Path(volume_path))
    print(json.dumps({"signal":light,"volume":counts},indent=2))
if __name__ == "__main__":
    import sys
    if len(sys.argv)!=3:
        raise SystemExit("usage: signal_volume_gate.py traffic-lights.csv traffic-volume.csv")
    main(sys.argv[1],sys.argv[2])
