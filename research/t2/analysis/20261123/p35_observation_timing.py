"""P35: inspect *available-at-crossing* field signal samples, not controller policy.

P34 counted events come from same DLR producer as volume, NOT independent field truth.
P33 traffic-light signals cannot yet be assigned to these inferred approach crossings.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right, bisect_left
from collections import Counter
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import statistics
import sys
from zipfile import ZipFile

P34_ARCHIVE_SHA = 'bb8701db35578951e82202845c5fa9b65d5ee55afb31c1afed22292e65a3c679'
P34_EVENT_SHA = 'ea0eaae72afd8e82547a5f0b278765e27a871d86cdabeb34a2e4bf4e0a646c72'
SIGNAL_SHA = '95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c'
VOLUME_SHA = '00f6f29b2be6c2fa517077de3b7accbbfc75edddc92332534f00ad6b62312798'
FRESHNESS = (0.25, 0.5, 1.0, 1.5, 2.5)
MATCH_THRESHOLDS = (0.25, 0.5, 0.75, 1.0, 1.5)
GAP_START = datetime.fromisoformat('2023-09-24T23:31:44.010+00:00')
GAP_END = datetime.fromisoformat('2023-09-24T23:31:46.014+00:00')


def verify_bytes(path: Path, sha: str) -> bytes:
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != sha:
        raise ValueError(f'SHA-256 mismatch: {path}')
    return data


def load_p34(archive: Path):
    verify_bytes(archive, P34_ARCHIVE_SHA)
    with ZipFile(archive) as z:
        data = z.read('p34_result.json')
        if hashlib.sha256(data).hexdigest() != P34_EVENT_SHA:
            raise ValueError('P34 event ledger differs from frozen original')
        j = json.loads(data)
        if len(j['crossings']) != 17 or len(j['matched_pairs']) != 16:
            raise ValueError('unexpected P34 crossing/matching count')
        return j


def read_signals(path: Path):
    verify_bytes(path, SIGNAL_SHA)
    heads = {}
    with path.open(newline='', encoding='utf-8') as f:
        rd = csv.DictReader(f)
        if rd.fieldnames != ['timestamp', 'id', 'state']:
            raise ValueError('signal schema changed')
        n = 0
        for row in rd:
            head = int(row['id'])
            state = int(row['state'])
            timestamp = datetime.fromisoformat(row['timestamp'])
            if timestamp.tzinfo is None or head not in range(1, 31) or state not in range(10):
                raise ValueError('out-of-domain signal timestamp, head or state')
            heads.setdefault(head, []).append((timestamp, state))
            n += 1
    if n != 26970 or set(heads) != set(range(1, 31)):
        raise ValueError('incomplete signals')
    grid = None
    for head, seq in heads.items():
        seq.sort()
        ticks = [t for t,_ in seq]
        if len(ticks) != len(set(ticks)) or len(seq) != 899:
            raise ValueError(f'duplicate or missing samples on head {head}')
        if grid is not None and ticks != grid:
            raise ValueError('heads are not on common acquisition grid')
        grid = ticks
    gaps = [(a.isoformat(), b.isoformat(), (b-a).total_seconds())
            for a,b in zip(grid,grid[1:]) if (b-a).total_seconds() > 1.5]
    if len(gaps) != 1 or gaps[0][:2] != (GAP_START.isoformat(), GAP_END.isoformat()):
        raise ValueError('unexpected common signal gap')
    return heads,grid,gaps


def crossing_brackets(crossings):
    clean = []
    for e in crossings:
        a = datetime.fromisoformat(e['bracket_start_utc'])
        b = datetime.fromisoformat(e['bracket_end_utc'])
        t = datetime.fromisoformat(e['crossing_time_utc'])
        if not (a.tzinfo and b.tzinfo and t.tzinfo and a <= t <= b):
            raise ValueError('invalid or non-causal event bracket')
        if abs((b-a).total_seconds() - 0.05) > 1e-6 or e['controlling_signal_id'] is not None:
            raise ValueError('P34 bracket or unmapped head changed')
        clean.append((a,b,t))
    return clean


def analyse(archive: Path, signals: Path, volume: Path):
    p34 = load_p34(archive)
    heads,grid,gaps = read_signals(signals)
    verify_bytes(volume, VOLUME_SHA)
    bracket = crossing_brackets(p34['crossings'])
    # Import the *frozen original matcher* directly from its immutable ZIP, not a copied rewrite.
    sys.path.insert(0, str(archive))
    try:
        import p34_dlr_stopline_event_reconciliation as p34lib
        old_tolerance = p34lib.MAX_MATCH_ERROR_S
        volume_events = p34lib.reference_volume_events(p34lib.rows_from_csv(volume))
        if len(volume_events) != 17:
            raise ValueError('official event count drift')
        sensitivity = []
        try:
            for limit in MATCH_THRESHOLDS:
                p34lib.MAX_MATCH_ERROR_S = limit
                paired, lost_c, lost_v = p34lib.reconcile(p34['crossings'], volume_events)
                sensitivity.append({'matching_tolerance_s': limit, 'matched':len(paired),
                                    'unmatched_trajectory':len(lost_c),'unmatched_volume':len(lost_v),
                                    'median_abs_error_s':round(statistics.median(x['abs_time_difference_s'] for x in paired),6) if paired else None})
        finally:
            p34lib.MAX_MATCH_ERROR_S = old_tolerance
    finally:
        sys.path.pop(0)
    if next(v['matched'] for v in sensitivity if v['matching_tolerance_s']==1.0) != 16:
        raise AssertionError('P34 pairing parity failed')
    freshness_counts = Counter()
    hindsight_future = 0
    closest_future_after_bracket = 0
    discordant_head_pairs = 0
    crossing_with_discordant_head = 0
    straddled_sample_brackets = 0
    event_rows = []
    for c,(a,b,t) in zip(p34['crossings'],bracket):
        idx = bisect_right(grid, a) - 1
        next_after_idx = bisect_right(grid, b)
        if idx < 0 or next_after_idx >= len(grid):
            raise ValueError('outside observable signal time interval')
        past, nxt = grid[idx],grid[next_after_idx]
        if not past <= a <= t <= b < nxt:
            raise ValueError('invalid source ordering or event bracket')
        # The vehicle bracket can straddle an observed 1Hz signal sample; never
        # pretend its exact physical crossing instant is known within 50ms.
        inside_count = next_after_idx - (idx+1)
        straddled_sample_brackets += bool(inside_count)
        age = (b-past).total_seconds()
        left_idx = bisect_right(grid,t)-1
        right_idx = left_idx+1
        if left_idx < 0 or right_idx >= len(grid):
            raise ValueError('crossing interpolation outside signal coverage')
        nearest_next = ((grid[right_idx]-t).total_seconds() <
                        (t-grid[left_idx]).total_seconds())
        nearest = grid[right_idx] if nearest_next else grid[left_idx]
        if nearest>t: hindsight_future += 1
        if nearest>b: closest_future_after_bracket += 1
        changes = [head for head in heads if
                   heads[head][idx][1]!=heads[head][next_after_idx][1]]
        discordant_head_pairs += len(changes)
        crossing_with_discordant_head += bool(changes)
        for threshold in FRESHNESS:
            if age <= threshold+1e-10: freshness_counts[threshold]+=1
        gap_overlaps = a < GAP_END and b > GAP_START
        event_rows.append({'object_id':c['id'],'source_arm':c['source_arm'],
            'crossing_estimate':t.isoformat(), 'bracket_start':a.isoformat(), 'bracket_end':b.isoformat(),
            'causal_last_sample':past.isoformat(),'first_future_sample':nxt.isoformat(),
            'causal_sample_age_at_bracket_end_s':round(age,6),
            'nearest_hindsight_uses_future':nearest>t,
            'nearest_hindsight_timestamp':nearest.isoformat(),
            'signal_samples_inside_crossing_bracket':inside_count,
            'sampled_state_discordant_head_ids':changes,
            'shared_gap_overlap':gap_overlaps,
            'status':'UNMAPPED_SIGNAL_HEAD_TO_MOVEMENT'})
    ages=sorted(x['causal_sample_age_at_bracket_end_s'] for x in event_rows)
    return {'protocol':'P35_FORWARD_ONLY_OBSERVATION_TIMING','status':'REAL_SAME_SOURCE_MEASUREMENT_QA_NOT_CONTROLLER_EVIDENCE',
        'source_sha256':{'P34_archive':P34_ARCHIVE_SHA,'P34_event_ledger':P34_EVENT_SHA,
                         'signal_csv':SIGNAL_SHA,'volume_csv':VOLUME_SHA},
        'crossings':len(bracket),'signal_ids':len(heads),'signal_rows':sum(map(len,heads.values())),
        'matched_tolerance_sensitivity':sensitivity,
        'crossings_with_nearest_hindsight_sample_future':hindsight_future,
        'crossings_with_nearest_hindsight_sample_after_bracket':closest_future_after_bracket,
        'crossings_with_any_head_discordant_between_sample_bounds':crossing_with_discordant_head,
        'crossing_brackets_containing_signal_sample':straddled_sample_brackets,
        'signal_head_event_pairs_with_discordant_samples':discordant_head_pairs,
        'freshness_at_bracket_end':{str(v):{'causally_fresh_crossings':freshness_counts[v],
                                         'stale_crossings':len(bracket)-freshness_counts[v]} for v in FRESHNESS},
        'age_at_bracket_end_s':{'min':ages[0],'median':round(statistics.median(ages),6),'max':ages[-1]},
        'common_signal_gap':gaps,
        'crossings_overlapping_common_gap':sum(x['shared_gap_overlap'] for x in event_rows),
        'event_records':event_rows,
        'limits':['No independent traffic field truth: volume counts derive from the same tracking source',
                  'Neither 30-head sampled state nor 2015 OpenDRIVE static IDs establish the controlled lane',
                  'The nearest sampled signal state may be from the FUTURE of a crossing; it is hindsight only',
                  'Signal state cannot be assumed unchanged between two 1Hz samples',
                  'Crossing time is 50ms bracketed/estimated, not exact physical instant']}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--p34-zip',required=True,type=Path)
    p.add_argument('--signals',required=True,type=Path)
    p.add_argument('--volume',required=True,type=Path)
    p.add_argument('--out',required=True,type=Path)
    args=p.parse_args()
    args.out.write_text(json.dumps(analyse(args.p34_zip,args.signals,args.volume),ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')

if __name__ == '__main__':
    main()
