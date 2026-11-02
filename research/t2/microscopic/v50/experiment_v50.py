"""T2 v5.0 controlled green/offset factorial and microscopic parameter sensitivity.
Synthetic matched-OD experiments only; not a fit to Korean field measurements.
"""
from __future__ import annotations
import csv, json, statistics, math
from pathlib import Path
from network_v50 import SignalPlan, DEMANDS, make_arrivals, simulate, DriverParameters

ROOT=Path(__file__).resolve().parent
SEEDS=(11,29,41,73)
# 3 green splits x 2 offset patterns; no simultaneous modifications in factor comparisons.
SPLITS=(25,32,38)
OFFSETS={'zero':(0,0,0),'progression':(0,14,28)}
DRIVERS=(DriverParameters(desired_speed_mps=10,headway_s=1.8),
         DriverParameters(desired_speed_mps=13,headway_s=1.0),
         DriverParameters(desired_speed_mps=13,headway_s=1.3))

def driver_key(p):return f'v{p.desired_speed_mps:g}_T{p.headway_s:g}'

def plan(g,offset):return SignalPlan(f'g{g}_{offset}',(g,g,g),OFFSETS[offset])

def write_csv(path,rows):
    if not rows:return
    with open(path,'w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def execute(root=ROOT):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    rows=[]
    for demand in DEMANDS:
        for seed in SEEDS:
            arrivals=make_arrivals(demand,seed,arrive_until=320.)
            for driver in DRIVERS:
                for green in SPLITS:
                    for offset in OFFSETS:
                        p=plan(green,offset)
                        s=simulate(p,arrivals,horizon=580.,driver=driver)['summary']
                        assert s['generated']==len(arrivals)
                        assert s['generated']==s['completed']+s['remaining_inside']+s['pending_boundary']
                        rows.append({'demand':demand.name,'seed':seed,
                            'driver':driver_key(driver),'desired_speed_mps':driver.desired_speed_mps,
                            'headway_s':driver.headway_s,'green_s':green,'offset':offset,
                            'generated':s['generated'],'completed':s['completed'],
                            'remaining_inside':s['remaining_inside'],'pending_boundary':s['pending_boundary'],
                            'vehicle_seconds':s['system_vehicle_seconds_in_horizon'],
                            'mean_completed_s':s['mean_completed_duration_s'],
                            'downstream_full_ticks':s['downstream_full_ticks']})
    write_csv(root/'matched_runs.csv',rows)
    by={}
    for r in rows:
        k=(r['demand'],r['driver'],r['green_s'],r['offset'])
        by.setdefault(k,[]).append(r)
    means={k:statistics.mean(r['vehicle_seconds'] for r in sub) for k,sub in by.items()}
    summaries=[{'demand':d,'driver':t,'green_s':g,'offset':o,
                'mean_vehicle_seconds':v,
                'mean_completed':statistics.mean(r['completed'] for r in by[(d,t,g,o)]),
                'mean_residual':statistics.mean(r['remaining_inside']+r['pending_boundary'] for r in by[(d,t,g,o)]),
                'n_seeds':len(SEEDS)} for (d,t,g,o),v in sorted(means.items())]
    write_csv(root/'cell_means.csv',summaries)
    paired=[]
    for d in (q.name for q in DEMANDS):
        for driver in (driver_key(p) for p in DRIVERS):
            bycase={(r['seed'],r['green_s'],r['offset']):r for r in rows
                    if r['demand']==d and r['driver']==driver}
            for g in SPLITS:
                diffs=[bycase[(seed,g,'progression')]['vehicle_seconds']-
                       bycase[(seed,g,'zero')]['vehicle_seconds'] for seed in SEEDS]
                paired.append({'demand':d,'driver':driver,'contrast':f'offset_progression_minus_zero_at_g{g}',
                               'mean_delta_vehicle_seconds':statistics.mean(diffs),
                               'sd_seed_deltas':statistics.stdev(diffs),
                               'individual_deltas':';'.join(str(x) for x in diffs)})
            for o in OFFSETS:
                for g in (25,38):
                    diffs=[bycase[(seed,g,o)]['vehicle_seconds']-
                           bycase[(seed,32,o)]['vehicle_seconds'] for seed in SEEDS]
                    paired.append({'demand':d,'driver':driver,'contrast':f'green_g{g}_minus_g32_at_{o}',
                                   'mean_delta_vehicle_seconds':statistics.mean(diffs),
                                   'sd_seed_deltas':statistics.stdev(diffs),
                                   'individual_deltas':';'.join(str(x) for x in diffs)})
    write_csv(root/'paired_contrasts.csv',paired)
    robust=[];rankings={}
    for d in (q.name for q in DEMANDS):
        keys=tuple((g,o) for g in SPLITS for o in OFFSETS)
        scenarios=tuple(driver_key(p) for p in DRIVERS)
        best={driver:min(means[(d,driver,*k)] for k in keys) for driver in scenarios}
        overall={k:max((means[(d,driver,*k)]-best[driver])/best[driver] for driver in scenarios) for k in keys}
        for k in keys:
            robust.append({'demand':d,'green_s':k[0],'offset':k[1],
                'max_regret_fraction_over_three_driver_models':overall[k],
                'mean_vehicle_seconds_across_driver_models':statistics.mean(means[(d,driver,*k)] for driver in scenarios)})
        rankings[d]={driver:[{'green_s':k[0],'offset':k[1],'vehicle_seconds':means[(d,driver,*k)]}
                             for k in sorted(keys,key=lambda k:means[(d,driver,*k)])] for driver in scenarios}
    write_csv(root/'robust_policy.csv',robust)
    report={'study':'T2 v5.0: factorial and microscopic sensitivity (synthetic)',
        'n_runs':len(rows),'n_seeds':len(SEEDS),'n_driver_variants':len(DRIVERS),
        'n_policies':len(SPLITS)*len(OFFSETS),'dt_s':.5,'horizon_s':580,
        'arrival_until_s':320,'driver_variants':[vars(p) for p in DRIVERS],
        'policy_best_by_driver':{d:{k:v[0] for k,v in rank.items()} for d,rank in rankings.items()},
        'max_regret_minimizers':{d:[{'green_s':r['green_s'],'offset':r['offset'],
                 'maximum_regret':r['max_regret_fraction_over_three_driver_models']} for r in sorted(
             (x for x in robust if x['demand']==d),key=lambda x:x['max_regret_fraction_over_three_driver_models'])[:2]]
            for d in (q.name for q in DEMANDS)},
        'unverified':['OD real counts','SUMO alignment','microscopic parameters calibrated',
                      'separate left turning conflicts','pedestrian and bus processes']}
    (root/'summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report,rows,means,paired,robust

if __name__=='__main__':
    report,*_=execute()
    print(json.dumps(report['max_regret_minimizers'],indent=2))
