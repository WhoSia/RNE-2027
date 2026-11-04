"""P9 experimental fixed-order ablation; one transition rule only, original P2 untouched."""
import sys,csv,json
from pathlib import Path
from dataclasses import replace
from importlib.util import spec_from_file_location,module_from_spec
from dt_convergence import SCENARIOS,PLANS,arrivals_for,make_config,run as original_run

fixpath=Path(__file__).resolve().parents[1]/'derived'/'corridor_tick_safe.py'
spec=spec_from_file_location('corridor_tick_safe',fixpath)
mod=module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)

def eval_run(engine,plan,arr,storage,dt):
 cfg=replace(make_config(plan,storage,horizon_s=1200.),dt=dt)
 r=engine(cfg,arr);z=r['summary']
 if z['issues'] or z['unfinished']!=0:raise AssertionError('invalid/censored ablation')
 last_exit={};overlap=[]
 for e in r['events']:
  if e['event']=='connector_exit':last_exit[e['j']]=e['t']
  elif e['event']=='connector_enter' and e['j'] in last_exit and e['t']<last_exit[e['j']]-1e-8:
   overlap.append(last_exit[e['j']]-e['t'])
 return z['exposure_vehicle_seconds'],len(overlap)

def run_cases():
 target=(('upstream_peak',18.,223,(24.,24.,24.)),('downstream_side_peak',18.,211,(24.,30.,24.)),('balanced',18.,223,(30.,30.,0.)))
 rows=[]
 for sc,storage,seed,key in target:
  s=next(x for x in SCENARIOS if x.name==sc);p=next(x for x in PLANS if x.key==key);a=arrivals_for(s,seed)
  for dt in (.5,.4,.25,.2,.125,.1,.0625,.05):
   for label,engine in (('original',original_run),('release-gated',mod.run)):
    value,overlaps=eval_run(engine,p,a,storage,dt)
    rows.append(dict(scenario=sc,storage_m=storage,seed=seed,plan=str(key),engine=label,dt=dt,
                     exposure_vehicle_seconds=value,temporal_overlap_count=overlaps))
 return rows
if __name__=='__main__':
 out=Path(__file__).resolve().parents[1]/'results';rows=run_cases()
 with (out/'tick_release_ablation.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 for s in ('upstream_peak','downstream_side_peak','balanced'):
  print(s,[(x['engine'],x['dt'],round(x['exposure_vehicle_seconds'],2),x['temporal_overlap_count']) for x in rows if x['scenario']==s])
