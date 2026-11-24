"""RF19: offline partitioned features; external truth custody still required."""
import csv
import math
import statistics
from collections import Counter
from pathlib import Path

WINDOW = ('trial_id','session_id','placement_id','trial_origin','link_id','start_us','stop_us')
FEATURES = ('rssi_1_dbm','rssi_2_dbm','csi_1_amp_dispersion','csi_2_amp_dispersion')
WIRE = ('trial_id','session_id','placement_id','trial_origin','quality') + FEATURES
TRUTH = ('trial_id','label','ground_truth_source')
LABELS = ('no_demand','free','pocket','downstream','both')
ORIGINS = {'synthetic_test_fixture','measured_authorized_lab'}
TRAIN = {('S1','P1'),('S2','P1')}
TEST = {('S2','P2'),('S3','P1'),('S3','P2')}


def expected(plan, partition):
    cells = TRAIN if partition == 'train' else TEST if partition == 'holdout' else None
    if cells is None:
        raise ValueError('invalid partition')
    ids = {}
    seen = set()
    for r in plan:
        tid = r['trial_id']; cell = (r['session_id'],r['placement_id'])
        if tid in seen:
            raise ValueError('duplicate plan ID')
        seen.add(tid)
        if cell in cells:
            ids[tid] = cell
    if not ids or set(ids.values()) != cells:
        raise ValueError('incomplete partition')
    return ids


def domains(ids):
    return {(*cell,lid) for cell in ids.values() for lid in ('1','2')}


def aggregate(plan, windows, streams, partition, *, min_packets=2):
    ids = expected(plan,partition)
    if set(streams) != domains(ids) or type(min_packets) is not int or min_packets < 2:
        raise ValueError('invalid stream domains or packet minimum')
    bounds = {}; spans = {k:[] for k in streams}; origins = set()
    for w in windows:
        if set(w) != set(WINDOW):
            raise ValueError('window must be label-free')
        tid = w['trial_id']; cell = (w['session_id'],w['placement_id']); lid = w['link_id']
        key = (*cell,lid); origin = w['trial_origin']
        if ids.get(tid) != cell or key not in spans or origin not in ORIGINS:
            raise ValueError('window outside partition or invalid origin')
        start,stop = int(w['start_us']),int(w['stop_us'])
        if start < 0 or stop <= start or (tid,lid) in bounds:
            raise ValueError('invalid or duplicate window')
        bounds[tid,lid] = (start,stop); spans[key].append((start,stop)); origins.add(origin)
    if set(bounds) != {(tid,lid) for tid in ids for lid in ('1','2')} or len(origins) != 1:
        raise ValueError('partition denominator or provenance mismatch')
    for key,stream in streams.items():
        ordered = sorted(spans[key])
        if any(a[1] > b[0] for a,b in zip(ordered,ordered[1:])):
            raise ValueError('overlap within clock domain')
        times = [p['timestamp_us'] for p in stream]
        if any(type(t) is not int or t < 0 for t in times) or any(a >= b for a,b in zip(times,times[1:])):
            raise ValueError('invalid clock or reset inside domain')
        if any(not math.isfinite(float(p[k])) for p in stream for k in ('rssi','mean_amplitude')):
            raise ValueError('nonfinite packet feature')
    rows = []
    for tid,cell in ids.items():
        r = dict(trial_id=tid,session_id=cell[0],placement_id=cell[1],trial_origin=next(iter(origins)),quality='ok')
        r.update(dict.fromkeys(FEATURES,''))
        for lid in ('1','2'):
            lo,hi = bounds[tid,lid]
            samples = [p for p in streams[(*cell,lid)] if lo <= p['timestamp_us'] < hi]
            if len(samples) < min_packets:
                r['quality'] = 'missing'; continue
            r[f'rssi_{lid}_dbm'] = round(statistics.fmean(p['rssi'] for p in samples),8)
            r[f'csi_{lid}_amp_dispersion'] = round(statistics.pstdev(p['mean_amplitude'] for p in samples),8)
        rows.append(r)
    return rows


def join_training(plan, features, truth):
    ids = expected(plan,'train')
    f = {r['trial_id']:r for r in features}; t = {r['trial_id']:r for r in truth}
    if len(f) != len(features) or len(t) != len(truth) or set(f) != set(ids) or set(t) != set(ids):
        raise ValueError('training denominator mismatch')
    counts = {cell:Counter() for cell in TRAIN}
    result = []
    for tid,cell in ids.items():
        r = f[tid]; label = t[tid]
        if set(r) != set(WIRE) or (r['session_id'],r['placement_id']) != cell:
            raise ValueError('invalid training features')
        if set(label) != set(TRUTH) or label['label'] not in LABELS or label['ground_truth_source'] != 'manual_model_state':
            raise ValueError('invalid private training truth')
        counts[cell][label['label']] += 1
        result.append(dict(r,label=label['label'],ground_truth_source=label['ground_truth_source']))
    for c in counts.values():
        if set(c) != set(LABELS) or len(set(c.values())) != 1 or min(c.values()) < 10:
            raise ValueError('unbalanced training labels')
    return result


def load_streams(raw_paths, ids, *, authorized_lab, loader, invalid_policy='reject'):
    if not authorized_lab:
        raise PermissionError('authorized first-party offline input only')
    if set(raw_paths) != domains(ids):
        raise ValueError('raw domain mismatch')
    paths = [Path(p).resolve() for p in raw_paths.values() if p is not None]
    if len(paths) != len(set(paths)):
        raise ValueError('raw path reused across domains')
    return {k:[] if p is None else loader(p,lab_authorized=True,invalid_policy=invalid_policy) for k,p in raw_paths.items()}


def build_files(plan_path, windows_path, raw_paths, output_path, *, partition, expected_plan_sha256, authorized_lab=False, truth_path=None, invalid_policy='reject'):
    from rf17_feature_only_bridge import read_exact, read_frozen_plan
    from rf10_esp_csi_trial_bridge import load_owned_csv
    if (partition == 'train') != (truth_path is not None):
        raise ValueError('truth allowed only for training')
    plan = read_frozen_plan(plan_path,expected_plan_sha256)
    ids = expected(plan,partition)
    windows = read_exact(windows_path,WINDOW)
    streams = load_streams(raw_paths,ids,authorized_lab=authorized_lab,loader=load_owned_csv,invalid_policy=invalid_policy)
    rows = aggregate(plan,windows,streams,partition)
    fields = WIRE
    if partition == 'train':
        rows = join_training(plan,rows,read_exact(truth_path,TRUTH))
        from rf_pilot_evaluator import REQUIRED, validate
        validate(rows); fields = REQUIRED
    with Path(output_path).open('x',encoding='utf-8',newline='') as f:
        w = csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    return rows
