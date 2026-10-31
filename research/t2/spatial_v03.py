"""T2 split-diverge cellular prototype v0.3 (25 ft cells, 1 s steps).
Research simulation only; not a calibrated traffic model.
"""
from dataclasses import dataclass
from collections import deque,Counter
import random

@dataclass(frozen=True)
class Config:
    duration:int=4200
    cycle:int=150
    green:int=60
    left_green:int=54
    storage_ft:int=100
    approach_ft:int=2000
    demand_vph:int=3000
    left_fraction:float=.4
    outer_straight_fraction:float=.55
    seed:int=42
    speed_cells:int=2
    gap_cells:int=1

def simulate(c=Config()):
    assert c.storage_ft>0 and c.storage_ft%25==0 and c.approach_ft>c.storage_ft+50
    cells=c.approach_ft//25
    bay_cells=c.storage_ft//25
    fork=-bay_cells-1
    rng=random.Random(c.seed)
    generated=[]
    for t in range(c.duration):
        count=(t+1)*c.demand_vph//3600-t*c.demand_vph//3600
        for _ in range(count):
            left=rng.random()<c.left_fraction
            lane='upstream' if left or rng.random()>=c.outer_straight_fraction else 'outer'
            generated.append({'id':len(generated),'t':t,'route':'L' if left else 'S','lane':lane,'x':-cells,'exit_at':None})
    lanes={'upstream':[],'downstream':[],'outer':[],'bay':[]}
    waiting={'upstream':deque(),'outer':deque()}
    index=0
    counts=Counter()
    last={x:-100 for x in ('downstream','outer','bay')}
    events=[]

    def advance(row,stop):
        for i,v in enumerate(row):
            front=row[i-1]['x'] if i else stop
            v['x']=min(v['x']+c.speed_cells,front-c.gap_cells-1)

    for t in range(c.duration):
        while index<len(generated) and generated[index]['t']<=t:
            v=generated[index]
            waiting[v['lane']].append(v)
            index+=1
        sg=t%c.cycle<c.green
        lg=t%c.cycle<c.left_green
        for lane,active in (('bay',lg),('downstream',sg),('outer',sg)):
            row=lanes[lane]
            if active and row and row[0]['x']>=-c.speed_cells and t-last[lane]>=2:
                v=row.pop(0)
                v['exit_at']=t
                counts['exit_'+lane]+=1
                last[lane]=t
                events.append((t,v['id'],'exit_'+lane))
        for lane in ('bay','downstream','outer'):
            advance(lanes[lane],0)
        upstream=lanes['upstream']
        bay=lanes['bay']
        down=lanes['downstream']
        for i,v in enumerate(upstream):
            front=upstream[i-1]['x'] if i else fork+c.gap_cells+1
            v['x']=min(v['x']+c.speed_cells,front-c.gap_cells-1)
        if upstream and upstream[0]['x']>=fork:
            v=upstream[0]
            target=bay if v['route']=='L' else down
            target_x=-bay_cells if v['route']=='L' else fork+1
            if not target or target[-1]['x']>=target_x+c.gap_cells+1:
                upstream.pop(0)
                v['x']=target_x
                v['lane']='bay' if v['route']=='L' else 'downstream'
                target.append(v)
                events.append((t,v['id'],'transfer_'+v['lane']))
            else:
                counts['fork_block_s']+=1
        for lane in ('upstream','outer'):
            if waiting[lane] and (not lanes[lane] or lanes[lane][-1]['x']>=-cells+c.gap_cells+1):
                v=waiting[lane].popleft()
                v['x']=-cells
                lanes[lane].append(v)
        for row in lanes.values():
            assert all(row[i]['x']-row[i+1]['x']>=c.gap_cells+1 for i in range(len(row)-1))
        assert len({v['id'] for row in lanes.values() for v in row})==sum(len(row) for row in lanes.values())
    counts['arrivals']=len(generated)
    counts['exits']=sum(v for k,v in counts.items() if k.startswith('exit_'))
    counts['remaining']=sum(map(len,lanes.values()))+sum(map(len,waiting.values()))
    assert counts['arrivals']==counts['exits']+counts['remaining']
    return dict(stats=dict(counts),events=events)

if __name__=='__main__':
    for seed in range(10):
        print(seed,[simulate(Config(seed=seed,storage_ft=ft))['stats']['exits'] for ft in (100,200,400,500)])
