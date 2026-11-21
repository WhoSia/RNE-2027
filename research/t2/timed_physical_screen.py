"""Preregistered PHYS-02: equal-duration early/late lane-change opportunity windows.

Original PHYS-01 geometry, 8 seeds, 14/28/70m pockets, B shares 0/.5,
720s and four regimes never/early/late/always; no field calibration.
"""
import json
from itertools import product
from dataclasses import replace
from pathlib import Path
from dual_lane_v11 import DualConfig, run
from spatial_v10 import Config, arrivals
from physical_transfer_screen import score

SEEDS=range(8)
POCKETS=(14.,28.,70.)
B_SHARES=(0.,.5)
REGIMES=('never','early','late','always')
ORDERS=('leading','lagging')
WINDOWS={
 'early':tuple((20+120*c,35+120*c) for c in range(6)),
 'late':tuple((70+120*c,85+120*c) for c in range(6))
}


def experiment():
    demand={s:arrivals(Config(seed=s,duration_s=720,demand_vph=1800,left_fraction=.5)) for s in SEEDS}
    rows=[]
    for seed,pocket,share,regime,order in product(SEEDS,POCKETS,B_SHARES,REGIMES,ORDERS):
        base=Config(seed=seed,duration_s=720,demand_vph=1800,left_fraction=.5,
                    pocket_length_m=pocket,phase_order=order)
        d=DualConfig(base=base,through_B_share=share,
            allow_lane_changes=(regime!='never'),change_zone_m=70.,
            lane_change_windows=WINDOWS.get(regime,()),receiver_mode='cells',receiver_slots=4)
        result=run(d,demand[seed])
        relevant=('generated','remaining','network_out_S','network_out_L',
                  'outside_vehicle_seconds','upstream_vehicle_seconds','receiver_vehicle_seconds',
                  'pocket_block_seconds','changes_A_to_B','receiver_denied_attempts','receiver_denied_seconds')
        row={'seed':seed,'pocket_m':pocket,'b_share':share,'regime':regime,'order':order,
             **{k:result[k] for k in relevant}}
        for p in (0,60,120):
            row[f'cost_p{p}']=score(row,p)
        rows.append(row)
    lookup={(r['seed'],r['pocket_m'],r['b_share'],r['regime'],r['order']):r for r in rows}
    pairs=[]
    for seed,pocket,share,regime in product(SEEDS,POCKETS,B_SHARES,REGIMES):
        left=lookup[seed,pocket,share,regime,'leading'];through=lookup[seed,pocket,share,regime,'lagging']
        pairs.append({'seed':seed,'pocket_m':pocket,'b_share':share,'regime':regime,
                      **{f'delta_p{p}':left[f'cost_p{p}']-through[f'cost_p{p}'] for p in (0,60,120)},
                      'changes_both_orders':left['changes_A_to_B']+through['changes_A_to_B'],
                      'exit_S_left':left['network_out_S'],'exit_S_through':through['network_out_S'],
                      'exit_L_left':left['network_out_L'],'exit_L_through':through['network_out_L']})
    grouped={(x['seed'],x['pocket_m'],x['b_share'],x['regime']):x for x in pairs}
    contrasts=[]
    for seed,pocket,share in product(SEEDS,POCKETS,B_SHARES):
        e=grouped[seed,pocket,share,'early'];l=grouped[seed,pocket,share,'late'];n=grouped[seed,pocket,share,'never'];a=grouped[seed,pocket,share,'always']
        contrasts.append({'seed':seed,'pocket_m':pocket,'b_share':share,
                          **{f'early_delta_p{p}':e[f'delta_p{p}'] for p in (0,60,120)},
                          **{f'late_delta_p{p}':l[f'delta_p{p}'] for p in (0,60,120)},
                          'early_changes':e['changes_both_orders'],'late_changes':l['changes_both_orders'],
                          'never_delta_p60':n['delta_p60'],'always_delta_p60':a['delta_p60']})
    result={
        'status':'SYNTHETIC_UNCALIBRATED','protocol':'T2-PHYS-02',
        'windows':WINDOWS,'runs':rows,'phase_pairs':pairs,'early_late_contrasts':contrasts,
        'summary':{
            'n_runs':len(rows),'phase_pairs':len(pairs),'matched_opportunity_pairs':len(contrasts),
            'reversals_by_penalty':{str(p):sum(x[f'early_delta_p{p}']*x[f'late_delta_p{p}']<0 for x in contrasts) for p in (0,60,120)},
            'ties_p60':sum(x['early_delta_p60']==0 or x['late_delta_p60']==0 for x in contrasts),
            'same_actual_bypass_count':sum(x['early_changes']==x['late_changes'] for x in contrasts),
            'early_total_changes':sum(x['early_changes'] for x in contrasts),
            'late_total_changes':sum(x['late_changes'] for x in contrasts),
        }}
    assert len(rows)==384 and len(pairs)==192 and len(contrasts)==48
    return result


def assert_baseline_equal(windowed,pre_registered):
    originals={(x['seed'],x['pocket_m'],x['b_share'],x['change'],x['order']):x
               for x in pre_registered['runs']}
    keys=('generated','network_out_S','network_out_L','remaining',
          'outside_vehicle_seconds','upstream_vehicle_seconds','receiver_vehicle_seconds',
          'pocket_block_seconds','changes_A_to_B','receiver_denied_attempts','receiver_denied_seconds')
    count=0
    for new in windowed['runs']:
        if new['regime'] not in ('never','always'):continue
        orig=originals[new['seed'],new['pocket_m'],new['b_share'],new['regime']=='always',new['order']]
        if any(new[k]!=orig[k] for k in keys) or new['cost_p60']!=orig['objective']:
            raise AssertionError(('default regression mismatch',new,orig))
        count+=1
    if count!=192:raise AssertionError('missing original baseline rows')
    return count

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);ap.add_argument('--baseline',type=Path)
    args=ap.parse_args()
    result=experiment()
    if args.baseline:
        n=assert_baseline_equal(result,json.loads(args.baseline.read_text()))
        result['summary']['baseline_verified_rows']=n
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
