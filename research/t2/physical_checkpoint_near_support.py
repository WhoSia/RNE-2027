"""PHYS-10: pretrained support veto under mild demand shift & stale/occluded sensors.

Exact 8 previously unused seeds 72..79; four single-variable shifts.
Predeclared PHYS_10_NEAR_SUPPORT_SHIFT_AND_TELEMETRY_PREREG.md.
Synthetic policy experiment; no human road-control safety claim.
"""
import argparse
import hashlib
import json
import random
from copy import deepcopy
from itertools import product
from pathlib import Path

from dual_lane_v11 import run, checkpoint_observation
from spatial_v10 import arrivals
from physical_transfer_screen import score
from physical_checkpoint_delay_and_shift import make_config, INTERVENTION
from physical_checkpoint_observation_ablation import predict, features
from physical_checkpoint_ood_abstention import training_radii, squared_distance

TEST_SEEDS=tuple(range(72,80))
REGIMES=(('left45',1800,.45),('left55',1800,.55),
         ('demand1650',1650,.5),('demand1950',1950,.5))
SCENARIOS=('exact','stale12','occluded')
FEATURES=('counts','positions')


def omit_upstream_a_segment(observation):
    """Drop ten contiguous A cells and consistently decrement the A count."""
    obs=deepcopy(observation)
    original=tuple(obs['approach_A_positions'])
    remaining=[x for x in original if x > -11]
    missing=len(original)-len(remaining)
    obs['approach_A_positions']=tuple(remaining)
    obs['approach_A']-=missing
    if obs['approach_A']!=len(remaining) or obs['approach_A']<0:
        raise AssertionError('occlusion corrupted internal count consistency')
    return obs


def support_distance(train,sample,level):
    point=features(sample,level)
    return min(squared_distance(point,features(other,level)) for other in train)


def policy_outputs(train,geometry,observation,radii):
    """No outcome or future data passed to decision logic."""
    sample=dict(geometry,decision_observation=observation)
    out={}
    for level in FEATURES:
        estimate=predict(train,sample,level,k=5)
        distance=support_distance(train,sample,level)
        in_support=distance<=radii[level]
        learned=estimate<0
        out[level]={'predicted_delta':estimate,'distance':distance,
                    'in_support':in_support,'learned_action':learned,
                    'vetoed_action':learned and in_support}
    return out


def summary(rows,scenario,level):
    key=lambda r:r['observations'][scenario][level]
    oracle=sum(max(-r['delta_p60'],0) for r in rows)
    def savings(policy):
        return sum(-r['delta_p60'] for r in rows if policy(r))
    unconditional=savings(lambda r:key(r)['learned_action'])
    veto=savings(lambda r:key(r)['vetoed_action'])
    counts={
        'in_support':sum(key(r)['in_support'] for r in rows),
        'out_of_support':sum(not key(r)['in_support'] for r in rows),
        'unconditional_treat':sum(key(r)['learned_action'] for r in rows),
        'veto_treat':sum(key(r)['vetoed_action'] for r in rows),
        'harmful_admitted':sum(key(r)['vetoed_action'] and r['delta_p60']>0 for r in rows),
        'beneficial_admitted':sum(key(r)['vetoed_action'] and r['delta_p60']<0 for r in rows),
        'blocked_harmful':sum(key(r)['learned_action'] and not key(r)['in_support'] and r['delta_p60']>0 for r in rows),
        'blocked_beneficial':sum(key(r)['learned_action'] and not key(r)['in_support'] and r['delta_p60']<0 for r in rows),
        'unconditional_savings':unconditional,'veto_savings':veto,
        'veto_regret':oracle-veto,'oracle_savings':oracle}
    seed_diffs=[sum((-r['delta_p60'] if key(r)['vetoed_action'] else 0)-
                    (-r['delta_p60'] if key(r)['learned_action'] else 0)
                    for r in rows if r['seed']==seed)/18 for seed in TEST_SEEDS]
    rng=random.Random(20261000+SCENARIOS.index(scenario)*37+FEATURES.index(level)*17+
                      sum(ord(ch) for ch in rows[0]['regime']))
    draws=sorted(sum(rng.choices(seed_diffs,k=8))/8 for _ in range(10000))
    counts['veto_advantage_mean_per_pair']=sum(seed_diffs)/8
    counts['veto_advantage_seed_bootstrap_95pct']=[draws[249],draws[9749]]
    counts['seed_positive_advantage']=sum(x>0 for x in seed_diffs)
    counts['seed_negative_advantage']=sum(x<0 for x in seed_diffs)
    return counts


def experiment(training):
    if len(training)!=144 or {r['seed'] for r in training}!=set(range(8)):
        raise ValueError('requires 144 PHYS-04 training cases from seeds 0..7')
    radii=training_radii(training)
    payload={}
    for regime,demand,left in REGIMES:
        rows=[]
        for seed,capacity,pocket,share in product(TEST_SEEDS,(2,4,8),(14.,28.,70.),(0.,.5)):
            c=make_config(seed,capacity,pocket,share,demand,left,'uniform')
            tape=arrivals(c.base)
            cp=run(c,tape,checkpoint_at=84)
            baseline=run(c,tape,resume_from=cp)
            if baseline!=run(c,tape):
                raise AssertionError(('checkpoint replay',regime,seed,capacity,pocket,share))
            treated=run(c,tape,resume_from=cp,phase_overrides=INTERVENTION)
            for result in (baseline,treated):
                if result['generated']!=result['remaining']+result['network_out_S']+result['network_out_L']:
                    raise AssertionError('conservation')
            now=checkpoint_observation(cp)
            stale=checkpoint_observation(run(c,tape,checkpoint_at=72))
            occluded=omit_upstream_a_segment(now)
            if stale['decision_tick']!=72 or now['decision_tick']!=84:
                raise AssertionError('observation time leakage')
            geometry={'seed':seed,'capacity':capacity,'pocket_m':pocket,'b_share':share}
            decisions={name:policy_outputs(training,geometry,obs,radii)
                       for name,obs in (('exact',now),('stale12',stale),('occluded',occluded))}
            rows.append(dict(**geometry,regime=regime,
                             delta_p60=score(treated,60)-score(baseline,60),
                             observations=decisions,
                             observation_counts={'t84_A':now['approach_A'],
                                                 't72_A':stale['approach_A'],
                                                 'occluded_A':occluded['approach_A']}))
        if len(rows)!=144:raise AssertionError('scenario count')
        payload[regime]={'demand_vph':demand,'left_fraction':left,
                         'always_treat_saved':-sum(r['delta_p60'] for r in rows),
                         'oracle_saved':sum(max(-r['delta_p60'],0) for r in rows),
                         'summaries':{scenario:{level:summary(rows,scenario,level)
                                                for level in FEATURES}
                                      for scenario in SCENARIOS},
                         'paired_cases':rows}
    return {'status':'SYNTHETIC_UNCALIBRATED','protocol':'PHYS-10 near-support and telemetry loss',
            'train_seeds':[0,7],'test_seeds':[72,79],
            'support_radii':radii,'regimes':payload}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('training_json',type=Path)
    ap.add_argument('output_json',type=Path)
    args=ap.parse_args()
    cases=json.loads(args.training_json.read_text(encoding='utf-8'))['pairs']
    result=experiment(cases)
    data=(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    args.output_json.write_bytes(data)
    print('SHA256',hashlib.sha256(data).hexdigest())
    for key,regime in result['regimes'].items():
        print(key,'always',regime['always_treat_saved'],'oracle',regime['oracle_saved'])
        for scenario in SCENARIOS:
            for level in FEATURES:
                r=regime['summaries'][scenario][level]
                print(' ',scenario,level,'OOD',r['out_of_support'],'admitted_harm',r['harmful_admitted'],
                      'loss',r['blocked_beneficial'],'saved',r['veto_savings'],
                      'unconditional',r['unconditional_savings'])
