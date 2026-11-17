"""D51: fixed-demand leading vs lagging protected-left phase order.

Synthetic single-approach point-queue model, not a physical road model.
Both alternatives have identical cycle, split, total loss time, demand,
source FIFO, receiving capacity, and per-second service. Only phase order
changes. Pre-tick occupancy rule as D50. A randomized arrival/turning
order can be supplied as a fixed external Vehicle sequence.
"""
from __future__ import annotations
from dataclasses import dataclass
from collections import deque
from statistics import mean
from typing import Iterable
from d50_turn_pocket import Vehicle, periodic_arrivals

@dataclass(frozen=True)
class Params:
    cycle_s: int = 60
    through_green_s: int = 24
    left_green_s: int = 12
    horizon_s: int = 600
    through_capacity: int = 12
    left_capacity: int = 4
    left_first: bool = False
    def __post_init__(self):
        for name in ('cycle_s','through_green_s','left_green_s','horizon_s','through_capacity','left_capacity'):
            if type(getattr(self,name)) is not int: raise ValueError(f'{name} must be int')
        if type(self.left_first) is not bool: raise ValueError('left_first must be bool')
        if (self.cycle_s <= 0 or self.through_green_s <= 0 or self.left_green_s <= 0
            or self.through_green_s+self.left_green_s > self.cycle_s
            or self.horizon_s < 1 or self.through_capacity < 1 or self.left_capacity < 1):
            raise ValueError('invalid timing/capacity')

@dataclass(frozen=True)
class Outcome:
    left_first: bool
    arrivals_through: int
    arrivals_left: int
    completed_through: int
    completed_left: int
    unserved_through: int
    unserved_left: int
    mean_through_delay_s: float | None
    mean_left_delay_s: float | None
    mean_vehicle_delay_s: float | None
    maximum_through_delay_s: int | None
    left_head_blocked_seconds: int
    through_behind_left_seconds: int
    maximum_left_occupancy: int
    maximum_through_occupancy: int
    last_cycle_left_queue: int
    last_cycle_through_queue: int
    @property
    def unserved(self): return self.unserved_through+self.unserved_left

def phase(t:int,p:Params)->str:
    s=t%p.cycle_s
    if p.left_first:
        if s < p.left_green_s: return 'L'
        if s < p.left_green_s+p.through_green_s: return 'T'
    else:
        if s < p.through_green_s: return 'T'
        if s < p.through_green_s+p.left_green_s: return 'L'
    return 'R'

def simulate(vehicles:Iterable[Vehicle],p:Params)->Outcome:
    xs=tuple(vehicles)
    if (any(type(x.arrival_s) is not int or x.arrival_s<0 or x.arrival_s>=p.horizon_s
            or type(x.ident) is not int or x.movement not in ('T','L') for x in xs)
        or tuple(x.arrival_s for x in xs)!=tuple(sorted(x.arrival_s for x in xs))
        or len(set(x.ident for x in xs))!=len(xs)):
        raise ValueError('invalid vehicles')
    source,through,left=deque(),deque(),deque()
    done_t,done_l=[],[]
    idx=max_t=max_l=blocked=trapped=0
    exp_t=sum(x.movement=='T' for x in xs)
    final_t=final_l=0
    for t in range(p.horizon_s):
        while idx<len(xs) and xs[idx].arrival_s==t:
            source.append(xs[idx]);idx+=1
        pre_t,pre_l=len(through),len(left)
        ph=phase(t,p)
        if ph=='T' and through: done_t.append(t-through.popleft().arrival_s)
        if ph=='L' and left: done_l.append(t-left.popleft().arrival_s)
        if source:
            v=source[0]
            if v.movement=='T' and pre_t<p.through_capacity:
                through.append(source.popleft())
            elif v.movement=='L' and pre_l<p.left_capacity:
                left.append(source.popleft())
            elif v.movement=='L':
                blocked+=1
                trapped+=int(any(w.movement=='T' for w in source))
        max_t=max(max_t,len(through));max_l=max(max_l,len(left))
        assert len(through)<=p.through_capacity and len(left)<=p.left_capacity
        assert idx==len(source)+len(through)+len(left)+len(done_t)+len(done_l)
        if t==p.horizon_s-1:
            final_t=sum(w.movement=='T' for w in source)+len(through)
            final_l=sum(w.movement=='L' for w in source)+len(left)
    total_count=len(done_t)+len(done_l)
    return Outcome(p.left_first,exp_t,len(xs)-exp_t,len(done_t),len(done_l),
                   final_t,final_l,mean(done_t) if done_t else None,
                   mean(done_l) if done_l else None,
                   (sum(done_t)+sum(done_l))/total_count if total_count else None,
                   max(done_t) if done_t else None,blocked,trapped,max_l,max_t,
                   final_l,final_t)

def key(r:Outcome):
    return (r.unserved,r.mean_vehicle_delay_s if r.mean_vehicle_delay_s is not None else float('inf'))

if __name__=='__main__':
    from dataclasses import replace
    x=periodic_arrivals()
    for k in (1,2,3,4,6,8,12):
        pair=[simulate(x,Params(left_capacity=k,left_first=v)) for v in (False,True)]
        print(k,[(r.left_first,r.unserved,round(r.mean_vehicle_delay_s or 0,3),r.through_behind_left_seconds) for r in pair])
