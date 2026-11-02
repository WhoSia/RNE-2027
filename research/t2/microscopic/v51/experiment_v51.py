"""T2 v5.1 same-OD sensitivity to movement-level crossing clearance.
   All headways in this experiment are synthetic stress assumptions, not estimates.
"""
from __future__ import annotations
import csv, json, statistics, math
from collections import defaultdict
from pathlib import Path
from network_v51 import DEMANDS, TurnParameters, make_arrivals, simulate
from experiment_v50 import plan, SPLITS, OFFSETS

ROOT=Path(__file__).resolve().parent
SEEDS=(11,29,41,73)
TURN_VARIANTS={
 'equal_2s':TurnParameters(),
 'turn_moderate':TurnParameters(main_exit_s=3.,side_merge_s=4.),
 'turn_stress':TurnParameters(main_exit_s=5.,side_merge_s=7.),
}

def write_csv(path,rows):
    if not rows:return
    with Path(path).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def execute(root=ROOT):
    root=Path(root);root.mkdir(exist_ok=True,parents=True)
    runs=[]
    for d in DEMANDS:
        for seed in SEEDS:
            arrivals=make_arrivals(d,seed,arrive_until=320.)
            for name,turn in TURN_VARIANTS.items():
                for green in SPLITS:
                    for offset in OFFSETS:
                        r=simulate(plan(green,offset),arrivals,horizon=580.,turns=turn)
                        s=r['summary'];m=s['crossings_by_movement']
                        runs.append({'demand':d.name,'seed':seed,'turn_model':name,
                            'green_s':green,'offset':offset,
                            'generated':s['generated'],'completed':s['completed'],
                            'inside':s['remaining_inside'],'boundary_pending':s['pending_boundary'],
                            'vehicle_seconds':s['system_vehicle_seconds_in_horizon'],
                            'release_events':s['release_events'],
                            'main_through':m['main_through'],'main_exit':m['main_exit'],
                            'side_merge':m['side_merge'],'side_exit':m['side_exit'],
                            'downstream_full_ticks':s['downstream_full_ticks'],
                            'exposure_identity_error':s['exposure_reconstruction_error_s']})
    write_csv(root/'runs.csv',runs)
    by=defaultdict(list)
    for r in runs:by[(r['demand'],r['turn_model'],r['green_s'],r['offset'])].append(r)
    means={k:statistics.mean(v['vehicle_seconds'] for v in a) for k,a in by.items()}
    meanrows=[{'demand':d,'turn_model':turn,'green_s':g,'offset':o,
               'mean_vehicle_seconds':means[(d,turn,g,o)],
               'mean_completed':statistics.mean(v['completed'] for v in by[(d,turn,g,o)]),
               'mean_side_merges':statistics.mean(v['side_merge'] for v in by[(d,turn,g,o)]),
               'n_seeds':len(by[(d,turn,g,o)])}
              for d,turn,g,o in sorted(by)]
    write_csv(root/'means.csv',meanrows)
    optima={}
    robust=[]
    for d in (v.name for v in DEMANDS):
        optima[d]={}
        choices=list((g,o) for g in SPLITS for o in OFFSETS)
        for turn in TURN_VARIANTS:
            ranked=sorted(choices,key=lambda x:means[(d,turn,*x)])
            optima[d][turn]={'best':ranked[0], 'ranking':ranked,
                 'best_vehicle_seconds':means[(d,turn,*ranked[0])]}
        for g,o in choices:
            regrets=[]
            for turn in TURN_VARIANTS:
                best=optima[d][turn]['best_vehicle_seconds']
                regrets.append((means[(d,turn,g,o)]-best)/best)
            robust.append({'demand':d,'green_s':g,'offset':o,
                   'max_fractional_regret':max(regrets),
                   'mean_fractional_regret':statistics.mean(regrets)})
    write_csv(root/'robust.csv',robust)
    paired=[]
    lookup={(r['demand'],r['seed'],r['turn_model'],r['green_s'],r['offset']):r for r in runs}
    for d in (v.name for v in DEMANDS):
        for name in ('turn_moderate','turn_stress'):
            for g in SPLITS:
                for o in OFFSETS:
                    changes=[lookup[(d,s,name,g,o)]['vehicle_seconds']-lookup[(d,s,'equal_2s',g,o)]['vehicle_seconds'] for s in SEEDS]
                    paired.append({'demand':d,'turn_model':name,'green_s':g,'offset':o,
                        'mean_increase_vehicle_seconds':statistics.mean(changes),
                        'min_increase':min(changes),'max_increase':max(changes),
                        'n_positive':sum(v>0 for v in changes),'n_seeds':len(SEEDS)})
    write_csv(root/'paired_model_effect.csv',paired)
    summary={'study':'T2 v5.1 movement-specific clearance sensitivity; synthetic',
      'runs':len(runs),'seeds':list(SEEDS),'policies':len(SPLITS)*len(OFFSETS),
      'turn_models':{k:vars(v) for k,v in TURN_VARIANTS.items()},
      'rankings':optima,
      'robust_best':{d:min((r for r in robust if r['demand']==d),key=lambda x:x['max_fractional_regret']) for d in optima},
      'max_abs_exposure_error':max(abs(r['exposure_identity_error']) for r in runs),
      'min_completed':min(r['completed'] for r in runs),
      'limits':['not real observed turning-saturation headways','no geometric conflict calibration',
       'single incoming lane per approach; no explicit turn bay','no real pedestrian movements',
       'not a SUMO independent verification','no field-calibrated OD']}
    (root/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    return summary,runs,means,robust

if __name__=='__main__':
    report,*_=execute();print('runs',report['runs']);
    for k,v in report['rankings'].items():print(k,{name:item['best'] for name,item in v.items()})
