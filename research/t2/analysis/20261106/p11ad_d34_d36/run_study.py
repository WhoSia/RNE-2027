import csv, hashlib, json, sys
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from refinement_reference import run as refinement
from sensor_court import run_case, aggregate

res=ROOT/'results';res.mkdir(exist_ok=True)
dts=[1.,.5,.25,.125,.0625,.03125]
ref=[{k:v for k,v in refinement(dt).items() if k!='trace'} for dt in dts]
rows=[]
# Fixed, perfect detector, and 20%/50% misses with 1-tick observation delay.
# Separate development and held-out seed sets. No tuning after holdout.
for cohort,seeds in [('development',(301,303,305,307)),('holdout',(401,403,405,407))]:
 for n,h in [(18,3),(28,2),(40,1)]:
  for seed in seeds:
   for mode,noise,delay in [('fixed10',0,0),('actuated',0,0),('actuated',.2,1),('actuated',.5,1)]:
    z=run_case(seed,n,h,mode,noise,delay)
    z['cohort']=cohort
    rows.append(z)
summary={}
for cohort in ('development','holdout'):
 summary[cohort]=aggregate([r for r in rows if r['cohort']==cohort])
with (res/'d34_refinement.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['dt_s','exit_time_s','steps']);w.writeheader();w.writerows(ref)
with (res/'d36_sensor_per_seed.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with (res/'d36_sensor_summary.csv').open('w',newline='') as f:
 s=[{'cohort':c,**r} for c,entries in summary.items() for r in entries]
 w=csv.DictWriter(f,fieldnames=list(s[0]));w.writeheader();w.writerows(s)
report={'d34':ref,'d36':summary,'limitations':['d34 is a separate single-car integrator; NOT original T2 convergence','d36 observation is queue proxy, not an authentic traffic detector','model internal results only; no SUMO/field validation','no tuning performed on holdout']}
(res/'results.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'d34':ref,'holdout':summary['holdout']},indent=2))
