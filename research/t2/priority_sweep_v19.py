"""Explore receiving-group priority interaction without an upstream bay.
2 receiving structures x 3 merge priorities x 2 common space levels
x 3 initial L queues x 2 L-green levels x 8 paired input seeds = 576 cases.
"""
from dataclasses import replace
from itertools import product
from pathlib import Path
from statistics import mean
from collections import defaultdict
import csv,json,random
from link_supply_v19 import TwoMovementLink,ReceivingPolicy


def run():
    result=[]
    for seed in range(8):
        rng=random.Random(seed+404)
        # shared random incoming stream across ALL interventions for this seed
        arrival_stream=[(int(rng.random()<.32),int(rng.random()<.20)) for _ in range(360)]
        for shared,priority,capacity,qL,gL in product((False,True),
                  ('S_first','L_first','alternate'),(1,4),(0,20,40),(0,20)):
            policy=ReceivingPolicy(capacity_S=capacity,capacity_L=capacity,
                cycle_s=60,green_S=45,green_L=gL,headway_S=3,headway_L=3,
                shared_receiver=shared,admission_priority=priority)
            model=TwoMovementLink(policy,initial_S=10,initial_L=qL)
            for t,(s,l) in enumerate(arrival_stream):model.tick(t,s,l)
            r=model.result()
            assert all(r['generated'][m]==r['completed'][m]+r['upstream'][m]+r['downstream'][m] for m in 'SL')
            result.append(dict(seed=seed,shared=shared,priority=priority,capacity=capacity,
              initial_L=qL,green_L=gL,through=r['completed']['S'],left=r['completed']['L'],
              through_blocked=r['blocked_attempts']['S'],left_blocked=r['blocked_attempts']['L']))
    assert len(result)==576
    return result


def summary(rows):
    d=defaultdict(list)
    for r in rows:d[(r['shared'],r['priority'],r['capacity'],r['initial_L'],r['green_L'])].append(r)
    return [dict(shared=k[0],priority=k[1],capacity=k[2],initial_L=k[3],green_L=k[4],
         mean_S=mean(q['through'] for q in v),mean_L=mean(q['left'] for q in v),
         mean_blocked_S=mean(q['through_blocked'] for q in v)) for k,v in sorted(d.items())]

if __name__=='__main__':
    rows=run();dest=Path(__file__).parent/'results';dest.mkdir(exist_ok=True)
    with (dest/'priority_576_v19.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    out=summary(rows);(dest/'priority_summary_v19.json').write_text(json.dumps(out,indent=2))
    print('run count',len(rows))
    for shared,priority in product((False,True),('S_first','L_first','alternate')):
        x=next(z for z in out if z['shared']==shared and z['priority']==priority and z['capacity']==1 and z['initial_L']==20 and z['green_L']==0)
        print('shared',shared,'priority',priority,'completed_S',x['mean_S'],'completed_L',x['mean_L'])
