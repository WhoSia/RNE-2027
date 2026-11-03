"""Audit old v5.6 event logs under hypothetical temporal occupancy (synthetic)."""
from pathlib import Path
from network_v56 import simulate,make_arrivals,DEMANDS,PLANS,ParallelSignalPlan,PocketGeometry,GEOMETRY_MOVEMENTS,GEOMETRY_GRAPH
from temporal_conflicts import Occupancy,audit
import csv,json
HERE=Path(__file__).resolve().parent
def main():
    rows=[]
    for demand in DEMANDS:
        for seed in (*range(300,312),*range(500,512)):
            a=make_arrivals(demand,seed,arrive_until=180.)
            old=simulate(ParallelSignalPlan(PLANS[0],12),a,horizon=300.,
                         pockets=PocketGeometry((30,30,0)))
            for seconds in (2.,5.):
                ev=[Occupancy(e['junction'],GEOMETRY_MOVEMENTS[e['movement']],
                              e['t_s'],e['t_s']+seconds,e['id']) for e in old['crossings']]
                result=audit(ev,GEOMETRY_GRAPH)
                rows.append(dict(demand=demand.name,seed=seed,hypothetical_occupancy_s=seconds,
                                 crossings=result['events'],
                                 cross_movement_overlap_pairs=result['conflicting_intervals']))
    with (HERE/'historical_interval_violations.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    summary=[]
    for d in DEMANDS:
        for seconds in (2.,5.):
            group=[x for x in rows if x['demand']==d.name and x['hypothetical_occupancy_s']==seconds]
            summary.append(dict(demand=d.name,occupancy_s=seconds,n=len(group),
                violation_pairs=sum(x['cross_movement_overlap_pairs'] for x in group),
                seeds_with_at_least_one=sum(x['cross_movement_overlap_pairs']>0 for x in group)))
    (HERE/'historical_audit_summary.json').write_text(json.dumps(summary,indent=2))
    print(summary)
if __name__=='__main__':main()
