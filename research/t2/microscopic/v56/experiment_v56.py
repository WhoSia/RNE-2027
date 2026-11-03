"""Matched synthetic factorial of concurrent geometry-compatible junction crossings."""
import csv, json, math, statistics
from collections import defaultdict
from network_v56 import make_arrivals, DEMANDS, PLANS, PocketGeometry, ParallelSignalPlan, simulate

def run(nseeds=24):
    records=[]
    for d in DEMANDS:
        for seed in range(200,200+nseeds):
            arrivals=make_arrivals(d,seed,arrive_until=180.)
            kw=dict(horizon=300.,pockets=PocketGeometry((30.,30.,0.)))
            for window in (0.,12.):
                plan=PLANS[0] if window==0 else ParallelSignalPlan(PLANS[0],window)
                r=simulate(plan,arrivals,**kw)['summary']
                records.append(dict(demand=d.name,seed=seed,parallel_window_s=window,
                    generated=r['generated'],completed=r['completed'],remaining=r['remaining_inside']+r['pending_boundary'],
                    vehicle_seconds=r['system_vehicle_seconds_in_horizon'],
                    parallel_slots=r['parallel_crossing_slots'],blocked=r['blocked_transfers']))
    path='runs.csv'
    with open(path,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    pairs=[];summary=[]
    for d in DEMANDS:
        current=[x for x in records if x['demand']==d.name]
        dct={(x['seed'],x['parallel_window_s']):x for x in current}
        vals=[];completed_delta=[];paired_slots=[]
        for seed in range(200,200+nseeds):
            a,b=dct[(seed,0.)],dct[(seed,12.)]
            assert a['generated']==b['generated']
            delta=b['vehicle_seconds']-a['vehicle_seconds']
            vals.append(delta);completed_delta.append(b['completed']-a['completed']);paired_slots.append(b['parallel_slots'])
            pairs.append(dict(demand=d.name,seed=seed,delta_vehicle_seconds=delta,
                              delta_completed=b['completed']-a['completed'],parallel_slots=b['parallel_slots']))
        m=statistics.mean(vals);sd=statistics.stdev(vals);se=sd/math.sqrt(len(vals))
        summary.append(dict(demand=d.name,n=len(vals),mean_delta_vehicle_seconds=m,
            ci95_low=m-2.069*se,ci95_high=m+2.069*se,
            negative_count=sum(v<0 for v in vals),positive_count=sum(v>0 for v in vals),
            average_parallel_slots=statistics.mean(paired_slots),
            average_delta_completed=statistics.mean(completed_delta)))
    with open('paired.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(pairs[0]));w.writeheader();w.writerows(pairs)
    with open('summary.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
    json.dump(dict(design='3 demands x 24 matched OD seeds x 2 release schedulers',runs=len(records),paired=len(pairs),summary=summary),open('summary.json','w'),indent=2)
    for row in summary:print(row)
if __name__=='__main__':run()
