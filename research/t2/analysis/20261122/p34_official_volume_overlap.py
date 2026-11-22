"""Exact-source DLR published crossing bins vs naive same-second track presence.

This is a negative-control observation audit, not a lane matched detector.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from pathlib import Path

SOURCE_HASHES = {
    "volume": "00f6f29b2be6c2fa517077de3b7accbbfc75edddc92332534f00ad6b62312798",
    "trajectories": "6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50",
    "signals": "95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c",
}
EXPECTED_MOVEMENTS = (
    'East1South1', 'East2West0', 'East3West1', 'South1West1',
    'South2North1', 'South4East0', 'West0North0', 'West0North1',
    'West1East0', 'West2East0', 'West2East1', 'West4South1',
)
GAP_MIN_SEC = 1.5


def hash_guard(path: Path, name: str) -> None:
    actual = sha256(path.read_bytes()).hexdigest()
    if actual != SOURCE_HASHES[name]:
        raise ValueError(f'{name} SHA-256 source drift: {actual}')


def parse_utc(value: str) -> datetime:
    try:
        dt = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f'bad ISO time {value!r}') from exc
    if dt.tzinfo is None or dt.utcoffset() != timedelta(0):
        raise ValueError(f'not UTC offset-aware: {value!r}')
    return dt.astimezone(timezone.utc)


def read_volume(path: Path, *, guard: bool = True):
    if guard:
        hash_guard(path, 'volume')
    with path.open(newline='', encoding='utf-8') as f:
        rd = csv.DictReader(f)
        if tuple(rd.fieldnames or ()) != ('timestamp', *EXPECTED_MOVEMENTS):
            raise ValueError('unknown or reordered volume schema')
        rows = {}
        for line in rd:
            t = parse_utc(line['timestamp'])
            if t.microsecond:
                raise ValueError('not a 1-second grid')
            if t in rows:
                raise ValueError('duplicate published volume time')
            if rows and t <= next(reversed(rows)):
                raise ValueError('out of order published volume time')
            vals = []
            for m in EXPECTED_MOVEMENTS:
                v = line[m]
                if v not in ('0', '1'):
                    raise ValueError(f'unexpected movement indicator: {m}={v}')
                vals.append(int(v))
            rows[t] = tuple(vals)
    if not rows:
        raise ValueError('no volume rows')
    return rows


def read_tracks(path: Path, *, guard: bool = True):
    if guard:
        hash_guard(path, 'trajectories')
    bins = defaultdict(set)
    observations = []
    with path.open(newline='', encoding='utf-8') as f:
        rd = csv.DictReader(f)
        if not rd.fieldnames or not {'timestamp', 'id'}.issubset(rd.fieldnames):
            raise ValueError('trajectory schema missing time or ID')
        for line in rd:
            t = parse_utc(line['timestamp'])
            try:
                vid = int(line['id'])
            except (ValueError, TypeError) as exc:
                raise ValueError('invalid tracked ID') from exc
            if vid <= 0:
                raise ValueError('nonpositive tracked ID')
            bins[t.replace(microsecond=0)].add(vid)
            observations.append((t, vid))
    if not observations:
        raise ValueError('empty trajectories')
    return bins, observations


def read_signal_gap(path: Path, *, guard: bool = True):
    if guard:
        hash_guard(path, 'signals')
    timestamps = defaultdict(dict)
    with path.open(newline='', encoding='utf-8') as f:
        rd = csv.DictReader(f)
        if tuple(rd.fieldnames or ()) != ('timestamp', 'id', 'state'):
            raise ValueError('unexpected signal schema')
        for line in rd:
            t = parse_utc(line['timestamp'])
            try:
                hid = int(line['id'])
                state = int(line['state'])
            except (TypeError, ValueError) as exc:
                raise ValueError('bad signal ID/state') from exc
            if hid <= 0 or not 0 <= state <= 9:
                raise ValueError('out-of-range signal ID/state')
            if hid in timestamps[t]:
                raise ValueError('duplicate signal ID/timestamp')
            timestamps[t][hid] = state
    times = sorted(timestamps)
    if not times:
        raise ValueError('empty signals')
    namespaces = set(timestamps[times[0]])
    if any(set(row) != namespaces for row in timestamps.values()):
        raise ValueError('missing head on global signal sample')
    gaps = []
    for before, after in zip(times, times[1:]):
        if (after - before).total_seconds() > GAP_MIN_SEC:
            changed = [i for i in sorted(namespaces) if timestamps[before][i] != timestamps[after][i]]
            gaps.append({'start_utc': before.isoformat(), 'end_utc': after.isoformat(),
                         'duration_ms': round((after-before).total_seconds()*1000),
                         'all_heads_sampled_at_both_ends': len(namespaces),
                         'changed_endpoint_ids': changed,
                         'changed_endpoint_codes': {str(i): [timestamps[before][i],timestamps[after][i]] for i in changed},
                         '_start': before, '_end': after})
    return {'sample_instants': len(times), 'head_ids': len(namespaces), 'gap_records': gaps}


def confusion(labels: dict, tracked_by_second: dict, *, shift_s: int = 0):
    shifted = {sec + timedelta(seconds=shift_s) for sec, ids in tracked_by_second.items() if ids}
    tp = fp = fn = tn = 0
    for t, movement_flags in labels.items():
        positive = any(movement_flags)
        predicted = t in shifted
        if positive and predicted: tp += 1
        elif positive: fn += 1
        elif predicted: fp += 1
        else: tn += 1
    n = tp + fp + fn + tn
    return {'shift_seconds': shift_s, 'bins': n, 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn,
            'precision': tp/(tp+fp) if tp+fp else None,
            'recall': tp/(tp+fn) if tp+fn else None,
            'specificity': tn/(tn+fp) if tn+fp else None}


def analyze(volume: Path, tracks: Path, signals: Path, *, guard: bool = True):
    labels = read_volume(volume, guard=guard)
    binned, obs = read_tracks(tracks, guard=guard)
    sig = read_signal_gap(signals, guard=guard)
    positive_times = [t for t, flags in labels.items() if any(flags)]
    total_positive_channels = sum(sum(x) for x in labels.values())
    if total_positive_channels < len(positive_times):
        raise AssertionError('impossible movement count')
    gaps = []
    for g in sig['gap_records']:
        sub = [(t,vid) for t,vid in obs if g['_start'] < t < g['_end']]
        affected_volume = [t for t in labels if t < g['_end'] and t + timedelta(seconds=1) > g['_start']]
        gaps.append({**{k:v for k,v in g.items() if not k.startswith('_')},
                     'tracked_samples_strictly_inside': len(sub),
                     'distinct_tracked_ids_strictly_inside': len({vid for _,vid in sub}),
                     'official_1s_volume_intervals_intersecting_gap': [x.isoformat() for x in affected_volume],
                     'published_positive_bins_whose_intervals_intersect_gap': sum(bool(any(labels[t])) for t in affected_volume)})
    candidate_hist = Counter(len(binned.get(t, ())) for t in positive_times)
    return {
        'protocol': 'P34_OFFICIAL_DLR_VOLUME_VS_TRAJECTORY_BIN_BASELINE',
        'scope': 'REAL_CSV_TEMPORAL_COOCCURRENCE_NOT_VEHICLE_MATCH_NOT_CAUSAL_SIGNAL',
        'source_sha256': SOURCE_HASHES if guard else 'TEST_FIXTURE_NO_HASH',
        'volume_rows_1s': len(labels),
        'volume_movement_channels': len(EXPECTED_MOVEMENTS),
        'published_positive_channel_bins': total_positive_channels,
        'published_positive_unique_1s_bins': len(positive_times),
        'trajectory_rows': len(obs),
        'distinct_tracked_ids': len({vid for _,vid in obs}),
        'candidate_ids_at_official_positive_bins_histogram': dict(sorted(candidate_hist.items())),
        'positive_bins_with_more_than_one_candidate': sum(len(binned.get(t, ())) > 1 for t in positive_times),
        'movement_positive_counts': {m:sum(row[i] for row in labels.values()) for i,m in enumerate(EXPECTED_MOVEMENTS)},
        'naive_presence_classifier': confusion(labels,binned),
        'shift_diagnostics': [confusion(labels,binned,shift_s=d) for d in (-2,-1,0,1,2)],
        'signal_sample_instants': sig['sample_instants'],
        'signal_heads_per_instant': sig['head_ids'],
        'global_signal_observation_gaps_over_1_5s': gaps,
        'interpretive_limits': [
            'Movement labels and track IDs do not establish per-vehicle event identity',
            'Published volume and trajectory exports may share an upstream tracking pipeline',
            'Any track in a second is an intentionally weak negative-control baseline, not a geomatic stopline detector',
            'Common-mode missing signal observation cannot be filled from trajectories',
            'No causal traffic-signal intervention, stopline geometry matching, or SUMO validation',
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('volume', type=Path)
    p.add_argument('trajectories', type=Path)
    p.add_argument('signals', type=Path)
    p.add_argument('out', type=Path)
    args = p.parse_args()
    obj = analyze(args.volume, args.trajectories, args.signals)
    args.out.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)+'\n',encoding='utf-8')

if __name__ == '__main__':
    main()
