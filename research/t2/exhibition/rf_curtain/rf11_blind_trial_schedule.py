"""RF11: reproducible BLIND experiment schedule for RF-CURTAIN.

Creates an operator-only ground-truth schedule and a separate analyst-facing
blank-label plan. These are future laboratory intentions, not measurements.
No radio hardware or real road access is used.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import secrets
from pathlib import Path

LABELS=('no_demand','free','pocket','downstream','both')
SESSIONS=('S1','S2','S3')
PLACEMENTS=('P1','P2')
TRAIN={('S1','P1'),('S2','P1')}
PRIMARY=('S3','P2')
RESERVE=('S1','P2')


def schedule(*,seed: int | None=None,reset_per_class: int=10):
    if seed is None:
        seed=secrets.randbits(128)
    if type(seed) is not int or seed<0:
        raise ValueError('seed must be nonnegative integer')
    if type(reset_per_class) is not int or reset_per_class<10:
        raise ValueError('minimum ten independent resets per class')
    out=[]
    for session in SESSIONS:
        for placement in PLACEMENTS:
            conditions=[label for label in LABELS for _ in range(reset_per_class)]
            # Per-cell deterministic permutation independent of any CSI signal.
            r=random.Random(f'RF11-v1:{seed}:{session}:{placement}')
            r.shuffle(conditions)
            for index,label in enumerate(conditions,1):
                trial_id=f'{session}_{placement}_{index:03d}'
                if (session,placement) in TRAIN:
                    partition='train'
                elif (session,placement)==PRIMARY:
                    partition='primary_blind_holdout'
                elif (session,placement)==RESERVE:
                    partition='sealed_unused_reserve'
                else:
                    partition='secondary_holdout'
                out.append(dict(trial_id=trial_id,session_id=session,
                   placement_id=placement,reset_index=index,partition=partition,
                   label=label,ground_truth_source='manual_model_state',
                   trial_origin='planned_not_measured'))
    assert len(out)==len(SESSIONS)*len(PLACEMENTS)*len(LABELS)*reset_per_class
    assert len({r['trial_id'] for r in out})==len(out)
    return out


def export(rows,path,*,operator:bool):
    fields=('trial_id','session_id','placement_id','reset_index','partition')
    if operator:
        fields+=('label','ground_truth_source','trial_origin')
    with Path(path).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore')
        w.writeheader();w.writerows(rows)


def manifest_receipt(rows):
    # A digest of the fixed order including hidden labels. Public digest can be
    # compared to operator schedule *without* leaking exact trial labels.
    encoded=json.dumps(rows,sort_keys=True,ensure_ascii=False,
                       separators=(',',':')).encode('utf-8')
    counts={p:sum(r['partition']==p for r in rows) for p in
            ('train','primary_blind_holdout','secondary_holdout','sealed_unused_reserve')}
    return dict(status='PLANNED_TRIAL_SCHEDULE_NOT_MEASURED',
                schedule_sha256=hashlib.sha256(encoded).hexdigest(),
                total_trials=len(rows),n_per_cell=len(rows)//(len(SESSIONS)*len(PLACEMENTS)),
                partition_counts=counts,
                warning='Never call this a measured dataset or train on sealed cells.')


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument('--outdir',required=True)
    p.add_argument('--seed',type=int,default=None,
                   help='DEMO/REPRO ONLY; never use a published seed for a blinded experiment')
    p.add_argument('--resets',type=int,default=10)
    a=p.parse_args(argv)
    directory=Path(a.outdir);directory.mkdir(parents=True,exist_ok=True)
    rows=schedule(seed=a.seed,reset_per_class=a.resets)
    export(rows,directory/'operator_only_truth_schedule.csv',operator=True)
    export(rows,directory/'analyst_blind_schedule.csv',operator=False)
    rec=manifest_receipt(rows)
    (directory/'schedule_integrity.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps(rec,ensure_ascii=False))
    print('OPERATOR: keep truth CSV PRIVATE; do not publish seed/labels or '+
          'share the operator directory with analysts.')

if __name__=='__main__':main()
