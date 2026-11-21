"""PHYS-08 prospective 12s telemetry-freshness fallback; synthetic experiment.

Locked 2026-11-21 before inspecting seeds 40..55. All policies use a frozen
k=5 learner trained on seeds 0..7. Geometry fallback is NOT a safety guarantee.
Usage: PYTHONPATH=research/t2 python research/t2/physical_checkpoint_freshness_fallback.py TRAIN.json OUTPUT.json
"""
import argparse
import hashlib
import json
import random
from itertools import product
from pathlib import Path
from dual_lane_v11 import run, checkpoint_observation
from spatial_v10 import arrivals
from physical_checkpoint_delay_and_shift import (
    make_config, decision, INTERVENTION, DECISION_TICK)
from physical_transfer_screen import score

SEEDS = tuple(range(40,56))
DELAYS = (0,6,12,24)
FALLBACK_AGE_S = 12
REGIMES = (('uniform_baseline', 1800, .5), ('uniform_lowturn', 1350, .3))


def freshness_choice(age_s, measured_action, geometry_action, threshold_s=FALLBACK_AGE_S):
    """Choose a frozen heuristic based on telemetry age, never on outcomes."""
    if not isinstance(age_s, int) or age_s < 0 or not isinstance(threshold_s, int) or threshold_s < 1:
        raise ValueError('invalid telemetry age or threshold')
    return measured_action if age_s < threshold_s else geometry_action


def evaluate(train):
    if len(train) != 144 or {r['seed'] for r in train} != set(range(8)):
        raise ValueError('expected 144 training conditions, seeds 0..7')
    output = {}
    for label,demand,left in REGIMES:
        cases = []
        for seed,cap,pocket,share in product(SEEDS,(2,4,8),(14.,28.,70.),(0.,.5)):
            c=make_config(seed,cap,pocket,share,demand,left,'uniform')
            tape=arrivals(c.base)
            cp=run(c,tape,checkpoint_at=DECISION_TICK)
            baseline=run(c,tape,resume_from=cp)
            if baseline != run(c,tape):
                raise AssertionError(('resume mismatch',label,seed,cap,pocket,share))
            changed=run(c,tape,resume_from=cp,phase_overrides=INTERVENTION)
            for result in (baseline,changed):
                if result['generated'] != result['remaining'] + result['network_out_S'] + result['network_out_L']:
                    raise AssertionError(('vehicle conservation',label,seed,cap,pocket,share))
            case={'seed':seed,'capacity':cap,'pocket_m':pocket,'b_share':share,
                  'delta_p60':score(changed,60)-score(baseline,60)}
            o=checkpoint_observation(cp)
            geom=decision(train,case,o,'geometry')
            case['geometry']=geom
            case['always_intervene']=True
            for age in DELAYS:
                old=o if age==0 else checkpoint_observation(run(c,tape,checkpoint_at=DECISION_TICK-age))
                if old['decision_tick'] != DECISION_TICK-age:
                    raise AssertionError('invalid observed tick')
                for level in ('counts','positions'):
                    key=f'{level}_age{age}'
                    case[key]=decision(train,case,old,level)
                    case[f'fallback_{key}']=freshness_choice(age,case[key],geom)
            cases.append(case)
        if len(cases) != 288:raise AssertionError('wrong prospective case count')
        summaries={}
        actions=('always_intervene','geometry') + tuple(
            p+f'_age{age}' for age in DELAYS
            for p in ('counts','positions','fallback_counts','fallback_positions'))
        oracle=sum(max(-r['delta_p60'],0) for r in cases)
        for name in actions:
            savings=sum(-r['delta_p60'] if r[name] else 0 for r in cases)
            summaries[name]={'total_saved':savings,'regret_to_hindsight':oracle-savings,
                             'treatment_count':sum(r[name] for r in cases),
                             'by_seed_saved':{str(seed):sum(-r['delta_p60'] if r[name] else 0
                                                     for r in cases if r['seed']==seed)
                                              for seed in SEEDS}}
        comparisons={}
        for age in DELAYS:
            for level in ('counts','positions'):
                frozen=summaries[f'{level}_age{age}']['by_seed_saved']
                fallback=summaries[f'fallback_{level}_age{age}']['by_seed_saved']
                differences=[(fallback[str(seed)]-frozen[str(seed)])/18 for seed in SEEDS]
                rng=random.Random(670000+age*19+(1 if level=='counts' else 2))
                boot=sorted(sum(rng.choices(differences,k=16))/16 for _ in range(10000))
                comparisons[f'{level}_age{age}']={
                    'mean_fallback_advantage_per_case':sum(differences)/16,
                    'seed_block_bootstrap_95pct': [boot[249],boot[9749]],
                    'positive_seed_blocks':sum(x>0 for x in differences),
                    'negative_seed_blocks':sum(x<0 for x in differences)}
        output[label]={'exogenous_demand_vph':demand,'left_share':left,
                       'pairs':cases,'summary':summaries,'oracle_saved':oracle,
                       'fallback_minus_stale':comparisons}
    return {'status':'SYNTHETIC_UNCALIBRATED','protocol':'PHYS-08 frozen prospective 12s fallback',
            'training_seeds':[0,7],'prospective_seeds':[40,55],
            'observation_ages_s':DELAYS,'fallback_threshold_s':FALLBACK_AGE_S,
            'regimes':output}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('training_json',type=Path)
    parser.add_argument('output_json',type=Path)
    args=parser.parse_args()
    train=json.loads(args.training_json.read_text(encoding='utf-8'))['pairs']
    result=evaluate(train)
    blob=(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    args.output_json.write_bytes(blob)
    print('SHA-256',hashlib.sha256(blob).hexdigest())
    for name,regime in result['regimes'].items():
        print(name,'oracle',regime['oracle_saved'])
        for p in ('always_intervene','geometry','counts_age24','positions_age24',
                  'fallback_counts_age24','fallback_positions_age24'):
            print(' ',p,regime['summary'][p]['total_saved'],regime['summary'][p]['regret_to_hindsight'])
