"""PHYS-11: prospective 144 policy pairs under 1/2/3-tick gap confirmation.

Seed 80..87 only, locked in PHYS_11_GAP_CONFIRMATION_PREREG.md.
Different confirmation values are different predecision physical worlds.
Within each value, control and treatment share a tick84 checkpoint.
"""
import argparse
import hashlib
import json
from itertools import product
from pathlib import Path

from dual_lane_v11 import DualConfig, run
from spatial_v10 import Config, arrivals
from physical_transfer_screen import score

SEEDS=tuple(range(80,88))
CONFIRMATIONS=(1,2,3)
POCKETS=(14.,28.,70.)
B_SHARES=(0.,.5)
PLAN=((84,87,'-'),(87,91,'L'),(91,120,'-'))


def experiment():
    rows=[]
    for confirm,seed,pocket,share in product(CONFIRMATIONS,SEEDS,POCKETS,B_SHARES):
        base=Config(seed=seed,duration_s=240,pocket_length_m=pocket,
                    demand_vph=1800,left_fraction=.5,phase_order='leading')
        c=DualConfig(base=base,through_B_share=share,allow_lane_changes=True,
                     change_zone_m=100.,receiver_mode='cells',receiver_slots=4,
                     lane_change_target_gap_cells=1,
                     lane_change_gap_confirmation_s=confirm)
        tape=arrivals(base)
        cp=run(c,tape,checkpoint_at=84)
        baseline=run(c,tape,resume_from=cp)
        if baseline!=run(c,tape):
            raise AssertionError(('bad checkpoint',confirm,seed,pocket,share))
        treated=run(c,tape,resume_from=cp,phase_overrides=PLAN)
        for r in (baseline,treated):
            if r['generated']!=r['network_out_S']+r['network_out_L']+r['remaining']:
                raise AssertionError('vehicle conservation')
        rows.append({'confirmation_s':confirm,'seed':seed,'pocket_m':pocket,
                     'b_share':share,'delta':score(treated,60)-score(baseline,60),
                     'baseline_cost':score(baseline,60),'treated_cost':score(treated,60),
                     'baseline_changes':baseline['changes_A_to_B'],
                     'treated_changes':treated['changes_A_to_B'],
                     'baseline_confirmation_wait_s':baseline['lane_change_gap_confirmation_wait_s'],
                     'treated_confirmation_wait_s':treated['lane_change_gap_confirmation_wait_s'],
                     'baseline_target_denials':baseline['lane_change_target_gap_denials'],
                     'treated_target_denials':treated['lane_change_target_gap_denials'],
                     'baseline_remaining':baseline['remaining'],
                     'treated_remaining':treated['remaining'],
                     'baseline_out_S':baseline['network_out_S'],
                     'treated_out_S':treated['network_out_S'],
                     'baseline_out_L':baseline['network_out_L'],
                     'treated_out_L':treated['network_out_L'],
                     'matched_predecision':True})
    if len(rows)!=144:raise AssertionError('wrong pair count')
    summary={}
    for confirm in CONFIRMATIONS:
        cohort=[r for r in rows if r['confirmation_s']==confirm]
        summary[str(confirm)]={'pairs':len(cohort),
               'treat_better':sum(r['delta']<0 for r in cohort),
               'baseline_better':sum(r['delta']>0 for r in cohort),
               'ties':sum(r['delta']==0 for r in cohort),
               'mean_delta':sum(r['delta'] for r in cohort)/len(cohort),
               'baseline_changes':sum(r['baseline_changes'] for r in cohort),
               'baseline_confirmation_wait_s':sum(r['baseline_confirmation_wait_s'] for r in cohort),
               'baseline_remaining':sum(r['baseline_remaining'] for r in cohort)}
    reversals=[]
    for seed,pocket,share in product(SEEDS,POCKETS,B_SHARES):
        matches=[next(r for r in rows if r['seed']==seed and r['pocket_m']==pocket
                      and r['b_share']==share and r['confirmation_s']==confirm)
                 for confirm in CONFIRMATIONS]
        d=[r['delta'] for r in matches]
        if min(d)<0<max(d):
            reversals.append({'seed':seed,'pocket_m':pocket,'b_share':share,'deltas':d})
    return {'status':'SYNTHETIC_UNCALIBRATED',
            'protocol':'PHYS-11 consecutive candidate target-gap persistence',
            'physically_distinct_predecision_worlds':True,
            'prespecified_seeds':[80,87],
            'summary':summary,'strict_sign_reversals':reversals,'pairs':rows}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('output_json',type=Path)
    args=ap.parse_args()
    data=(json.dumps(experiment(),sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    args.output_json.write_bytes(data)
    print('SHA256',hashlib.sha256(data).hexdigest())
    result=json.loads(data)
    print(result['summary'])
    print('strict reversals',len(result['strict_sign_reversals']))
    print('first witnesses',result['strict_sign_reversals'][:4])
