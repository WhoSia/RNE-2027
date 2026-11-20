"""Predeclared 192-case T2 transfer screen using existing dual_lane_v11.

Requires canonical research/t2/dual_lane_v11.py, receiving_cells_v15.py and
spatial_v10.py on PYTHONPATH. The 192 physical cases have NOT been evaluated
in this standalone analysis environment; tests below are design tests.
"""
from dataclasses import dataclass, asdict, replace
from itertools import product
from pathlib import Path
import json,csv

SEEDS=tuple(range(8))
POCKETS_M=(14.,28.,70.)
B_SHARES=(0.,0.5)
LANE_CHANGES=(False,True)
ORDERS=('leading','lagging')
DURATION_S=720
DEMAND_VPH=1800
TURN_SHARE=.5
TERMINAL_PENALTY=60

@dataclass(frozen=True)
class Case:
    seed:int
    pocket_m:float
    b_share:float
    change:bool
    order:str


def cases():
    return tuple(Case(*x) for x in product(SEEDS,POCKETS_M,B_SHARES,LANE_CHANGES,ORDERS))


def score(r,terminal_penalty=TERMINAL_PENALTY):
    fields=('outside_vehicle_seconds','upstream_vehicle_seconds','receiver_vehicle_seconds')
    if any(r[f]<0 for f in fields) or r['remaining']<0:
        raise ValueError('negative occupancy or terminal state')
    if r['generated'] != r['network_out_S'] + r['network_out_L'] + r['remaining']:
        raise AssertionError('vehicle conservation mismatch')
    return sum(r[f] for f in fields)+terminal_penalty*r['remaining']


def paired(rows):
    lookup={}
    for x in rows:
        k=x['seed'],x['pocket_m'],x['b_share'],x['change']
        key=k+(x['order'],)
        if key in lookup:raise ValueError('duplicate physical condition '+str(key))
        lookup[key]=x
    result=[]
    for seed,pocket,b,change in product(SEEDS,POCKETS_M,B_SHARES,LANE_CHANGES):
        k=(seed,pocket,b,change)
        if k+('leading',) not in lookup or k+('lagging',) not in lookup:
            raise ValueError('missing matched physical pair '+str(k))
        left=lookup[k+('leading',)]
        right=lookup[k+('lagging',)]
        if left['generated']!=right['generated']:
            raise AssertionError('unmatched demand between protected phase orders')
        result.append(dict(seed=seed,pocket_m=pocket,b_share=b,change=change,
                           delta_left_first_minus_through_first=left['objective']-right['objective'],
                           L_first=left['objective'],S_first=right['objective'],
                           difference_exit_S=left['network_out_S']-right['network_out_S'],
                           difference_exit_L=left['network_out_L']-right['network_out_L']))
    return result


def summarize(pairs):
    groups={}
    for x in pairs:
        k=x['seed'],x['pocket_m'],x['b_share']
        groups.setdefault(k,{})[x['change']]=x['delta_left_first_minus_through_first']
    reversed_pairs=[]
    zeros=[]
    for key,v in groups.items():
        if set(v)!={False,True}:raise AssertionError('missing bypass matched pair')
        if v[False]*v[True]<0: reversed_pairs.append(key)
        if 0 in v.values():zeros.append(key)
    return {'scenario_count':len(pairs)*2,'paired_phase_comparisons':len(pairs),
            'paired_lane_change_comparisons':len(groups),
            'strict_sign_reversals_on_lane_change_permission':len(reversed_pairs),
            'ties_in_any_comparison':len(zeros),
            'strict_reversal_case_keys':[list(x) for x in reversed_pairs]}


def experiment(simulator_run=None):
    if simulator_run is None:
        from spatial_v10 import Config,arrivals
        from dual_lane_v11 import DualConfig,run
    else:
        from dataclasses import dataclass
        @dataclass(frozen=True)
        class Config:
            seed:int=0
            pocket_length_m:float=28.
            phase_order:str='leading'
            duration_s:int=DURATION_S
            demand_vph:int=DEMAND_VPH
            left_fraction:float=TURN_SHARE
        @dataclass(frozen=True)
        class DualConfig:
            base:object
            through_B_share:float
            allow_lane_changes:bool
            change_zone_m:float=70.
            receiver_mode:str='cells'
            receiver_slots:int=4
        def arrivals(base):return tuple((i,'S') for i in range(12))
        run=simulator_run
    streams={s:arrivals(Config(seed=s,duration_s=DURATION_S,
                    demand_vph=DEMAND_VPH,left_fraction=TURN_SHARE)) for s in SEEDS}
    results=[]
    for case in cases():
        base=Config(seed=case.seed,duration_s=DURATION_S,demand_vph=DEMAND_VPH,
                    left_fraction=TURN_SHARE,pocket_length_m=case.pocket_m,phase_order=case.order)
        cfg=DualConfig(base=base,through_B_share=case.b_share,
                      allow_lane_changes=case.change,change_zone_m=70.,
                      receiver_mode='cells',receiver_slots=4)
        y=run(cfg,streams[case.seed])
        result={**asdict(case),**{key:y[key] for key in (
            'generated','network_out_S','network_out_L','remaining',
            'outside_vehicle_seconds','upstream_vehicle_seconds',
            'receiver_vehicle_seconds','pocket_block_seconds',
            'changes_A_to_B','receiver_denied_attempts','receiver_denied_seconds')}}
        result['objective']=score(result)
        results.append(result)
    pair_rows=paired(results)
    return {'contract':'192 runs, existing v2.2 7m cell physics, synthetic uncalibrated',
            'summary':summarize(pair_rows),'runs':results,'paired':pair_rows}


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    args=ap.parse_args()
    payload=experiment()
    args.output.write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
