"""T2 v0.8 finite-storage two-movement queue comparator.

MODEL NOT CALIBRATED TO A FIELD INTERSECTION. A shared FIFO feeder with a
finite L pocket and a finite S downstream buffer. No overtaking, acceleration,
late lane changes, multiple through lanes, or travel-time geometry. Each
step discharges first, then admits at most one head vehicle into its branch.
The upstream backlog is outside the explicitly represented storage segment.
"""
from dataclasses import dataclass, replace, asdict
from collections import deque, Counter
import random, json, math

@dataclass(frozen=True)
class Setup:
    duration: int = 1800
    cycle: int = 120
    left_green: int = 35
    through_green: int = 50
    clearance: int = 3
    leading: bool = True
    left_length_m: float = 28.0
    through_length_m: float = 56.0
    pitch_m: float = 7.0
    demand_vph: int = 1500
    left_share: float = 0.30
    seed: int = 0
    discharge_headway: int = 2

def validate(c):
    if c.duration<1 or c.cycle<1 or min(c.left_green,c.through_green,c.discharge_headway)<1:
        raise ValueError('invalid timing')
    if c.clearance<0 or c.left_green+c.through_green+2*c.clearance>c.cycle:
        raise ValueError('overlapping protected phases')
    if min(c.left_length_m,c.through_length_m)<0 or c.pitch_m<=0:
        raise ValueError('invalid geometry')
    if c.demand_vph<0 or not 0<=c.left_share<=1:
        raise ValueError('invalid demand')
    return math.floor(c.left_length_m/c.pitch_m+1e-9), math.floor(c.through_length_m/c.pitch_m+1e-9)

def signal(c,t):
    x=t%c.cycle
    first='L' if c.leading else 'S'
    second='S' if c.leading else 'L'
    width=c.left_green if c.leading else c.through_green
    if x<width: return first
    x-=width
    if x<c.clearance: return '-'
    x-=c.clearance
    width=c.through_green if c.leading else c.left_green
    return second if x<width else '-'

def generated_stream(c):
    rng=random.Random(c.seed)
    return tuple('L' if rng.random()<c.left_share else 'S'
                 for _ in range(c.duration*c.demand_vph//3600))

def run(c=Setup(), stream=None, *, pocket_infinite=False):
    cap_l,cap_s=validate(c)
    if stream is None: stream=generated_stream(c)
    if len(stream)!=c.duration*c.demand_vph//3600 or any(x not in ('L','S') for x in stream):
        raise ValueError('stream not compatible with setup')
    external=deque(); queues={'L':deque(),'S':deque()}; last={'L':-10**9,'S':-10**9}
    count=Counter(); curves=[]; index=0
    for t in range(c.duration):
        target=(t+1)*c.demand_vph//3600
        while index<target:
            external.append((index,stream[index]));index+=1
        phase=signal(c,t)
        if phase in queues and queues[phase] and t-last[phase]>=c.discharge_headway:
            queues[phase].popleft();last[phase]=t;count[f'exit_{phase}']+=1
        if external:
            vehicle=external[0];route=vehicle[1]
            limit=(10**12 if pocket_infinite and route=='L' else cap_l if route=='L' else cap_s)
            if len(queues[route])<limit:
                queues[route].append(external.popleft());count[f'transfer_{route}']+=1
            else:
                count[f'block_{route}_s']+=1
                if phase=='S' and route=='L':count['blocked_during_S_green_s']+=1
        count['max_external']=max(count['max_external'],len(external))
        count['max_L']=max(count['max_L'],len(queues['L']))
        count['max_S']=max(count['max_S'],len(queues['S']))
        exits=count['exit_L']+count['exit_S']
        if index != exits+len(external)+len(queues['L'])+len(queues['S']):
            raise AssertionError(('conservation',t))
        if (not pocket_infinite and len(queues['L'])>cap_l) or len(queues['S'])>cap_s:
            raise AssertionError(('overflow',t))
        if (t+1)%c.cycle==0 or t==c.duration-1:
            curves.append({'end_s':t+1,'L_queue':len(queues['L']),
                'S_queue':len(queues['S']),'external_queue':len(external),
                'exits_L':count['exit_L'],'exits_S':count['exit_S'],
                'blocked_L_s':count['block_L_s'],'blocked_S_s':count['block_S_s']})
    return {'source':'SYNTHETIC_UNCALIBRATED','config':asdict(c),
        'pocket_slots':cap_l,'through_slots':cap_s,'arrivals':index,
        'exits_L':count['exit_L'],'exits_S':count['exit_S'],
        'total_exits':count['exit_L']+count['exit_S'],
        'remaining':len(external)+len(queues['L'])+len(queues['S']),
        'block_L_s':count['block_L_s'],'block_S_s':count['block_S_s'],
        'blocked_during_S_green_s':count['blocked_during_S_green_s'],
        'max_external':count['max_external'],'max_L':count['max_L'],
        'max_S':count['max_S'],'cycles':curves}

def paired_grid():
    rows=[]
    for ratio in (.15,.30,.45):
        for seed in range(8):
            c=Setup(left_share=ratio,seed=seed)
            stream=generated_stream(c)
            for leading in (True,False):
                for length in (14.,28.,42.,70.):
                    y=run(replace(c,left_length_m=length,leading=leading),stream)
                    rows.append({'left_share':ratio,'seed':seed,'leading':leading,
                        'length_m':length,'through_exits':y['exits_S'],
                        'left_exits':y['exits_L'],'block_L_s':y['block_L_s'],
                        'external_max':y['max_external'],'total_exits':y['total_exits']})
    return rows

if __name__=='__main__':
    print(json.dumps(run(Setup(duration=240)),ensure_ascii=False)[:500])
