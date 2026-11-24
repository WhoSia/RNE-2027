"""RF17: label-free RF10 packet-window bridge to RF16 prediction.

Only offline authorized first-party input. No acquisition, truth access,
or physical validation. Shared RF10 parser and RF16 prediction are reused.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
import math
import statistics
from pathlib import Path

PLAN = ('trial_id','session_id','placement_id','reset_index','partition')
FEATURES = ('rssi_1_dbm','rssi_2_dbm','csi_1_amp_dispersion','csi_2_amp_dispersion')
WIRE = ('trial_id','session_id','placement_id','trial_origin','quality') + FEATURES
WINDOW = ('trial_id','session_id','placement_id','trial_origin','link_id','start_us','stop_us')
ORIGINS = {'synthetic_test_fixture','measured_authorized_lab'}
TRAIN = {('S1','P1'),('S2','P1')}
RESERVE = ('S1','P2')
CELLS = {(s,p) for s in ('S1','S2','S3') for p in ('P1','P2')}


def read_exact(path, fields):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        if len(reader.fieldnames or [])!=len(fields) or set(reader.fieldnames or [])!=set(fields):
            raise ValueError('unexpected CSV schema')
        rows=list(reader)
    if any(set(r)!=set(fields) or any(v is None for v in r.values()) for r in rows):
        raise ValueError('malformed CSV row')
    return rows


def testing_plan(plan):
    expected={}; seen=set()
    for r in plan:
        if set(r)!=set(PLAN) or not r['trial_id'] or r['trial_id'] in seen:
            raise ValueError('invalid or duplicate plan row')
        seen.add(r['trial_id'])
        cell=r['session_id'],r['placement_id']
        if cell not in CELLS:
            raise ValueError('unknown cell')
        partition=('train' if cell in TRAIN else 'sealed_unused_reserve' if cell==RESERVE else
                   'primary_blind_holdout' if cell==('S3','P2') else 'secondary_holdout')
        if r['partition']!=partition:
            raise ValueError('plan partition mismatch')
        if cell not in TRAIN and cell!=RESERVE:
            expected[r['trial_id']]=cell
    if not expected:
        raise ValueError('empty holdout')
    return expected


def read_frozen_plan(path, expected_sha256):
    """Verify a separately frozen PUBLIC plan before interpreting its rows."""
    raw=Path(path).read_bytes()
    if not isinstance(expected_sha256,str) or hashlib.sha256(raw).hexdigest()!=expected_sha256:
        raise ValueError('public plan digest mismatch')
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig'),newline=''))
    if len(reader.fieldnames or [])!=len(PLAN) or set(reader.fieldnames or [])!=set(PLAN):
        raise ValueError('unexpected plan schema')
    plan=list(reader)
    if any(set(r)!=set(PLAN) or any(v is None for v in r.values()) for r in plan):
        raise ValueError('malformed plan row')
    testing_plan(plan)
    indices={cell:[] for cell in CELLS}
    for r in plan:
        index=int(r['reset_index'])
        cell=r['session_id'],r['placement_id']
        if index<=0 or r['trial_id']!=f'{cell[0]}_{cell[1]}_{index:03d}':
            raise ValueError('invalid reset identity')
        indices[cell].append(index)
    sizes={len(v) for v in indices.values()}
    if len(sizes)!=1 or min(sizes)<50 or min(sizes)%5:
        raise ValueError('incomplete or unbalanced RF11 cells')
    if any(sorted(v)!=list(range(1,len(v)+1)) for v in indices.values()):
        raise ValueError('missing or duplicate reset index')
    return plan


def aggregate_holdout(plan, windows, packets, *, min_packets=2):
    """Neither the plan nor windows may contain truth or unknown columns.

    Both link windows are mandatory for each planned holdout ID. Missing
    packet coverage, including a completely empty packet stream, abstains.
    """
    if type(min_packets) is not int or min_packets<2 or set(packets)!={'1','2'}:
        raise ValueError('invalid coverage contract')
    expected=testing_plan(plan)
    grouped={}; origins=set(); spans={'1':[],'2':[]}
    for w in windows:
        if set(w)!=set(WINDOW) or any(not str(v).strip() for v in w.values()):
            raise ValueError('window schema must be label-free')
        tid=w['trial_id']; lid=w['link_id']; origin=w['trial_origin']
        if tid not in expected or expected[tid]!=(w['session_id'],w['placement_id']) or lid not in spans or origin not in ORIGINS:
            raise ValueError('window outside frozen holdout or invalid metadata')
        start,stop=int(w['start_us']),int(w['stop_us'])
        if start<0 or stop<=start:
            raise ValueError('invalid window bounds')
        key=(tid,lid)
        if key in grouped:
            raise ValueError('duplicate window')
        grouped[key]=(start,stop,origin); origins.add(origin); spans[lid].append((start,stop))
    if set(grouped)!={(tid,lid) for tid in expected for lid in ('1','2')} or len(origins)!=1:
        raise ValueError('planned denominator or provenance mismatch')
    for lid, intervals in spans.items():
        ordered=sorted(intervals)
        if any(a[1]>b[0] for a,b in zip(ordered,ordered[1:])):
            raise ValueError('overlapping trial windows')
        stream=packets[lid]
        if any(b['timestamp_us']<=a['timestamp_us'] for a,b in zip(stream,stream[1:])):
            raise ValueError('nonmonotone packet clock')
        if any(not math.isfinite(float(p[k])) for p in stream for k in ('rssi','mean_amplitude')):
            raise ValueError('nonfinite packet feature')
    result=[]
    for tid,(session,placement) in expected.items():
        row=dict(trial_id=tid,session_id=session,placement_id=placement,trial_origin=next(iter(origins)),quality='ok')
        row.update(dict.fromkeys(FEATURES,''))
        for lid in ('1','2'):
            start,stop,_=grouped[tid,lid]
            samples=[p for p in packets[lid] if start<=p['timestamp_us']<stop]
            if len(samples)<min_packets:
                row['quality']='missing'
                continue
            row[f'rssi_{lid}_dbm']=round(statistics.fmean(p['rssi'] for p in samples),8)
            row[f'csi_{lid}_amp_dispersion']=round(statistics.pstdev(p['mean_amplitude'] for p in samples),8)
        result.append(row)
    return result


def export_features(rows,path):
    if any(set(r)!=set(WIRE) for r in rows):
        raise ValueError('feature export must be label-free')
    with Path(path).open('x',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=WIRE)
        writer.writeheader(); writer.writerows(rows)


def predict_files(plan_path,train_path,features_path,prediction_path,*,expected_plan_sha256):
    from rf16_blind_predict import predict_blind
    from rf_pilot_evaluator import REQUIRED
    plan=read_frozen_plan(plan_path,expected_plan_sha256)
    train=read_exact(train_path,REQUIRED)
    features=read_exact(features_path,WIRE)
    result=predict_blind(plan,train,features)
    with Path(prediction_path).open('x',encoding='utf-8') as f:
        json.dump(result,f,sort_keys=True,indent=2); f.write('\n')
    return result


def bridge_files(plan_path,windows_path,link1,link2,output_path,*,expected_plan_sha256,authorized_lab=False,invalid_policy='reject'):
    from rf10_esp_csi_trial_bridge import load_owned_csv
    plan=read_frozen_plan(plan_path,expected_plan_sha256)
    windows=read_exact(windows_path,WINDOW)
    streams={}
    for lid,path in [('1',link1),('2',link2)]:
        # None is an explicit missing link; never turn a malformed CSV into missingness.
        if not authorized_lab:
            raise PermissionError('authorized first-party offline input only')
        streams[lid]=[] if path is None else load_owned_csv(path,lab_authorized=True,invalid_policy=invalid_policy)
    rows=aggregate_holdout(plan,windows,streams)
    export_features(rows,output_path)
    return rows
