"""Independent synthetic holdout seed replication, no field-data inference."""
from pathlib import Path
import csv, math, statistics, json
from collections import defaultdict
from network_v52 import PocketGeometry,DEMANDS,PLANS,make_arrivals,simulate
ROOT=Path(__file__).parent
HOLDOUT=(211,233,257,269,307,331,353,389)
LENGTHS=(15.,90.)
POLICIES=PLANS[:3]

def run():
 rows=[]
 for demand in DEMANDS:
  for seed in HOLDOUT:
   a=make_arrivals(demand,seed,260.)
   for length in LENGTHS:
    for p in POLICIES:
     s=simulate(p,a,440.,pockets=PocketGeometry((length,length,0.)))['summary']
     rows.append({'demand':demand.name,'seed':seed,'pocket_m':length,'policy':p.name,
      'generated':s['generated'],'completed':s['completed'],
      'vehicle_seconds':s['system_vehicle_seconds_in_horizon'],
      'bay_wait_ticks':s['pocket_wait_ticks'],
      'exposure_error':s['exposure_reconstruction_error_s']})
 with (ROOT/'heldout_runs.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 look={(r['demand'],r['seed'],r['pocket_m'],r['policy']):r for r in rows}
 paired=[];rankings=[]
 for d in DEMANDS:
  for p in POLICIES:
   vals=[look[(d.name,seed,90.,p.name)]['vehicle_seconds']-
         look[(d.name,seed,15.,p.name)]['vehicle_seconds'] for seed in HOLDOUT]
   mu=statistics.mean(vals);sd=statistics.stdev(vals)
   margin=2.365*sd/math.sqrt(len(vals))
   paired.append({'demand':d.name,'policy':p.name,'mean_diff_vehicle_seconds':mu,
                  'ci95_low':mu-margin,'ci95_high':mu+margin,'n_long_better':sum(x<0 for x in vals),
                  'n':len(vals)})
  for length in LENGTHS:
   averages={p.name:statistics.mean(look[(d.name,seed,length,p.name)]['vehicle_seconds'] for seed in HOLDOUT) for p in POLICIES}
   rankings.append({'demand':d.name,'pocket_m':length,'optimal_of_three':min(averages,key=averages.get),**averages})
 for name,arr in [('heldout_paired.csv',paired),('heldout_policy_rank.csv',rankings)]:
  with (ROOT/name).open('w',newline='',encoding='utf-8') as f:
   w=csv.DictWriter(f,fieldnames=list(arr[0]));w.writeheader();w.writerows(arr)
 out={'runs':len(rows),'holdout_seeds':HOLDOUT,'paired_results':paired,'policy_rankings':rankings,
      'max_exposure_error':max(abs(r['exposure_error']) for r in rows)}
 (ROOT/'heldout_summary.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
 return out
if __name__=='__main__':
 r=run();print('runs',r['runs']);
 for x in r['paired_results']:print(x['demand'],x['policy'],round(x['mean_diff_vehicle_seconds'],1),round(x['ci95_low'],1),round(x['ci95_high'],1),x['n_long_better'])
 print('rankings',[(x['demand'],x['pocket_m'],x['optimal_of_three']) for x in r['policy_rankings']])
