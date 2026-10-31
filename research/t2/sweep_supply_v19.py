"""Ablation of shared/independent receiving supply, initial L queue and signal phase.
384 scenarios: 2 shared modes x 3 initial L queue x 4 offsets x 2 L greens
x 8 demand seeds. This is standalone, NOT the upstream bay geometry.
"""
from dataclasses import replace
from statistics import mean
from itertools import product
from collections import defaultdict
from pathlib import Path
import random,csv,json
from link_supply_v19 import ReceivingPolicy,TwoMovementLink

def run_design():
    rows=[]
    for seed in range(8):
        rng=random.Random(seed+100)
        stream=[(int(rng.random()<.37), int(rng.random()<.23)) for _ in range(720)]
        for shared,qL,offset,gL in product((False,True),(0,10,30),(0,15,30,45),(0,20)):
            config=ReceivingPolicy(capacity_S=4,capacity_L=4,cycle_s=60,
                green_S=45,green_L=gL,offset_L=offset,shared_receiver=shared)
            eng=TwoMovementLink(config,initial_S=10,initial_L=qL)
            for t,(s,l) in enumerate(stream):eng.tick(t,s,l)
            r=eng.result()
            rows.append({'seed':seed,'shared':shared,'initial_L':qL,'offset_L':offset,
                'green_L':gL,'generated_S':r['generated']['S'],'generated_L':r['generated']['L'],
                'completed_S':r['completed']['S'],'completed_L':r['completed']['L'],
                'remaining_S':r['upstream']['S']+r['downstream']['S'],
                'remaining_L':r['upstream']['L']+r['downstream']['L'],
                'blocked_attempts_S':r['blocked_attempts']['S'],
                'blocked_attempts_L':r['blocked_attempts']['L']})
    assert len(rows)==384
    return rows

def summarize(rows):
    groups=defaultdict(list)
    for r in rows:groups[(r['shared'],r['initial_L'],r['offset_L'],r['green_L'])].append(r)
    return [dict(shared=k[0],initial_L=k[1],offset_L=k[2],green_L=k[3],
                mean_S=mean(x['completed_S'] for x in v),
                mean_L=mean(x['completed_L'] for x in v),
                mean_denied_S=mean(x['blocked_attempts_S'] for x in v))
            for k,v in sorted(groups.items())]

if __name__=='__main__':
    r=run_design();root=Path(__file__).parent/'results';root.mkdir(exist_ok=True)
    with (root/'shared_supply_384_v19.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(r[0]));w.writeheader();w.writerows(r)
    (root/'shared_supply_summary_v19.json').write_text(json.dumps(summarize(r),indent=2))
    print('run count',len(r))
    for k in ((False,30,0,0),(True,30,0,0),(False,30,0,20),(True,30,0,20)):
        x=next(y for y in summarize(r) if (y['shared'],y['initial_L'],y['offset_L'],y['green_L'])==k)
        print(k,round(x['mean_S'],2),round(x['mean_L'],2),round(x['mean_denied_S'],2))
