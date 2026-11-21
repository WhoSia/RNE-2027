"""T2-PHYS-07: frozen decision policy under stale telemetry and demand shift.

All cost outcomes are synthetic, model-conditional; no field inference.
Training on seeds 0..7 at 1800 vph, 50% left turns only. Validation is
on disjoint seed groups; no held-out outcome is used in an action decision.
Usage: PYTHONPATH=research/t2 python research/t2/physical_checkpoint_delay_and_shift.py TRAIN.json HOLDOUT.json OUTPUT.json
"""
import argparse
import hashlib
import json
from itertools import product
from pathlib import Path
from dual_lane_v11 import DualConfig, run, checkpoint_observation
from spatial_v10 import Config, arrivals
from physical_checkpoint_observation_ablation import predict
from physical_transfer_screen import score

DECISION_TICK = 84
INTERVENTION = ((84,87,'-'),(87,91,'L'),(91,120,'-'))
DELAYS = (0,3,6,12,24)
SEED_SHIFT = range(32,40)
REGIMES = (
    ('baseline_unseen', 1800, .5, 'uniform'),
    ('light_lowturn', 1350, .3, 'uniform'),
    ('heavy_highturn', 2250, .7, 'uniform'),
    ('platoon_baseline', 1800, .5, 'platoon'),
    ('platoon_heavy', 2250, .7, 'platoon'),
)


def make_config(seed, capacity, pocket, share, demand=1800, left=.5, pattern='uniform'):
    base = Config(seed=seed, duration_s=240, demand_vph=demand,
                  left_fraction=left, arrival_pattern=pattern,
                  pocket_length_m=pocket, phase_order='leading')
    c = DualConfig(base=base, through_B_share=share, allow_lane_changes=True,
                   change_zone_m=100., receiver_slots=capacity, receiver_mode='cells')
    return c


def decision(train, case, observation, level):
    sample = dict(case, decision_observation=observation)
    return predict(train, sample, level, k=5) < 0


def summarize(rows, names):
    oracle = sum(max(-r['delta_p60'], 0) for r in rows)
    out = {}
    for name in names:
        total = sum(-r['delta_p60'] if r[name] else 0 for r in rows)
        by_seed = {str(seed): sum(-r['delta_p60'] if r[name] else 0
                   for r in rows if r['seed'] == seed)
                   for seed in sorted(set(r['seed'] for r in rows))}
        out[name] = {'saved_vs_always_control': total,
                     'regret_to_hindsight_oracle': oracle - total,
                     'actions_treat': sum(r[name] for r in rows),
                     'by_seed_saved': by_seed}
    return {'cases': len(rows), 'oracle_saved': oracle, 'policies': out}


def observation_delay_stress(train, holdout):
    out = []
    assert len(holdout) == 432
    for row in holdout:
        seed, cap, pocket, share = (row[k] for k in ('seed','capacity','pocket_m','b_share'))
        cfg = make_config(seed,cap,pocket,share)
        tape = arrivals(cfg.base)
        observation_now = checkpoint_observation(run(cfg,tape,checkpoint_at=DECISION_TICK))
        assert all(observation_now[key] == row['decision_observation'][key]
                   for key in ('outside_A','outside_B','approach_A','approach_B',
                               'pocket_vehicles','receiver_vehicles'))
        assert all(tuple(observation_now[key]) == tuple(row['decision_observation'][key])
                   for key in ('approach_A_positions','approach_B_positions',
                               'pocket_positions','receiver_occupied_cells'))
        result = {k: row[k] for k in ('seed','capacity','pocket_m','b_share','delta_p60')}
        for delay in DELAYS:
            if delay:
                stale = checkpoint_observation(run(cfg,tape,checkpoint_at=DECISION_TICK-delay))
            else:
                stale = observation_now
            for level in ('counts','positions'):
                result[f'{level}_delay{delay}'] = decision(train,row,stale,level)
        out.append(result)
    labels = [f'{level}_delay{d}' for d in DELAYS for level in ('counts','positions')]
    stats = summarize(out, labels)
    for label in labels:
        base = label.split('_delay')[0] + '_delay0'
        stats['policies'][label]['changed_vs_current'] = sum(r[label] != r[base] for r in out)
    return {'summary': stats, 'paired_decisions': out}


def demand_shift_stress(train):
    all_regimes={}
    for label,demand,left,pattern in REGIMES:
        rows=[]
        for seed,cap,pocket,share in product(SEED_SHIFT,(2,4,8),(14.,28.,70.),(0.,.5)):
            c = make_config(seed,cap,pocket,share,demand,left,pattern)
            tape = arrivals(c.base)
            cp=run(c,tape,checkpoint_at=DECISION_TICK)
            baseline=run(c,tape,resume_from=cp)
            if baseline != run(c,tape):
                raise AssertionError(('checkpoint replay mismatch',label,seed,cap,pocket,share))
            policy=run(c,tape,resume_from=cp,phase_overrides=INTERVENTION)
            for branch in (baseline,policy):
                if branch['generated'] != branch['remaining'] + branch['network_out_S'] + branch['network_out_L']:
                    raise AssertionError(('conservation',label,seed,cap,pocket,share))
            delta=score(policy,60)-score(baseline,60)
            obs=checkpoint_observation(cp)
            case={'seed':seed,'capacity':cap,'pocket_m':pocket,'b_share':share,
                  'delta_p60':delta,'count_t84':obs['approach_A']+obs['approach_B']}
            for level in ('geometry','counts','positions'):
                case[level]=decision(train,case,obs,level)
            case['always_intervene']=True
            rows.append(case)
        assert len(rows)==144
        all_regimes[label]={'parameters':{'demand_vph':demand,'left_fraction':left,
                                         'arrival_pattern':pattern},
                            'summary':summarize(rows,('always_intervene','geometry','counts','positions')),
                            'paired_cases':rows}
    return all_regimes


def experiment(train,holdout):
    if len(train)!=144 or {r['seed'] for r in train}!=set(range(8)):
        raise ValueError('training requires seeds 0..7, all 144 cases')
    if len(holdout)!=432 or {r['seed'] for r in holdout}!=set(range(8,32)):
        raise ValueError('holdout requires seeds 8..31, all 432 cases')
    return {'status':'SYNTHETIC_UNCALIBRATED',
            'protocol':'PHYS-07 frozen-policy observation-lag and demand-shift',
            'train_seeds':[0,7], 'holdout_seeds':[8,31], 'shift_seeds':[32,39],
            'lags_s':DELAYS, 'shift_regimes':demand_shift_stress(train),
            'lag_results':observation_delay_stress(train,holdout)}


def write_output(payload,path):
    raw=(json.dumps(payload,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('training_json',type=Path)
    parser.add_argument('holdout_json',type=Path)
    parser.add_argument('output_json',type=Path)
    args=parser.parse_args()
    train=json.loads(args.training_json.read_text(encoding='utf-8'))['pairs']
    holdout=json.loads(args.holdout_json.read_text(encoding='utf-8'))['cases']
    outcome=experiment(train,holdout)
    print('SHA-256',write_output(outcome,args.output_json))
    print('LAGS', {k:(v['saved_vs_always_control'],v['changed_vs_current'])
          for k,v in outcome['lag_results']['summary']['policies'].items()})
    print('SHIFT', {k:{z:w['saved_vs_always_control'] for z,w in r['summary']['policies'].items()}
          for k,r in outcome['shift_regimes'].items()})
