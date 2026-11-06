"""Fail-closed ingestion of recorded AV encounters with traffic lights.

The CATS-Lab/Waymo-derived source is a *selected* set of short trajectory
segments; it is neither a full intersection record nor a signal policy trial.
No network calls and no direct real-world traffic-control actions.
"""
from __future__ import annotations
import csv
import hashlib
import io
import math
from dataclasses import dataclass

REQUIRED = ('AV_speed', 'AV_x', 'AV_y', 'AV_acc', 'AV_distance_to_light',
            'nearest_light_x', 'nearest_light_y', 'nearest_light_state',
            'AV_speed_enhanced', 'AV_acc_enhanced')
RED = frozenset((1, 4)); GREEN = frozenset((3, 6)); YELLOW = frozenset((2, 5, 8))
UNKNOWN = frozenset((-1, 0))

@dataclass(frozen=True)
class Observation:
    speed_mps: float
    distance_m: float
    signal_code: int


def parse_csv(original_bytes: bytes) -> list[Observation]:
    if not isinstance(original_bytes, bytes) or not original_bytes:
        raise ValueError('original CSV bytes required')
    try:
        text = original_bytes.decode('utf-8-sig')
    except UnicodeDecodeError as ex:
        raise ValueError('non-UTF8 CSV') from ex
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None or set(REQUIRED) - set(reader.fieldnames):
        raise ValueError('required columns missing')
    if len(reader.fieldnames) != len(set(reader.fieldnames)):
        raise ValueError('duplicate header')
    observations = []
    for row in reader:
        if None in row or any(row[k] is None or not row[k].strip() for k in REQUIRED):
            raise ValueError('missing or malformed CSV row')
        try:
            values = [float(row[k]) for k in REQUIRED]
        except (ValueError, TypeError) as ex:
            raise ValueError('non-numeric frame') from ex
        if not all(map(math.isfinite, values)):
            raise ValueError('nonfinite frame')
        code = float(row['nearest_light_state'])
        if not code.is_integer() or int(code) not in range(-1, 9):
            raise ValueError('unsupported signal code; do not silently map to red/green')
        speed = float(row['AV_speed'])
        if speed < -0.5:
            raise ValueError('significantly negative velocity; inspect coordinate convention')
        observations.append(Observation(speed, float(row['AV_distance_to_light']), int(code)))
    if len(observations) < 2:
        raise ValueError('at least two frames required')
    return observations


def summarize(original_bytes: bytes) -> dict:
    frames = parse_csv(original_bytes)
    n = len(frames)
    return {
        'sha256': hashlib.sha256(original_bytes).hexdigest(),
        'frames': n,
        'mean_speed_mps': sum(x.speed_mps for x in frames)/n,
        'frames_below_0p5_mps': sum(x.speed_mps < 0.5 for x in frames),
        'red_or_red_arrow_frames': sum(x.signal_code in RED for x in frames),
        'green_or_green_arrow_frames': sum(x.signal_code in GREEN for x in frames),
        'unknown_state_frames': sum(x.signal_code in UNKNOWN for x in frames),
        'unrecognized_state_codes': sorted({x.signal_code for x in frames if x.signal_code in UNKNOWN}),
        'distance_min_m': min(x.distance_m for x in frames),
        'distance_max_m': max(x.distance_m for x in frames),
    }


def verify_observed_file(original_bytes: bytes, entry: dict) -> dict:
    a = summarize(original_bytes)
    for key in ('frames', 'frames_below_0p5_mps', 'red_or_red_arrow_frames',
                'green_or_green_arrow_frames'):
        if a[key] != entry[key]:
            raise ValueError(f'real original differs from separately logged metadata: {key}')
    if not math.isclose(a['mean_speed_mps'],entry['mean_speed_mps'],rel_tol=1e-12,abs_tol=1e-12):
        raise ValueError('mean speed mismatch; verify original bytes/source version')
    return a
