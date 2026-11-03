"""Matched 0/2/5s crossing occupancy sensitivity experiment (synthetic)."""
from pathlib import Path
from collections import defaultdict
from network_v57 import make_arrivals,DEMANDS,PLANS,PocketGeometry,ParallelSignalPlan,simulate
import csv,json,math,statistics
HERE=Path(__file__).resolve().parent
DURATIONS=(0.,2.,5.)

def run(start=300,nseeds=12,tag='exploration'):
    rows=[]
    for d in DEMANDS:
        for seed in range(start,start+nseeds):
            a=make_arrivals(d,seed,arrive_until=180.)
            for duration in DURATIONS:
                x=simulate(ParallelSignalPlan(PLANS[0],12),a,horizon=300.,
                           pockets=PocketGeometry((30,30,0)),occupancy_s=duration)['summary']
                rows.append(dict(demand=d.name,seed=seed,occupancy_s=duration,
                                 generated=x['generated'],completed=x['completed'],
                                 vehicle_seconds=x['system_vehicle_seconds_in_horizon'],
                                 interval_events=x['occupancy_interval_events'],
                                 interval_conflicts=x['occupancy_conflicts'],
                                 paired_parallel_slots=x['parallel_crossing_slots'],
                                 blocked=x['blocked_transfers'],
                                 remaining=x['remaining_inside']+x['pending_boundary']))
    def save_csv(name,content):
        with (HERE/name).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(content[0]));w.writeheader();w.writerows(content)
    save_csv(f'{tag}_runs.csv',rows)
    index={(r['demand'],r['seed'],r['occupancy_s']):r for r in rows}
    paired=[];agg=[]
    for d in DEMANDS:
        for duration in DURATIONS[1:]:
            delta=[];counts=[]
            for seed in range(start,start+nseeds):
                x=index[(d.name,seed,0.)];y=index[(d.name,seed,duration)]
                assert x['generated']==y['generated']
                value=y['vehicle_seconds']-x['vehicle_seconds']
                delta.append(value);counts.append(y['completed']-x['completed'])
                paired.append(dict(demand=d.name,seed=seed,occupancy_s=duration,
                                   delta_vehicle_seconds=value,delta_completed=counts[-1]))
            mean=statistics.mean(delta);err=2.201*statistics.stdev(delta)/math.sqrt(nseeds) if nseeds==12 else None
            agg.append(dict(demand=d.name,occupancy_s=duration,n=nseeds,
                            mean_delta_vehicle_seconds=mean,
                            approx_ci95_low=mean-err if err is not None else None,
                            approx_ci95_high=mean+err if err is not None else None,
                            increases=sum(v>0 for v in delta),decreases=sum(v<0 for v in delta),
                            mean_delta_completed=statistics.mean(counts)))
    save_csv(f'{tag}_paired.csv',paired)
    save_csv(f'{tag}_summary.csv',agg)
    (HERE/f'{tag}_summary.json').write_text(json.dumps(dict(tag=tag,simulation_count=len(rows),aggregate=agg),indent=2))
    return agg
if __name__=='__main__':
    print(run(300,12,'exploration'))
    print(run(500,12,'holdout'))
