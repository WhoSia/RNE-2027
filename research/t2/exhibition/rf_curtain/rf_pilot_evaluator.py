"""Leakage-resistant trial-level RF sensing evaluator (NOT CSI acquisition).

Only evaluate independently reset authorized laboratory measurements. The
illustrative unit-test data are synthetic and cannot establish RF accuracy.
Train on P1 / sessions other than S3, test exclusively P2 / S3.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path

LABELS=('no_demand','free','pocket','downstream','both')
MODELS={
    'majority':(),
    'rssi_one':('rssi_1_dbm',),
    'rssi_both':('rssi_1_dbm','rssi_2_dbm'),
    'csi_both':('csi_1_amp_dispersion','csi_2_amp_dispersion'),
    'fused_exploratory':('rssi_1_dbm','rssi_2_dbm',
                         'csi_1_amp_dispersion','csi_2_amp_dispersion'),
}
REQUIRED=('trial_id','session_id','placement_id','trial_origin','label',
          'ground_truth_source','quality')+tuple(dict.fromkeys(
              field for fields in MODELS.values() for field in fields))


def read_trials(path: str | Path) -> list[dict]:
    with Path(path).open(newline='',encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames or any(x not in reader.fieldnames for x in REQUIRED):
            raise ValueError('CSV missing required columns')
        rows=list(reader)
    validate(rows)
    return rows


def validate(rows: list[dict]):
    if not rows:
        raise ValueError('no trial rows')
    ids=[]; origins=set()
    for row in rows:
        if any(k not in row for k in REQUIRED):
            raise ValueError('missing field')
        if any(not row[k].strip() for k in ('trial_id','session_id','placement_id',
                                           'label','trial_origin','ground_truth_source')):
            raise ValueError('missing trial metadata')
        if row['label'] not in LABELS:
            raise ValueError('unknown label')
        if row['quality'] not in ('ok','missing'):
            raise ValueError('invalid quality')
        if row['trial_origin'] not in ('measured_authorized_lab','synthetic_test_fixture'):
            raise ValueError('invalid trial origin')
        origins.add(row['trial_origin']);ids.append(row['trial_id'])
        if row['trial_origin']=='measured_authorized_lab' and row['ground_truth_source']!='manual_model_state':
            raise ValueError('real label requires independent manual ground truth')
        for field in REQUIRED[7:]:
            if row[field] not in ('',None):
                try: v=float(row[field])
                except (ValueError,TypeError): raise ValueError('non-numeric telemetry') from None
                if not math.isfinite(v): raise ValueError('nonfinite telemetry')
    if len(set(ids))!=len(ids):raise ValueError('duplicate trial_id')
    if len(origins)!=1:raise ValueError('mixed synthetic and real provenance')


def vector(row,fields):
    if row['quality']!='ok':return None
    try:
        if any(row[x] in ('',None) for x in fields):return None
        return tuple(float(row[x]) for x in fields)
    except (ValueError,TypeError,KeyError):return None


def fit_predict(train, test, fields):
    good=[(r,vector(r,fields)) for r in train]
    good=[(r,v) for r,v in good if v is not None]
    if {r['label'] for r,_ in good}!=set(LABELS):
        return ['abstain']*len(test),{'usable_training':len(good),'fit_possible':False}
    if not fields:
        counts=Counter(r['label'] for r,_ in good)
        majority=min(LABELS,key=lambda x:(-counts[x],LABELS.index(x)))
        return [majority if r['quality']=='ok' else 'abstain' for r in test],{
            'usable_training':len(good),'fit_possible':True}
    dims=len(fields)
    means=[sum(v[j] for _,v in good)/len(good) for j in range(dims)]
    scales=[max(math.sqrt(sum((v[j]-means[j])**2 for _,v in good)/len(good)),1e-9)
            for j in range(dims)]
    normalized=[(r,tuple((v[j]-means[j])/scales[j] for j in range(dims)))
                for r,v in good]
    centers={label:tuple(sum(v[j] for r,v in normalized if r['label']==label)/
                         sum(r['label']==label for r,_ in normalized)
                         for j in range(dims)) for label in LABELS}
    pred=[]
    for r in test:
        v=vector(r,fields)
        if v is None:
            pred.append('abstain');continue
        w=tuple((v[j]-means[j])/scales[j] for j in range(dims))
        pred.append(min(LABELS,key=lambda label:(
            sum((w[j]-centers[label][j])**2 for j in range(dims)),LABELS.index(label))))
    return pred,{'usable_training':len(good),'fit_possible':True}


def summarize(test, pred):
    confusion={actual:{p:0 for p in LABELS+('abstain',)} for actual in LABELS}
    for row,p in zip(test,pred):confusion[row['label']][p]+=1
    per_class={}
    for label in LABELS:
        tp=confusion[label][label]
        fn=sum(confusion[label].values())-tp
        fp=sum(confusion[other][label] for other in LABELS if other!=label)
        recall=tp/(tp+fn) if tp+fn else 0.
        precision=tp/(tp+fp) if tp+fp else 0.
        f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0.
        per_class[label]={'recall':recall,'precision':precision,'f1':f1,
                          'support':sum(confusion[label].values())}
    return {'test_n':len(test),'confusion':confusion,'per_class':per_class,
            'balanced_accuracy':sum(d['recall'] for d in per_class.values())/len(LABELS),
            'macro_f1':sum(d['f1'] for d in per_class.values())/len(LABELS),
            'abstain_rate':pred.count('abstain')/len(pred)}


def evaluate(rows):
    validate(rows)
    train=[r for r in rows if r['placement_id']=='P1' and r['session_id'] in ('S1','S2')]
    test=[r for r in rows if r['placement_id']=='P2' and r['session_id']=='S3']
    if not train or not test:raise ValueError('frozen train/test placement-session split absent')
    if {r['label'] for r in train}!=set(LABELS) or {r['label'] for r in test}!=set(LABELS):
        raise ValueError('a split lacks one or more prespecified labels')
    origin=rows[0]['trial_origin']
    reports={}
    for name,fields in MODELS.items():
        pred,fit=fit_predict(train,test,fields)
        reports[name]={**summarize(test,pred),**fit}
    n_per_label=Counter(r['label'] for r in test)
    counts_by_session={}
    for session in sorted({r['session_id'] for r in rows}):
        s=[r for r in rows if r['session_id']==session]
        counts_by_session[session]={'n':len(s),'valid_quality_rate':
                                    sum(r['quality']=='ok' for r in s)/len(s)}
    eligible=(len(train)>=100 and len(test)>=50 and
              all(n_per_label[x]>=10 for x in LABELS) and
              all(v['valid_quality_rate']>=.8 for v in counts_by_session.values()))
    csi=reports['csi_both'];rssi=max(reports['rssi_one']['macro_f1'],
                                    reports['rssi_both']['macro_f1'])
    passed=(eligible and csi['fit_possible'] and csi['macro_f1']>=.70 and
            min(csi['per_class'][x]['recall'] for x in LABELS)>=.50 and
            csi['macro_f1']-rssi>=.10)
    gate=('NOT_APPLICABLE_SYNTHETIC_FIXTURE' if origin=='synthetic_test_fixture' else
          ('INSUFFICIENT_DATA' if not eligible else ('PASS_PROVISIONAL_REQUIRES_SOURCE_AUDIT' if passed else 'FAIL')))
    return {'status':'SYNTHETIC_PIPELINE_TEST_NOT_RF_EVIDENCE' if
            origin=='synthetic_test_fixture' else 'LAB_TRIAL_ANALYSIS_REQUIRES_SOURCE_AUDIT',
            'evidence_origin':origin,'train_n':len(train),'test_n':len(test),
            'unused_n':len(rows)-len(train)-len(test),
            'per_session_quality':counts_by_session,'models':reports,
            'pilot_gate':gate,
            'note':'Cross-placement/session, five-label evaluation; no real controller or RF data is implied'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('trial_csv',type=Path)
    parser.add_argument('output_json',type=Path)
    args=parser.parse_args()
    args.output_json.write_text(json.dumps(evaluate(read_trials(args.trial_csv)),
                                          sort_keys=True,indent=2)+'\n',encoding='utf-8')
