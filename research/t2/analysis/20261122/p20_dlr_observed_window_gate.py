"""Read-only DLR-UT 15-min externally measured trajectory / signal schema gate.

Source originals in Drive; not a model-to-field calibration or phase-code interpretation.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import median

EXPECTED={
 'trajectories':'6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50',
 'signals':'95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c',
}

def read(path, expected):
    if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
        raise ValueError('source SHA256 not equal to sealed Drive download')
    with path.open('r',encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f))

def describe(trajectories, signals):
    if not trajectories or not signals:raise ValueError('nonempty source required')
    for records in (trajectories,signals):
        if any(not r.get('timestamp') or not r.get('id') for r in records):
            raise ValueError('missing id or timestamp')
    def ts(s):return datetime.fromisoformat(s)
    observed={}
    for name,rows in (('trajectories',trajectories),('traffic_lights',signals)):
        by_id=defaultdict(list)
        for r in rows:
            by_id[r['id']].append(ts(r['timestamp']))
        intervals=[]
        for times in by_id.values():
            ordered=sorted(times)
            intervals.extend((b-a).total_seconds() for a,b in zip(ordered,ordered[1:]))
        ids_times={(r['id'],r['timestamp']) for r in rows}
        observed[name]={
            'rows':len(rows),'unique_ids':len(by_id),
            'duplicate_id_timestamp_rows':len(rows)-len(ids_times),
            'start_utc':min(ts(r['timestamp']) for r in rows).isoformat(),
            'end_utc':max(ts(r['timestamp']) for r in rows).isoformat(),
            'within_id_sample_interval_median_s':median(intervals) if intervals else None,
            'all_fields_nonmissing':all(all(v!='' for v in r.values()) for r in rows),
        }
    cars=[float(r['velocity_magnitude']) for r in trajectories if float(r['classifications_car'])>.5]
    observed['trajectories']['car_class_over_half_rows']=len(cars)
    observed['trajectories']['car_class_over_half_velocity_magnitude_median']=median(cars) if cars else None
    by_id=defaultdict(list)
    for r in signals:by_id[r['id']].append((ts(r['timestamp']),r['state']))
    transitions=0
    for id,values in by_id.items():
        seq=[v for t,v in sorted(values)]
        transitions+=sum(a!=b for a,b in zip(seq,seq[1:]))
    observed['traffic_lights']['state_code_histogram']=dict(sorted(Counter(r['state'] for r in signals).items(),key=lambda x:int(x[0])))
    observed['traffic_lights']['total_within_id_state_code_transitions']=transitions
    return {
        'protocol':'P20_DLR_UT_15MIN_SOURCE_TIMING_GATE',
        'status':'REAL_OBSERVATIONAL_DATA_SCHEMA_AUDIT_NOT_CALIBRATION',
        'source_window':'2023-09-24 23:30 to 23:45 UTC',
        'sources_sha256':EXPECTED,
        'datasets':observed,
        'interpretation':'Signal integer code meanings and trajectory lane/stopline mapping not verified; do not compare per-row velocity to model discharge headway.',
    }

def run(traj,signals):return describe(read(traj,EXPECTED['trajectories']),read(signals,EXPECTED['signals']))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('trajectories',type=Path);p.add_argument('signals',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();a.output.write_text(json.dumps(run(a.trajectories,a.signals),indent=2,sort_keys=True)+'\n',encoding='utf-8')
