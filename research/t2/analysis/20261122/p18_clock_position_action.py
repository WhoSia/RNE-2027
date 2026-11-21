"""P18 prospectively declared canonical-T2 synthetic arrival-clock experiment.

This code never controls a real signal. A model-native '-' clearance is NOT
real yellow/red/pedestrian clearance. See the P18 preregistration.
"""
from dataclasses import replace
from collections import defaultdict, Counter
from itertools import product
from pathlib import Path
from random import Random
import hashlib
import json
import pickle

from spatial_v10 import Config, arrivals
from dual_lane_v11 import DualConfig, run, checkpoint_observation
from physical_transfer_screen import score

SEEDS = tuple(range(104, 112))
REGIMES = ((1800, .45), (1650, .50))
POCKETS = (14., 28.)
RECEIVERS = (2, 4)
B_SHARES = (0., .5)
CLOCKS = ('legacy', 'reshuffled_time')
DECISION_TICK = 84
EPSILON = 5
PENALTY = 60
OVERRIDES = {
    'left_4s': ((84, 87, '-'), (87, 91, 'L'), (91, 120, '-')),
    'left_8s': ((84, 87, '-'), (87, 95, 'L'), (95, 120, '-')),
}
SIX = ('outside_A','outside_B','approach_A','approach_B','pocket_vehicles','receiver_vehicles')
POSITION = ('pocket_positions','approach_A_positions','approach_B_positions','receiver_occupied_cells')


def arrival_clock_pair(base):
    """Keep total N and ordered route labels identical; vary timestamps only."""
    original = arrivals(base)
    rng = Random(base.seed + 1_000_003)
    new_times = sorted(rng.randrange(base.duration_s) for _ in original)
    changed = tuple((t, route) for t, (_, route) in zip(new_times, original))
    assert len(original) == len(changed)
    assert tuple(x[1] for x in original) == tuple(x[1] for x in changed)
    assert tuple(t for t, _ in changed) == tuple(sorted(t for t, _ in changed))
    return original, changed


def tape_hash(tape):
    return hashlib.sha256(json.dumps(tape, separators=(',',':')).encode('utf-8')).hexdigest()


def build_config(seed, demand, left_share, pocket_m, receiver, b_share):
    base = Config(seed=seed, duration_s=240, demand_vph=demand,
                  left_fraction=left_share, pocket_length_m=pocket_m,
                  phase_order='leading')
    cfg = DualConfig(base=base, receiver_slots=receiver,
                     receiver_mode='cells', through_B_share=b_share,
                     change_zone_m=100., allow_lane_changes=True)
    return cfg


def evaluate_world(config, tape, clock, *, check_direct=False):
    cp = run(config, tape, checkpoint_at=DECISION_TICK)
    cp_before = pickle.dumps(cp, protocol=4)
    observation = checkpoint_observation(cp)
    baseline = run(config, tape, resume_from=cp)
    assert pickle.dumps(cp, protocol=4) == cp_before, 'checkpoint modified by resume'
    if check_direct:
        assert run(config, tape) == baseline, 'direct/resumed baseline mismatch'
    values = {}
    for name, action in OVERRIDES.items():
        treatment = run(config, tape, resume_from=cp, phase_overrides=action)
        assert pickle.dumps(cp, protocol=4) == cp_before, 'checkpoint modified by intervention'
        assert baseline['generated'] == treatment['generated'] == len(tape)
        values[name] = score(treatment, PENALTY) - score(baseline, PENALTY)
    return {
        'clock': clock,
        'seed': config.base.seed,
        'demand_vph': config.base.demand_vph,
        'left_fraction': config.base.left_fraction,
        'pocket_m': config.base.pocket_length_m,
        'capacity': config.receiver_slots,
        'b_share': config.through_B_share,
        'generated': len(tape),
        'arrivals_before_tick84': sum(t < DECISION_TICK for t, _ in tape),
        'route_hash': hashlib.sha256(''.join(r for _,r in tape).encode()).hexdigest(),
        'tape_hash': tape_hash(tape),
        'counts': [observation[k] for k in SIX],
        'positions': [list(observation[k]) for k in POSITION],
        'checkpoint_sha256': hashlib.sha256(cp_before).hexdigest(),
        'baseline_cost': score(baseline, PENALTY),
        'delta': values,
        'model_clearance_validated': True,
        'illustrative_green_min6_eligible': {'left_4s': False, 'left_8s': True},
        'actual_yellow_red_pedestrian_modeled': False,
    }


def signature(row, positions=False):
    key=(row['demand_vph'], row['left_fraction'], row['capacity'],
         row['pocket_m'], row['b_share'], tuple(row['counts']))
    if positions:
        key+=tuple(tuple(x) for x in row['positions']),
    return key


def alias_screen(rows, action, *, positions=False, epsilon=EPSILON):
    grouped=defaultdict(list)
    for row in rows:
        grouped[signature(row, positions)].append(row)
    collision=[g for g in grouped.values() if len(g)>1]
    candidates=[]
    for group in collision:
        neg=[r for r in group if r['delta'][action] < -epsilon]
        pos=[r for r in group if r['delta'][action] > epsilon]
        if neg and pos:
            candidate={
                'key': repr(signature(group[0],positions)),
                'negative': [{'seed':r['seed'],'clock':r['clock'],'delta':r['delta'][action],
                              'tape_hash':r['tape_hash']} for r in neg],
                'positive': [{'seed':r['seed'],'clock':r['clock'],'delta':r['delta'][action],
                              'tape_hash':r['tape_hash']} for r in pos],
                'distinct_tape_sha256':len({r['tape_hash'] for r in neg+pos}),
            }
            candidates.append(candidate)
    return {'groups':len(grouped),'collision_groups':len(collision),
            'collision_rows':sum(len(g) for g in collision),
            'opposite_sign_groups':len(candidates),'candidates':candidates}


def screen_cross_clock(rows,action):
    by=defaultdict(dict)
    for r in rows:
        key=(r['demand_vph'],r['seed'],r['capacity'],r['pocket_m'],r['b_share'])
        if r['clock'] in by[key]: raise ValueError('duplicate clock within key')
        by[key][r['clock']]=r
    opposite=[]; state_equal=0; six_equal=0; positions_equal=0
    for key,r in sorted(by.items()):
        if set(r)!=set(CLOCKS):raise ValueError('missing paired clock')
        a,b=r[CLOCKS[0]],r[CLOCKS[1]]
        if a['route_hash']!=b['route_hash'] or a['generated']!=b['generated']:
            raise AssertionError('route/count matching failed')
        if a['counts']==b['counts']:
            six_equal+=1
            if a['positions']==b['positions']: positions_equal+=1
        if a['checkpoint_sha256']==b['checkpoint_sha256']: state_equal+=1
        da,db=a['delta'][action],b['delta'][action]
        if da < -EPSILON and db > EPSILON or db < -EPSILON and da > EPSILON:
            opposite.append({'demand':key[0],'seed':key[1], 'capacity':key[2],
                             'pocket_m':key[3], 'b_share':key[4],
                             'legacy_delta':da,'reshuffled_delta':db,
                             'six_counts_equal':a['counts']==b['counts'],
                             'positions_equal':a['positions']==b['positions'],
                             'pre84_arrivals':[a['arrivals_before_tick84'],b['arrivals_before_tick84']],
                             'tapes':[a['tape_hash'],b['tape_hash']]})
    return {'clock_pair_count':len(by), 'strict_cross_clock_sign_reversals':len(opposite),
            'six_counts_equal_pairs':six_equal,'positions_equal_pairs':positions_equal,
            'identical_checkpoint_serialization_pairs':state_equal,
            'reversal_seed_groups':len({(r['demand'],r['seed']) for r in opposite}),
            'opposite_witnesses':opposite}


def experiment():
    records=[]
    for (demand,left_share),seed,pocket,receiver,bshare in product(REGIMES,SEEDS,POCKETS,RECEIVERS,B_SHARES):
        cfg=build_config(seed,demand,left_share,pocket,receiver,bshare)
        original, changed=arrival_clock_pair(cfg.base)
        for clock,tape in zip(CLOCKS,(original,changed)):
            records.append(evaluate_world(cfg,tape,clock,check_direct=(seed==104 and clock=='legacy')))
    assert len(records)==256
    results={}
    for action in OVERRIDES:
        changes=[r['delta'][action] for r in records]
        results[action]={
            'negative':sum(d<0 for d in changes), 'positive':sum(d>0 for d in changes),
            'ties':sum(d==0 for d in changes),
            'mean_delta':sum(changes)/len(changes),
            'model_only_action_min_green6':('INELIGIBLE' if action=='left_4s' else 'ELIGIBLE_ON_MIN_GREEN_ALONE'),
            'aggregate_alias':alias_screen(records,action,positions=False),
            'position_alias':alias_screen(records,action,positions=True),
            'cross_clock':screen_cross_clock(records,action),
        }
    return {
        'protocol':'T2_P18_PROSPECTIVE_EXACT_MAIN', 'simulator':'SYNTHETIC_UNCALIBRATED',
        'seed_range':[104,111], 'clock_families':list(CLOCKS),
        'worlds':len(records), 'baseline_runs':len(records),'treatment_runs':len(records)*len(OVERRIDES),
        'actions':{k:[list(x) for x in v] for k,v in OVERRIDES.items()},
        'model_not_real_clearance':True,
        'unique_full_tapes':len({r['tape_hash'] for r in records}),
        'results':results,'records':records,
    }


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);args=ap.parse_args()
    args.output.write_text(json.dumps(experiment(),ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
