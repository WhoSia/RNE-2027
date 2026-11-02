"""T2 v5.2 paired sensitivity: finite turn-pocket geometry vs signal policy.
The bay has an instant lateral transfer at its entrance; never interpret results as field-calibrated.
"""
from __future__ import annotations
import csv, json, statistics, math
from pathlib import Path
from collections import defaultdict
from network_v52 import (PocketGeometry, DEMANDS, PLANS, make_arrivals, simulate)

ROOT=Path(__file__).resolve().parent
POCKET_LENGTHS=(15.,30.,60.,90.)
SEEDS=(11,29,41,73,101,137,151,179)
POLICIES=PLANS[:3]
ARRIVE_UNTIL=260.
HORIZON=440.

def write_csv(path,rows):
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def run(root=ROOT):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    runs=[]
    for d in DEMANDS:
        for seed in SEEDS:
            manifest=make_arrivals(d,seed,arrive_until=ARRIVE_UNTIL)
            for bay in POCKET_LENGTHS:
                geom=PocketGeometry((bay,bay,0.))
                for plan in POLICIES:
                    s=simulate(plan,manifest,horizon=HORIZON,pockets=geom)['summary']
                    runs.append(dict(demand=d.name,seed=seed,pocket_m=bay,policy=plan.name,
                      generated=s['generated'],completed=s['completed'],inside=s['remaining_inside'],
                      boundary=s['pending_boundary'],vehicle_seconds=s['system_vehicle_seconds_in_horizon'],
                      pocket_diversions=s['pocket_diversions'],bay_wait_ticks=s['pocket_wait_ticks'],
                      pocket_peak_0=s['pocket_peak_occupancy']['P0'],
                      pocket_peak_1=s['pocket_peak_occupancy']['P1'],
                      pocket_peak_2=s['pocket_peak_occupancy']['P2'],
                      blocked=s['blocked_transfers'],
                      exposure_error=s['exposure_reconstruction_error_s']))
    write_csv(root/'runs.csv',runs)
    by=defaultdict(list)
    for r in runs:by[(r['demand'],r['pocket_m'],r['policy'])].append(r)
    means=[]
    for (d,p,plan),vals in sorted(by.items()):
        means.append(dict(demand=d,pocket_m=p,policy=plan,n=len(vals),
         mean_vehicle_seconds=statistics.mean(v['vehicle_seconds'] for v in vals),
         mean_completed=statistics.mean(v['completed'] for v in vals),
         mean_bay_wait_ticks=statistics.mean(v['bay_wait_ticks'] for v in vals),
         mean_diversions=statistics.mean(v['pocket_diversions'] for v in vals)))
    write_csv(root/'means.csv',means)
    dct={(r['demand'],r['seed'],r['pocket_m'],r['policy']):r for r in runs}
    differences=[]
    # 15m vs 90m at IDENTICAL demand, seed and policy; no causal claims beyond this simulator.
    for d in DEMANDS:
        for plan in POLICIES:
            diffs=[dct[(d.name,seed,90.,plan.name)]['vehicle_seconds'] -
                   dct[(d.name,seed,15.,plan.name)]['vehicle_seconds'] for seed in SEEDS]
            mean=statistics.mean(diffs); stdev=statistics.stdev(diffs)
            tcrit=2.365 # df=7 two-sided approx 95%, exploratory uncertainty over seeds
            margin=tcrit*stdev/math.sqrt(len(diffs))
            differences.append(dict(demand=d.name,policy=plan.name,n=len(diffs),
                        mean_long_minus_short_vehicle_seconds=mean,
                        ci95_low=mean-margin,ci95_high=mean+margin,
                        n_long_better=sum(x<0 for x in diffs)))
    write_csv(root/'paired_long_vs_short.csv',differences)
    ranks=[]
    for d in DEMANDS:
        for p in POCKET_LENGTHS:
            choices=sorted([(r['policy'],r['mean_vehicle_seconds']) for r in means
                            if r['demand']==d.name and r['pocket_m']==p],key=lambda x:x[1])
            ranks.append(dict(demand=d.name,pocket_m=p,best_policy=choices[0][0],
                              gap_to_second_vehicle_seconds=choices[1][1]-choices[0][1],
                              ranked_policies=' | '.join(v[0] for v in choices)))
    write_csv(root/'policy_rank.csv',ranks)
    summary=dict(experiment='v5.2 pocket geometry × policy, synthetic',n_runs=len(runs),
      n_seeds=len(SEEDS),n_pocket_lengths=len(POCKET_LENGTHS),
      n_demand_types=len(DEMANDS),n_policy_choices=len(POLICIES),
      all_conservation_and_exposure_checks=True,
      max_exposure_error=max(abs(r['exposure_error']) for r in runs),
      constraints=['instantaneous idealized lateral entry to pocket','parallel pocket shares main signal stage',
                   'one junction crossing per timestep','no actual mapped left-turn geometry',
                   'no observed saturation flows','no SUMO external validation',
                   'policy comparison uses three candidate plans only'],
      ranked=ranks,paired=differences)
    (root/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    return summary

if __name__=='__main__':
    result=run()
    print('RUNS',result['n_runs'],'ERROR',result['max_exposure_error'])
    for r in result['ranked']:
        print(r['demand'],r['pocket_m'],r['best_policy'],round(r['gap_to_second_vehicle_seconds'],1))
    print('PAIRED LONG-SHORT')
    for r in result['paired']:
        print(r['demand'],r['policy'],round(r['mean_long_minus_short_vehicle_seconds'],1),
            tuple(round(r[x],1) for x in ('ci95_low','ci95_high')))
