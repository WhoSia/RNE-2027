"""Synthetic v5.8 factorial, fixed OD matched by seed; no field claims."""
from network_v58 import make_arrivals,DEMANDS,PLANS,PocketGeometry,ParallelSignalPlan,simulate
from path_occupancy import PathTimeModel
from pathlib import Path
from collections import defaultdict
import csv,json,statistics,math
OUT=Path(__file__).resolve().parent
MODELS={
 'zero':dict(occupancy_s=0.),
 'fixed3':dict(occupancy_s=3.),
 'path_floor4':dict(path_time=PathTimeModel(minimum_cross_speed_mps=4.)),
 'path_floor6':dict(path_time=PathTimeModel(minimum_cross_speed_mps=6.)),
}

def run(seeds,tag):
 rows=[]
 for demand in DEMANDS:
  for seed in seeds:
   arrivals=make_arrivals(demand,seed,arrive_until=150.)
   for model,kwargs in MODELS.items():
    result=simulate(ParallelSignalPlan(PLANS[0],12),arrivals,horizon=260.,pockets=PocketGeometry((30.,30.,0.)),**kwargs)
    s=result['summary']
    rows.append(dict(cohort=demand.name,seed=seed,model=model,generated=s['generated'],completed=s['completed'],
                     exposure_vehicle_s=s['system_vehicle_seconds_in_horizon'],conflicts=s['occupancy_conflicts'],
                     events=s['occupancy_interval_events'],mvt_duration_json=json.dumps(s['occupancy_mean_by_movement_s'],sort_keys=True)))
 fields=list(rows[0]);with_csv=OUT/f'{tag}_runs.csv'
 with with_csv.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 by={(r['cohort'],r['seed'],r['model']):r for r in rows};pairs=[];summary=[]
 for cohort in (d.name for d in DEMANDS):
  for model in MODELS:
   if model=='zero':continue
   deltas=[];comps=[]
   for seed in seeds:
    a,b=by[cohort,seed,'zero'],by[cohort,seed,model]
    assert a['generated']==b['generated']
    delta=b['exposure_vehicle_s']-a['exposure_vehicle_s']
    pairs.append(dict(cohort=cohort,seed=seed,comparison=model,delta_exposure_vehicle_s=delta,delta_completed=b['completed']-a['completed']))
    deltas.append(delta);comps.append(b['completed']-a['completed'])
   summary.append(dict(cohort=cohort,comparison=model,n=len(deltas),mean_delta_exposure_vehicle_s=statistics.mean(deltas),
                       sd_delta=statistics.stdev(deltas),positive=sum(x>0 for x in deltas),mean_delta_completed=statistics.mean(comps)))
 for n,items in ((f'{tag}_paired.csv',pairs),(f'{tag}_summary.csv',summary)):
  with (OUT/n).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(items[0]));w.writeheader();w.writerows(items)
 (OUT/f'{tag}_summary.json').write_text(json.dumps(dict(date='20261103',runs=len(rows),seeds=list(seeds),models=list(MODELS),summary=summary),indent=2))
 return summary
if __name__=='__main__':
 for tag,seeds in [('exploration',range(600,616)),('holdout',range(800,808))]:
  print(tag,run(list(seeds),tag))
