"""P21: byte-locked DLR-UT observed signal runs and low-speed proxy.

This is NOT a stopline/headway comparison, green-phase decoding or SUMO run.
"""
import csv, hashlib, json
from collections import Counter,defaultdict
from datetime import datetime
from pathlib import Path
from statistics import median

SHA_TRAJ='6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50'
SHA_SIGNAL='95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c'
CLASSES=('pedestrian','bicycle','motorbike','car','van','truck')

def read_raw(path,sha):
    if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=sha:
        raise ValueError('source hash mismatch')
    with Path(path).open(encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f))

def ts(s):
    d=datetime.fromisoformat(s)
    if d.tzinfo is None:raise ValueError('timezone missing')
    return d

def audit(trajectories,signals,stationary_speed=.5,max_gap=.2):
    if not trajectories or not signals or stationary_speed<0 or max_gap<=0:
        raise ValueError('invalid data or thresholds')
    t=defaultdict(list);s=defaultdict(list)
    for r in trajectories:t[r['id']].append((ts(r['timestamp']),r))
    for r in signals:s[r['id']].append((ts(r['timestamp']),r))
    runs=[];transitions=0
    for sid,rows in sorted(s.items()):
        rows=sorted(rows)
        if len({a for a,_ in rows})!=len(rows):raise ValueError('repeated signal timestamp')
        cur=None
        for instant,r in rows:
            if cur is None or cur['code']!=r['state']:
                if cur is not None:cur['right_censored']=False;transitions+=1
                cur={'id':sid,'code':r['state'],'first':instant.isoformat(),
                     'last':instant.isoformat(),'samples':0,
                     'left_censored':cur is None,'right_censored':True}
                runs.append(cur)
            cur['samples']+=1;cur['last']=instant.isoformat()
    modal=Counter(); stationary_ids=set(); low_intervals=0;seconds=0.;gaps=0
    for oid,rows in sorted(t.items()):
        rows=sorted(rows)
        scores=Counter(max(CLASSES,key=lambda cl:float(r['classifications_'+cl])) for _,r in rows)
        modal[scores.most_common(1)[0][0]]+=1
        for (ta,a),(tb,b) in zip(rows,rows[1:]):
            dt=(tb-ta).total_seconds()
            if dt<=0:raise ValueError('nonpositive object time step')
            if dt>max_gap:gaps+=1;continue
            if float(a['velocity_magnitude'])<=stationary_speed and float(b['velocity_magnitude'])<=stationary_speed:
                stationary_ids.add(oid);low_intervals+=1;seconds+=dt
    for r in runs:
        r['observed_span_s']=round((ts(r['last'])-ts(r['first'])).total_seconds(),6)
    by_code=defaultdict(list)
    for r in runs:by_code[r['code']].append(r['observed_span_s'])
    return {'status':'REAL_DLR_OBSERVATION_DESCRIPTION_ONLY',
       'source_window_utc':'2023-09-24 23:30–23:45 UTC',
       'tracked_object_ids':len(t),'signal_ids':len(s),
       'signal_runs':len(runs),'signal_code_changes':transitions,
       'code_run_median_observed_span_s':{code:median(vals) for code,vals in sorted(by_code.items())},
       'object_modal_classes':dict(sorted(modal.items())),
       'objects_with_adjacent_low_speed':len(stationary_ids),
       'low_speed_adjacent_intervals':low_intervals,
       'low_speed_observed_seconds':round(seconds,3),
       'large_trajectory_gaps':gaps,'speed_threshold':stationary_speed,'max_gap_s':max_gap,
       'gates':{'codebook_interpreted':False,'signal_lane_map':False,
           'stopline_crossing_validated':False,'exact_dwell_estimated':False,
           'queuing_identified':False,'sumo_external_validation':False},
       'signal_runs_detail':runs}

def execute(trajectory_path,signal_path):
    out=audit(read_raw(trajectory_path,SHA_TRAJ),read_raw(signal_path,SHA_SIGNAL))
    out['source_sha256']={'trajectories':SHA_TRAJ,'signals':SHA_SIGNAL}
    return out

if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser()
    a.add_argument('trajectory_path',type=Path);a.add_argument('signal_path',type=Path);a.add_argument('output',type=Path)
    x=a.parse_args()
    x.output.write_text(json.dumps(execute(x.trajectory_path,x.signal_path),sort_keys=True,indent=2)+'\n',encoding='utf-8')
