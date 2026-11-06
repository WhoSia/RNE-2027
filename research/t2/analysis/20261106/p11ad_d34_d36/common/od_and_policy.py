"""D29-D30: small OD generator and off-line fixed-signal candidate court.
Exploratory candidates are not traffic-control recommendations; no live deployment.
"""
from __future__ import annotations
from dataclasses import dataclass
from statistics import mean
from random import Random
from micro_world import Vehicle, Road, FixedSignal, run


def make_od_demand(paths:dict[str,tuple[str,...]], n:int, seed:int, *,headway_s:int=2, bus_every:int=0)->list[Vehicle]:
    if not paths or n<0 or headway_s<1:raise ValueError('invalid OD config')
    rng=Random(seed)
    names=sorted(paths)
    out=[]
    for i in range(n):
        choice=names[rng.randrange(len(names))]
        isbus=bool(bus_every and i%bus_every==0)
        out.append(Vehicle(str(i),paths[choice],i*headway_s+rng.randrange(headway_s),
                           length_m=10.0 if isbus else 4.5,
                           desired_mps=6.0 if isbus else 10.0,
                           accel_mps2=1.1 if isbus else 2.0,
                           bus_dwell_s=2 if isbus else 0,
                           stop_road='B' if isbus and 'B' in paths[choice] else None))
    return out

def court(*, seeds=(101,103,107,109),green_options=(6,10,14),horizon=260,holdout=(211,223)):
    """Competing approaches, fixed plans, held-out synthetic demand.

    This is *not* a safety-qualified signal timing or field-deployable controller.
    Both approaches have synthetic 2-second clearance before switching.
    """
    roads={'A':Road('A',24,1,8,('S',)), 'C':Road('C',24,1,8,('S',)),
           'S':Road('S',25,1,8)}
    candidates={}
    for green in green_options:
        if not 3<=green<=17:raise ValueError('green outside synthetic envelope')
        plans={'A':FixedSignal(24,green,0),
               'C':FixedSignal(24,20-green,green+2)}
        cohorts=[]
        for seed in tuple(seeds)+tuple(holdout):
            vs=make_od_demand({'east':('A','S'),'north':('C','S')},28,seed,headway_s=2,bus_every=7)
            z=run(roads,vs,horizon_s=horizon,signals=plans)
            finished=len(z.finishes);uncompleted=len(vs)-finished
            durations=[z.finishes[v.identity]-v.depart_s for v in vs if v.identity in z.finishes]
            subgroup={}
            for road in ('A','C'):
                vals=[z.finishes[v.identity]-v.depart_s for v in vs
                      if v.route[0]==road and v.identity in z.finishes]
                subgroup[road]={'completed':len(vals),'mean_duration_s':mean(vals) if vals else None}
            cohorts.append({'seed':seed,'completed':finished,'uncompleted':uncompleted,
                            'mean_duration_s':mean(durations) if durations else None,
                            'max_source_queue':z.max_queue,
                            'collision_violations':z.collision_violations,
                            'by_approach':subgroup})
        candidates[green]=cohorts
    train=[];hold=[]
    for green,cohorts in candidates.items():
        for label,records,seed_set in [('train',train,seeds),('holdout',hold,holdout)]:
            rows=[r for r in cohorts if r['seed'] in seed_set]
            if not rows or any(r['uncompleted'] for r in rows):
                records.append({'green_s':green,'cohort':label,'status':'CENSORED','mean_duration_s':None,
                                'mean_source_queue':mean(r['max_source_queue'] for r in rows),
                                'approach_disparity_s':None})
            else:
                disparities=[abs(r['by_approach']['A']['mean_duration_s']-r['by_approach']['C']['mean_duration_s'])
                             for r in rows if all(r['by_approach'][k]['mean_duration_s'] is not None for k in ('A','C'))]
                records.append({'green_s':green,'cohort':label,'status':'COMPLETE',
                                'mean_duration_s':mean(r['mean_duration_s'] for r in rows),
                                'mean_source_queue':mean(r['max_source_queue'] for r in rows),
                                'approach_disparity_s':mean(disparities) if disparities else None})
    return {'train':train,'holdout':hold,'raw':candidates,'policy_status':'SYNTHETIC_OFFLINE_ONLY'}
