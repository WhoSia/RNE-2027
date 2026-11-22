"""Independent stdlib reference on frozen DLR raw files; verifies Go P33 *measurement*.

This does not estimate traffic phase onset, lane routing, or real policy effects.
Python here is a parity oracle for an independent Go producer, NOT a replacement Go runtime.
"""
import argparse
import csv
import hashlib
import json
import math
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

SIGNAL_SHA = "95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c"
TRAJ_SHA = "6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50"


def audit(go_result: dict, signals: Path, trajectories: Path) -> dict:
    assert hashlib.sha256(signals.read_bytes()).hexdigest() == SIGNAL_SHA
    assert hashlib.sha256(trajectories.read_bytes()).hexdigest() == TRAJ_SHA
    assert go_result['sha256'] == {'signals': SIGNAL_SHA, 'trajectories': TRAJ_SHA}
    rows = Counter()
    prev = {}
    snapshots = Counter()
    codes = Counter()
    gaps = defaultdict(lambda: {'heads': set(), 'changed': set()})
    green_runs = []
    active_green_run = defaultdict(int)
    for row in csv.DictReader(signals.open(newline='')):
        ident, state = int(row['id']), int(row['state'])
        stamp = datetime.fromisoformat(row['timestamp'])
        stampstr = stamp.isoformat(timespec='microseconds')
        snapshots[stampstr] += 1
        rows[ident] += 1
        codes[str(state)] += 1
        if ident in prev:
            prior_time, prior_state = prev[ident]
            gap = (stamp - prior_time).total_seconds()
            assert gap > 0
            if state != prior_state:
                go_changes = 1
            else:
                go_changes = 0
            if gap > 1.5:
                key = (prior_time.isoformat(timespec='microseconds'), stampstr, int(round(gap * 1000)))
                gaps[key]['heads'].add(ident)
                if go_changes:
                    gaps[key]['changed'].add(ident)
                if active_green_run[ident]:
                    green_runs.append(active_green_run[ident]);active_green_run[ident] = 0
        else:
            go_changes = 0
        if state in (5,6):
            active_green_run[ident] += 1
        else:
            if active_green_run[ident]:
                green_runs.append(active_green_run[ident]);active_green_run[ident] = 0
        prev[ident] = (stamp, state)
    green_runs += [x for x in active_green_run.values() if x]
    gs = go_result['signals']
    assert gs['rows'] == sum(rows.values()) == 26970
    assert gs['ids'] == len(rows) == 30
    assert gs['code_counts'] == dict(codes)
    assert gs['distinct_sample_timestamps'] == len(snapshots) == 899
    assert gs['min_heads_per_timestamp'] == min(snapshots.values()) == 30
    assert gs['max_heads_per_timestamp'] == max(snapshots.values()) == 30
    assert gs['green_run_length_samples_sorted'] == sorted(green_runs)
    assert gs['sample_gaps_gt_1500ms'] == sum(len(v['heads']) for v in gaps.values()) == 30
    assert len(gaps) == len(gs['shared_timestamp_gaps']) == 1
    (start, end, dtms), group = next(iter(gaps.items()))
    g = gs['shared_timestamp_gaps'][0]
    assert g['gap_ms'] == dtms == 2004
    assert g['affected_signal_heads'] == len(group['heads']) == 30
    assert g['changed_state_signal_ids_across_gap'] == sorted(group['changed']) == [12,20,21]
    assert datetime.fromisoformat(g['last_observed_utc']) == datetime.fromisoformat(start)
    assert datetime.fromisoformat(g['next_observed_utc']) == datetime.fromisoformat(end)

    trajectories_rows = 0
    interp = 0
    traj_prev = {}
    traj_intervals = []
    fast_intervals = 0
    speed_01 = 0
    speed_05 = 0
    class_changes = 0
    prior_class = {}
    track_counts = Counter()
    for row in csv.DictReader(trajectories.open(newline='')):
        ident,stamp=int(row['id']),datetime.fromisoformat(row['timestamp'])
        trajectories_rows += 1
        track_counts[ident] += 1
        interp += row['interpolated'].lower() == 'true'
        vec=math.hypot(float(row['velocity_easting']),float(row['velocity_northing']))
        diff=abs(vec-float(row['velocity_magnitude']))
        speed_01 += diff > .1
        speed_05 += diff > .5
        classes=['pedestrian','bicycle','motorbike','car','van','truck']
        best=max(classes,key=lambda k:float(row['classifications_'+k]))
        if ident in prior_class and best!=prior_class[ident]:class_changes+=1
        prior_class[ident]=best
        if ident in traj_prev:
            dt=(stamp-traj_prev[ident]).total_seconds()
            assert dt > 0
            fast_intervals += dt > .1
            traj_intervals.append(round(dt * 1000))
        traj_prev[ident]=stamp
    gt=go_result['trajectories']
    assert gt['rows'] == trajectories_rows == 8624
    assert gt['ids'] == len(track_counts) == 37
    assert gt['interpolated_samples'] == interp == 116
    assert gt['gaps_gt_100ms'] == fast_intervals == 0
    assert gt['median_per_id_inter_sample_ms'] == statistics.median(traj_intervals) == 50
    assert gt['speed_component_disagreements_gt_0_1_mps'] == speed_01 == 0
    assert gt['speed_component_disagreements_gt_0_5_mps'] == speed_05 == 0
    assert gt['observed_top_class_changes'] == class_changes == 0
    return {'cross_language':'Go producer / independent Python stdlib parity','matched_fields':18,
            'signal_timestamp_groups':len(snapshots),'shared_gap_changed_heads':[12,20,21],
            'trajectory_interpolated_rows':interp,'status':'PASS'}

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('go_json',type=Path)
    p.add_argument('signals',type=Path)
    p.add_argument('trajectories',type=Path)
    a=p.parse_args()
    print(json.dumps(audit(json.loads(a.go_json.read_text()),a.signals,a.trajectories),sort_keys=True,ensure_ascii=False))
