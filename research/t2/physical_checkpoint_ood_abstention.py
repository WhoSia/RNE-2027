"""PHYS-09 label-free training-support abstention, prespecified seeds 56..71.

Test against separate traffic regimes without using their outcomes in
policy training. This is a synthetic study, NOT field-safe traffic control.
"""
import argparse
import hashlib
import json
import math
import random
from itertools import product
from pathlib import Path
from dual_lane_v11 import run, checkpoint_observation
from spatial_v10 import arrivals
from physical_checkpoint_delay_and_shift import make_config, decision, INTERVENTION
from physical_checkpoint_observation_ablation import features
from physical_transfer_screen import score

SEEDS=tuple(range(56,72))
REGIMES=(('uniform_baseline',1800,.5),('uniform_lowturn',1350,.3))
LEVELS=('counts','positions')
QUANTILE=.95


def squared_distance(a,b):
    return sum((x-y)**2 for x,y in zip(a,b))


def training_radii(train):
    radii={}
    for level in LEVELS:
        vectors=[features(row,level) for row in train]
        ds=[min(squared_distance(vectors[i],vectors[j])
                for j in range(len(train)) if train[j]['seed']!=row['seed'])
            for i,row in enumerate(train)]
        ds.sort()
        radii[level]=ds[math.ceil(QUANTILE*len(ds))-1]
    return radii


def is_supported(train,test,level,radius):
    vector=features(test,level)
    return min(squared_distance(vector,features(t,level)) for t in train)<=radius


def evaluate(train):
    if len(train)!=144 or {r['seed'] for r in train}!=set(range(8)):
        raise ValueError('expected seeds0..7, 144 rows')
    radii=training_radii(train)
    outputs={}
    for label,demand,left in REGIMES:
        cases=[]
        for seed,cap,pocket,share in product(SEEDS,(2,4,8),(14.,28.,70.),(0.,.5)):
            c=make_config(seed,cap,pocket,share,demand,left,'uniform')
            tape=arrivals(c.base)
            cp=run(c,tape,checkpoint_at=84)
            control=run(c,tape,resume_from=cp)
            if control!=run(c,tape):
                raise AssertionError(('restart mismatch',label,seed,cap,pocket,share))
            treat=run(c,tape,resume_from=cp,phase_overrides=INTERVENTION)
            for result in (control,treat):
                if result['generated'] != result['remaining'] + result['network_out_S'] + result['network_out_L']:
                    raise AssertionError(('conservation',label,seed,cap,pocket,share))
            observed=checkpoint_observation(cp)
            row={'seed':seed,'capacity':cap,'pocket_m':pocket,'b_share':share,
                 'delta_p60':score(treat,60)-score(control,60)}
            subject=dict(row,decision_observation=observed)
            row['always_intervene']=True
            for level in LEVELS:
                row[level]=decision(train,row,observed,level)
                row[level+'_support']=is_supported(train,subject,level,radii[level])
                row[level+'_abstain']=row[level] and row[level+'_support']
            cases.append(row)
        if len(cases)!=288:raise AssertionError('wrong evaluation grid')
        oracle=sum(max(-r['delta_p60'],0) for r in cases)
        policies={}
        for name in ('always_intervene','counts','positions','counts_abstain','positions_abstain'):
            saved=sum(-r['delta_p60'] if r[name] else 0 for r in cases)
            policies[name]={'total_saved':saved,'regret':oracle-saved,
                            'treated':sum(r[name] for r in cases),
                            'seed_savings':{str(seed):sum(-r['delta_p60'] if r[name] else 0
                                           for r in cases if r['seed']==seed) for seed in SEEDS}}
        for level in LEVELS:
            policies[level+'_abstain']['out_of_support']=sum(not r[level+'_support'] for r in cases)
            policies[level+'_abstain']['blocked_harmful_treatments']=sum(
                r[level] and not r[level+'_support'] and r['delta_p60']>0 for r in cases)
            policies[level+'_abstain']['blocked_beneficial_treatments']=sum(
                r[level] and not r[level+'_support'] and r['delta_p60']<0 for r in cases)
        comparison={}
        for level in LEVELS:
            by_seed1=policies[level]['seed_savings'];by_seed2=policies[level+'_abstain']['seed_savings']
            gains=[(by_seed2[str(seed)]-by_seed1[str(seed)])/18 for seed in SEEDS]
            rng=random.Random(901000+(0 if level=='counts' else 1)+(0 if label=='uniform_baseline' else 9))
            bs=sorted(sum(rng.choices(gains,k=16))/16 for _ in range(10000))
            comparison[level]={'avg_per_case_abstention_advantage':sum(gains)/16,
                               'seed_block_95pct':[bs[249],bs[9749]],
                               'positive_seed_blocks':sum(x>0 for x in gains),
                               'negative_seed_blocks':sum(x<0 for x in gains)}
        outputs[label]={'demand_vph':demand,'left_fraction':left,
                        'oracle_saved':oracle,'summary':policies,
                        'abstention_vs_unconditional':comparison,
                        'cases':cases}
    return {'status':'SYNTHETIC_UNCALIBRATED','protocol':'PHYS-09 prospective label-free OOD abstention',
            'train_seed_span':[0,7],'test_seed_span':[56,71],
            'support_quantile':QUANTILE,'squared_distance_radii':radii,
            'regimes':outputs}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('training_json',type=Path)
    ap.add_argument('output_json',type=Path)
    args=ap.parse_args()
    train=json.loads(args.training_json.read_text(encoding='utf-8'))['pairs']
    result=evaluate(train)
    blob=(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    args.output_json.write_bytes(blob)
    print('SHA-256',hashlib.sha256(blob).hexdigest())
    print('train-support radii',result['squared_distance_radii'])
    for name,v in result['regimes'].items():
        print(name,'oracle',v['oracle_saved'])
        for policy,r in v['summary'].items():
            print(' ',policy,'saved',r['total_saved'],'regret',r['regret'], 'treated',r['treated'], 'OOD',r.get('out_of_support'))
