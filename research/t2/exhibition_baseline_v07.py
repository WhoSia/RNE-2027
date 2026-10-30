"""T2 v0.7 exhibition baseline: queue conservation and finite physical pocket.

This is a *lumped queue* comparator, NOT a spatial car-following simulator.
One FIFO upstream feeder dispatches at most one vehicle per time step into
a finite left pocket or a through queue. Pocket length maps to queue slots
using specified standing vehicle pitch. Lane-changing and approach travel
times are abstracted away. This makes model discrepancies interpretable.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, replace
from collections import Counter, deque
import random
import json

@dataclass(frozen=True)
class Scenario:
    duration_s: int = 3600
    cycle_s: int = 120
    through_green_s: int = 50
    left_green_s: int = 35
    clearance_s: int = 3
    phase: str = 'leading'
    pocket_m: float = 35.0
    standing_pitch_m: float = 7.0
    demand_vph: int = 1500
    left_fraction: float = 0.3
    seed: int = 11
    through_headway_s: int = 2
    left_headway_s: int = 2

def capacity(c: Scenario) -> int:
    if c.duration_s < 1 or c.cycle_s < 1 or c.through_green_s < 1 or c.left_green_s < 1:
        raise ValueError('positive timing parameters required')
    if c.phase not in ('leading','lagging'):
        raise ValueError('protected left signal order must be leading or lagging')
    if c.clearance_s < 0 or c.left_green_s+c.through_green_s+2*c.clearance_s > c.cycle_s:
        raise ValueError('infeasible phase plan')
    if c.pocket_m < 0 or c.standing_pitch_m <= 0:
        raise ValueError('invalid pocket geometry')
    if c.through_headway_s < 1 or c.left_headway_s < 1 or c.demand_vph < 0:
        raise ValueError('invalid flow parameters')
    if not 0 <= c.left_fraction <= 1:
        raise ValueError('invalid turning ratio')
    return int((c.pocket_m+1e-9)//c.standing_pitch_m)

def greens(c: Scenario,t: int) -> tuple[bool,bool]:
    p=t%c.cycle_s
    first_l=c.phase=='leading'
    first_green=c.left_green_s if first_l else c.through_green_s
    second_green=c.through_green_s if first_l else c.left_green_s
    if p<first_green:
        return (not first_l,first_l)
    p-=first_green
    if p<c.clearance_s: return False,False
    p-=c.clearance_s
    if p<second_green:
        return (first_l,not first_l)
    return False,False

def arrivals(c: Scenario) -> tuple[str,...]:
    """Deterministically spaced demand with seeded turning choices."""
    rng=random.Random(c.seed)
    n=(c.duration_s*c.demand_vph)//3600
    return tuple('L' if rng.random()<c.left_fraction else 'S' for _ in range(n))

def simulate(c: Scenario, stream: tuple[str,...]|None=None) -> dict:
    cap=capacity(c)
    # Each ID remains in precisely one container until discharge.
    if stream is None: stream=arrivals(c)
    if any(route not in ('L','S') for route in stream):
        raise ValueError('stream accepts only L or S')
    # Input stream has deterministic timestamps based on configured demand
    # and can be reused with the same demand/length across interventions.
    horizon=(c.duration_s*c.demand_vph)//3600
    if len(stream)!=horizon:
        raise ValueError('stream must match deterministic generated vehicle count')
    q=deque()
    left=deque()
    through=deque()
    metrics=Counter()
    cycles=[]
    idx=0
    lastL=-9999
    lastS=-9999
    green_open_S=0
    green_open_L=0
    max_shared=0
    max_left=0
    max_through=0
    for t in range(c.duration_s):
        # arrivals are generated at integer deterministic grid times
        target=((t+1)*c.demand_vph)//3600
        while idx<target:
            q.append((idx,stream[idx],t))
            idx+=1
        sg,lg=greens(c,t)
        if sg: green_open_S+=1
        if lg: green_open_L+=1
        # A green second has no discharging supply if its queue was empty
        # BEFORE discharge and transfer; otherwise post-discharge emptiness
        # would mislabel an actually productive second as wasted.
        if sg and not through:
            metrics['through_green_empty_seconds']+=1
        if lg and not left:
            metrics['left_green_empty_seconds']+=1
        # Discharge branch queues. The signal is only a downstream exit gate.
        if lg and left and t-lastL>=c.left_headway_s:
            left.popleft()
            metrics['left_exits']+=1
            lastL=t
        if sg and through and t-lastS>=c.through_headway_s:
            through.popleft()
            metrics['through_exits']+=1
            lastS=t
        # FIFO shared feeder toward split; one transfer per step.
        if q:
            vid,route,arrived=q[0]
            if route=='L':
                if len(left)<cap:
                    q.popleft()
                    left.append((vid,arrived))
                    metrics['left_entries']+=1
                else:
                    metrics['spillback_block_seconds']+=1
                    if sg:
                        metrics['spillback_during_through_green_s']+=1
            else:
                q.popleft()
                through.append((vid,arrived))
                metrics['through_entries']+=1
        max_shared=max(max_shared,len(q))
        max_left=max(max_left,len(left))
        max_through=max(max_through,len(through))
        if len(left)>cap:
            raise AssertionError('pocket length capacity exceeded')
        if idx != metrics['left_exits']+metrics['through_exits']+len(q)+len(left)+len(through):
            raise AssertionError('vehicle conservation failed')
        if (t+1)%c.cycle_s==0 or t==c.duration_s-1:
            cycles.append({'end_s':t+1,
                           'shared_backlog':len(q),
                           'pocket_backlog':len(left),
                           'through_backlog':len(through),
                           'left_exits_cumulative':metrics['left_exits'],
                           'through_exits_cumulative':metrics['through_exits'],
                           'spillback_s_cumulative':metrics['spillback_block_seconds']})
    completed=metrics['left_exits']+metrics['through_exits']
    remaining=len(q)+len(left)+len(through)
    if completed+remaining!=len(stream):
        raise AssertionError('final vehicle conservation failed')
    return {'config':asdict(c),
            'pocket_capacity_veh':cap,
            'arrivals':len(stream),
            'left_exits':metrics['left_exits'],
            'through_exits':metrics['through_exits'],
            'total_exits':completed,
            'remaining':remaining,
            'spillback_block_seconds':metrics['spillback_block_seconds'],
            'spillback_during_through_green_s':metrics['spillback_during_through_green_s'],
            'through_green_empty_seconds':metrics['through_green_empty_seconds'],
            'left_green_empty_seconds':metrics['left_green_empty_seconds'],
            'max_shared_queue':max_shared,
            'max_pocket_queue':max_left,
            'max_through_queue':max_through,
            'cycles':cycles}

if __name__=='__main__':
    for L in (14,28,42,70):
        c=Scenario(pocket_m=L)
        r=simulate(c)
        print(json.dumps({'length_m':L,'slots':r['pocket_capacity_veh'],
              'through_exits':r['through_exits'],'left_exits':r['left_exits'],
              'spillback_s':r['spillback_block_seconds'],
              'remaining':r['remaining']},ensure_ascii=False))
