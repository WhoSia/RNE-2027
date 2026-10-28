"""T2 spatial cellular prototype; 25-ft cell, 1-s step, no VISSIM calibration.
Actual simulated x(t) coordinates, NOT empirically observed trajectories.
Run: python research/t2/spatial_model.py
"""
from dataclasses import dataclass
from collections import deque, Counter
import random, json, csv
from pathlib import Path

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

def simulate(c=Config(), trace=(385,470)):
    assert c.storage_ft>0 and c.storage_ft%25==0
    assert c.approach_ft>c.storage_ft+50
    cells=c.approach_ft//25
    bay_cells=c.storage_ft//25
    fork=-bay_cells-1
    rng=random.Random(c.seed)
    generated=[]
    for t in range(c.duration):
        count=(t+1)*c.demand_vph//3600-t*c.demand_vph//3600
        for _ in range(count):
            left=rng.random()<c.left_fraction
            lane='inner' if left or rng.random()>=c.outer_straight_fraction else 'outer'
            generated.append({'id':len(generated),'t':t,'route':'L' if left else 'S','lane':lane,'x':-cells,'bay_at':None,'exit_at':None})
    lanes={'inner':[],'outer':[],'bay':[]}
    waiting={'inner':deque(),'outer':deque()}
    logs=[];paths=[];counts=Counter();last={k:-100 for k in lanes}
    index=0
    for t in range(c.duration):
        while index<len(generated) and generated[index]['t']<=t:
            v=generated[index];waiting[v['lane']].append(v);index+=1
        sg=(t%c.cycle)<c.green
        lg=(t%c.cycle)<c.left_green
        for lane,active in (('bay',lg),('inner',sg),('outer',sg)):
            row=lanes[lane]
            if active and row and row[0]['x']>=-c.speed_cells and t-last[lane]>=2:
                if lane!='inner' or row[0]['route']=='S':
                    v=row.pop(0);v['exit_at']=t;v['x']=0
                    counts['exit_'+lane]+=1;last[lane]=t
                    logs.append((t,v['id'],'exit_'+lane,0))
        for lane in ('bay','outer','inner'):
            row=lanes[lane]
            for i,v in enumerate(row):
                front=row[i-1]['x'] if i else 0
                limit=front-c.gap_cells-1
                next_x=min(v['x']+c.speed_cells,limit)
                if lane=='inner' and v['route']=='L':
                    next_x=min(next_x,fork)
                v['x']=max(v['x'],next_x)
        shared=lanes['inner'];bay=lanes['bay']
        if shared and shared[0]['route']=='L' and shared[0]['x']>=fork:
            if not bay or bay[-1]['x']>=-bay_cells+c.gap_cells+1:
                v=shared.pop(0);v['lane']='bay';v['x']=-bay_cells;v['bay_at']=t
                bay.append(v);logs.append((t,v['id'],'enter_bay',-25*bay_cells))
            elif sg:
                counts['bay_block_green_s']+=1
        for lane in ('inner','outer'):
            if waiting[lane] and (not lanes[lane] or lanes[lane][-1]['x']>=-cells+c.gap_cells+1):
                v=waiting[lane].popleft();v['x']=-cells
                lanes[lane].append(v);logs.append((t,v['id'],'enter_road',-25*cells))
        for lane,row in lanes.items():
            assert all(row[i]['x']-row[i+1]['x']>=c.gap_cells+1 for i in range(len(row)-1))
            assert len(set(v['id'] for v in row))==len(row)
        if trace[0]<=t<=trace[1]:
            for lane,row in lanes.items():
                paths.extend((t,v['id'],lane,v['route'],v['x']*25) for v in row if v['x']>=-48)
    counts['arrivals']=len(generated)
    counts['exits']=sum(counts['exit_'+lane] for lane in lanes)
    counts['remaining']=sum(map(len,lanes.values()))+sum(map(len,waiting.values()))
    assert counts['arrivals']==counts['exits']+counts['remaining']
    return dict(stats=dict(counts),events=logs,trajectories=paths,vehicles=generated)

def save(result,dest):
    dest=Path(dest);dest.mkdir(parents=True,exist_ok=True)
    (dest/'metrics.json').write_text(json.dumps(result['stats'],indent=2))
    for file,header,rows in [
        ('events.csv',['t_s','vehicle_id','event','x_ft'],result['events']),
        ('trajectories.csv',['t_s','vehicle_id','lane','movement','x_ft'],result['trajectories']),
        ('vehicles.csv',['id','arrival_s','movement','last_lane','bay_entry_s','exit_s'],
         ((v['id'],v['t'],v['route'],v['lane'],v['bay_at'],v['exit_at']) for v in result['vehicles']))
    ]:
        with (dest/file).open('w',newline='',encoding='utf-8') as f:
            writer=csv.writer(f);writer.writerow(header);writer.writerows(rows)

if __name__=='__main__':
    for ft in (100,500):
        result=simulate(Config(storage_ft=ft))
        save(result,Path('outputs')/f'{ft}ft')
        print(ft,result['stats'])
