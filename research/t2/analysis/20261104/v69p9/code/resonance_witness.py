"""Selected P9 convergence witnesses, not fitted or tuned. Original P2 only."""
from __future__ import annotations
import csv,json,sys
from pathlib import Path
from dataclasses import replace
from dt_convergence import SCENARIOS,PLANS,arrivals_for,make_config,run

CASES=(
 ('downstream_side_peak',18.,211,(24.,30.,24.)),
 ('upstream_peak',18.,223,(24.,24.,24.)),
 ('balanced',18.,223,(30.,30.,0.)),
)
DTS=(.5,.4,.25,.2,.125,.1,.0625,.05)

def trace_completions(scenario,storage,seed,plan,dt):
 s=next(q for q in SCENARIOS if q.name==scenario)
 p=next(q for q in PLANS if q.key==plan)
 arr=arrivals_for(s,seed)
 cfg=replace(make_config(p,storage,horizon_s=1200.),dt=dt)
 z=run(cfg,arr)
 if z['summary']['issues'] or not z['summary']['all_completed']:
  raise AssertionError('witness dynamics invalid or censored')
 return z['summary'],{e['id']:e['t'] for e in z['events'] if e['event']=='complete'},len(arr)

def analyze():
 rows=[];by_case=[]
 for scenario,storage,seed,plan in CASES:
  traces={}
  for dt in DTS:
   summ,completion,n=trace_completions(scenario,storage,seed,plan,dt)
   traces[dt]=completion
   rows.append(dict(scenario=scenario,storage_m=storage,seed=seed,policy=str(plan),
                 dt=dt,exposure_vehicle_seconds=summ['exposure_vehicle_seconds'],
                 completed=summ['completed'],unfinished=summ['unfinished'],issues=summ['issues']))
  ref=traces[.05]
  for dt in DTS:
   lag=[traces[dt][vid]-ref[vid] for vid in ref]
   by_case.append(dict(scenario=scenario,storage_m=storage,seed=seed,policy=str(plan),dt=dt,
                       max_abs_vehicle_completion_time_difference_s=max(map(abs,lag)),
                       n_vehicles_60s_apart=sum(abs(x)>=50. for x in lag),
                       compared_vehicle_count=len(ref)))
 return rows,by_case

if __name__=='__main__':
 out=Path(__file__).resolve().parents[1]/'results'
 rows,by_case=analyze()
 for name,a in [('convergence_witness.csv',rows),('completion_trace_differences.csv',by_case)]:
  with (out/name).open('w',encoding='utf-8',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(a[0]));w.writeheader();w.writerows(a)
 print(json.dumps([r for r in rows if r['scenario']=='upstream_peak'],indent=2))
