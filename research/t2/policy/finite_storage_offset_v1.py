"""D48 synthetic two-way finite-storage corridor, NOT field-calibrated.

Integer-second event model, no turns or conflicts. Each directional link holds
at most K vehicles, including those travelling toward the downstream stopline.
Upstream admission uses link occupancy from START of tick, never same-tick
downstream space release. Upstream source queues are unbounded.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass, replace
from statistics import mean
from typing import Iterable

@dataclass(frozen=True)
class Config:
    cycle_s:int=60
    green_s:int=20
    travel_s:int=16
    horizon_s:int=600
    offset_B_s:int=0
    east_link_capacity:int=12
    west_link_capacity:int=12
    def __post_init__(self):
        vals=(self.cycle_s,self.green_s,self.travel_s,self.horizon_s,
              self.offset_B_s,self.east_link_capacity,self.west_link_capacity)
        if any(type(x) is not int for x in vals): raise ValueError("integers required")
        if not 0<self.green_s<=self.cycle_s: raise ValueError("green/cycle invalid")
        if not 0<=self.offset_B_s<self.cycle_s: raise ValueError("offset invalid")
        if not 0<self.travel_s<self.horizon_s: raise ValueError("travel/horizon invalid")
        if min(self.east_link_capacity,self.west_link_capacity)<1: raise ValueError("capacity invalid")

@dataclass(frozen=True)
class Direction:
    arrivals:int
    completed:int
    unserved:int
    mean_trip_s:float|None
    mean_delay_s:float|None
    max_source_queue:int
    max_link_occupancy:int
    blocked_green_seconds:int
    waiting_source_end:int
    on_link_end:int

@dataclass(frozen=True)
class Result:
    offset_B_s:int
    east:Direction
    west:Direction
    total_arrivals:int
    total_completed:int
    total_unserved:int
    mean_trip_s:float|None
    mean_delay_s:float|None
    max_direction_mean_delay_s:float|None
    blocked_green_seconds:int

def green(t:int,offset:int,cfg:Config)->bool:
    return (t-offset)%cfg.cycle_s<cfg.green_s

def _check(seq:tuple[int,...],cfg:Config):
    if tuple(sorted(seq))!=seq or any(type(t) is not int or not 0<=t<cfg.horizon_s for t in seq):
        raise ValueError("unsorted or invalid arrivals")

def _direction(seq:tuple[int,...],cfg:Config,start_offset:int,end_offset:int,capacity:int)->Direction:
    source=deque()
    link=deque()
    trips=[]
    i=max_s=max_l=blocked=0
    for t in range(cfg.horizon_s):
        while i<len(seq) and seq[i]==t:
            source.append((i,t));i+=1
        max_s=max(max_s,len(source))
        max_l=max(max_l,len(link))
        pre_tick_count=len(link)
        if link and link[0][2]<=t and green(t,end_offset,cfg):
            _,source_t,_=link.popleft()
            trips.append(t-source_t)
        if source and green(t,start_offset,cfg):
            if pre_tick_count<capacity:
                ident,source_t=source.popleft()
                link.append((ident,source_t,t+cfg.travel_s))
                max_l=max(max_l,len(link))
            else:
                blocked+=1
        assert len(link)<=capacity
        assert len(source)+len(link)+len(trips)==i, "conservation violated"
    avg=mean(trips) if trips else None
    assert len(seq)-len(trips)==len(source)+len(link)
    return Direction(len(seq),len(trips),len(seq)-len(trips),avg,
                     avg-cfg.travel_s if avg is not None else None,
                     max_s,max_l,blocked,len(source),len(link))

def simulate(east_arrivals:Iterable[int],west_arrivals:Iterable[int],cfg:Config)->Result:
    e_arr,w_arr=tuple(east_arrivals),tuple(west_arrivals)
    _check(e_arr,cfg);_check(w_arr,cfg)
    e=_direction(e_arr,cfg,0,cfg.offset_B_s,cfg.east_link_capacity)
    w=_direction(w_arr,cfg,cfg.offset_B_s,0,cfg.west_link_capacity)
    n=e.completed+w.completed
    total_trip=sum((x.mean_trip_s or 0)*x.completed for x in (e,w))
    avg=total_trip/n if n else None
    valid=[x.mean_delay_s for x in (e,w) if x.mean_delay_s is not None]
    return Result(cfg.offset_B_s,e,w,len(e_arr)+len(w_arr),n,e.unserved+w.unserved,
                  avg,avg-cfg.travel_s if avg is not None else None,
                  max(valid) if valid else None,
                  e.blocked_green_seconds+w.blocked_green_seconds)

def platoons(cycles:int,width:int,cycle_s:int=60,phase_s:int=0)->tuple[int,...]:
    if any(type(v) is not int for v in (cycles,width,cycle_s,phase_s)):
        raise ValueError("integers required")
    if cycles<1 or not 0<=width<=cycle_s or phase_s<0 or phase_s+width>cycle_s:
        raise ValueError("platoon parameters invalid")
    return tuple(c*cycle_s+phase_s+k for c in range(cycles) for k in range(width))

def sweep(east:Iterable[int],west:Iterable[int],cfg:Config)->list[Result]:
    e,w=tuple(east),tuple(west)
    return [simulate(e,w,replace(cfg,offset_B_s=i)) for i in range(cfg.cycle_s)]

def efficiency_key(r:Result)->tuple[int,float,int]:
    return (r.total_unserved,r.mean_delay_s if r.mean_delay_s is not None else float("inf"),r.offset_B_s)

def fairness_key(r:Result)->tuple[int,float,float,int]:
    return (r.total_unserved,
            r.max_direction_mean_delay_s if r.max_direction_mean_delay_s is not None else float("inf"),
            r.mean_delay_s if r.mean_delay_s is not None else float("inf"),r.offset_B_s)

if __name__=="__main__":
    for cap in (4,6,8,10,12,20,1000):
        results=sweep(platoons(6,12),platoons(6,12),
                      Config(east_link_capacity=cap,west_link_capacity=cap))
        best=min(results,key=efficiency_key)
        print(cap,best.offset_B_s,best.mean_delay_s,best.total_unserved,best.blocked_green_seconds)
