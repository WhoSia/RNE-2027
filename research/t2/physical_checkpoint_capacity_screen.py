"""PHYS-04 capacity sensitivity on *one identical predecision state per case*.

Run locally:
 PYTHONPATH=research/t2 python research/t2/physical_checkpoint_capacity_screen.py results.json

This is a planned canonical-engine execution, not a report of a completed run.
Receiver storage counts are distinct *baseline geometries*: 2,4,8 cells.
Within a given capacity the control and treatment always share the same
checkpoint. Comparisons ACROSS capacities are not same-state causal effects.
"""
import argparse
import json
from itertools import product
from pathlib import Path

from dual_lane_v11 import DualConfig, run, checkpoint_observation
from spatial_v10 import Config, arrivals
from physical_transfer_screen import score

SEEDS=tuple(range(8))
POCKETS=(14.,28.,70.)
B_SHARES=(0.,.5)
CAPACITIES=(2,4,8)
PENALTIES=(0,60,120)
INTERVENTION=((84,87,'-'),(87,91,'L'),(91,120,'-'))


def checkpoint_case(seed,pocket,share,capacity):
    base=Config(seed=seed,pocket_length_m=pocket,phase_order='leading',
                duration_s=240,demand_vph=1800,left_fraction=.5)
    cfg=DualConfig(base=base,through_B_share=share,change_zone_m=100.,
                   allow_lane_changes=True,receiver_slots=capacity,
                   receiver_mode='cells')
    tape=arrivals(base)
    cp=run(cfg,tape,checkpoint_at=84)
    baseline=run(cfg,tape,resume_from=cp)
    direct=run(cfg,tape)
    if baseline!=direct:
        raise AssertionError(('restart mismatch',seed,pocket,share,capacity))
    policy=run(cfg,tape,resume_from=cp,phase_overrides=INTERVENTION)
    # Every policy branch must conserve the same demand tape.
    if baseline['generated']!=policy['generated']:
        raise AssertionError('unmatched future demand')
    return baseline,policy,checkpoint_observation(cp)


def experiment():
    rows=[]
    for capacity,seed,pocket,share in product(CAPACITIES,SEEDS,POCKETS,B_SHARES):
        baseline,policy,observation=checkpoint_case(seed,pocket,share,capacity)
        row={'capacity':capacity,'seed':seed,'pocket_m':pocket,'b_share':share,
             'generated':baseline['generated'],
             'baseline_remaining':baseline['remaining'],
             'treatment_remaining':policy['remaining'],
             'baseline_out_S':baseline['network_out_S'],
             'baseline_out_L':baseline['network_out_L'],
             'treatment_out_S':policy['network_out_S'],
             'treatment_out_L':policy['network_out_L'],
             'baseline_bypass':baseline['changes_A_to_B'],
             'treatment_bypass':policy['changes_A_to_B'],
             'checkpoint_identity':True,
             'decision_observation':observation}
        for p in PENALTIES:
            x=score(baseline,p)
            y=score(policy,p)
            row[f'cost_baseline_p{p}']=x
            row[f'cost_treatment_p{p}']=y
            row[f'delta_p{p}']=y-x
        rows.append(row)
    summary={}
    for cap in CAPACITIES:
        subgroup=[x for x in rows if x['capacity']==cap]
        summary[str(cap)]={str(p):{
            'treatment_preferred':sum(r[f'delta_p{p}']<0 for r in subgroup),
            'baseline_preferred':sum(r[f'delta_p{p}']>0 for r in subgroup),
            'ties':sum(r[f'delta_p{p}']==0 for r in subgroup)}
            for p in PENALTIES}
    # This is a limited in-model aliasing audit: equivalent aggregate
    # occupancies can still require opposite signal decisions.
    aliases=[]
    for cap in CAPACITIES:
        bins={}
        for row in rows:
            if row['capacity']!=cap:
                continue
            o=row['decision_observation']
            key=(row['pocket_m'],o['pocket_vehicles'],
                 o['receiver_vehicles'],o['approach_A'],o['approach_B'],
                 o['outside_A'],o['outside_B'])
            bins.setdefault(key,[]).append(row)
        for key,group in bins.items():
            signs={1 if r['delta_p60']>0 else -1 if r['delta_p60']<0 else 0
                   for r in group}
            if -1 in signs and 1 in signs:
                aliases.append({'capacity':cap,'observed_signature':key,
                                'cases':[{'seed':r['seed'],'pocket_m':r['pocket_m'],
                                          'b_share':r['b_share'],'delta_p60':r['delta_p60']}
                                         for r in group]})
    assert len(rows)==144
    return {'status':'SYNTHETIC_UNCALIBRATED','protocol':'T2-PHYS-04-capacity',
            'predecision_tick':84,'runs_per_capacity':48,
            'policy':INTERVENTION,'penalties':PENALTIES,
            'cross_capacity_note':'Capacity is a baseline geometry, not a matched-state intervention',
            'summary':summary,'partial_observation_sign_conflicts':aliases,
            'pairs':rows}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    args.output.write_text(json.dumps(experiment(),ensure_ascii=False,
                                      sort_keys=True,indent=2)+'\n',encoding='utf-8')
