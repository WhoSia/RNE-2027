"""Synthetic platoon arrivals with nonstationary hourly demand and turning shares.

Each full period has a fixed vehicle budget. Rotating the within-period
arrival clock holds total vehicles and route-type multiset unchanged.
Results describe synthetic input uncertainty, NOT observed traffic.
"""
from dataclasses import dataclass
import random

@dataclass(frozen=True)
class ArrivalProfile:
    duration_s:int=720
    period_s:int=60
    active_s:int=20
    arrival_offset_s:int=0
    rates_vph:tuple[int,...]=(1500,)
    left_shares:tuple[float,...]=(.30,)
    seed:int=0

def make_arrivals(p:ArrivalProfile):
    if (not isinstance(p.duration_s,int) or not isinstance(p.period_s,int)
        or not isinstance(p.active_s,int) or p.duration_s<1 or p.period_s<1
        or not 1<=p.active_s<=p.period_s or p.duration_s%p.period_s):
        raise ValueError('positive complete arrival periods required')
    if not isinstance(p.arrival_offset_s,int) or not p.rates_vph or not p.left_shares:
        raise ValueError('missing or noninteger arrival control')
    if any(not isinstance(r,int) or r<0 for r in p.rates_vph):
        raise ValueError('nonnegative integer veh/h required')
    if any(not isinstance(x,(float,int)) or not 0<=x<=1 for x in p.left_shares):
        raise ValueError('invalid left fractions')
    rng=random.Random(p.seed)
    events=[]
    demand_units=0
    cumulative=0
    for period in range(p.duration_s//p.period_s):
        rate=p.rates_vph[period%len(p.rates_vph)]
        turn=p.left_shares[period%len(p.left_shares)]
        demand_units+=rate*p.period_s
        total=demand_units//3600
        n=total-cumulative
        cumulative=total
        vehicles=['L' if rng.random()<turn else 'S' for _ in range(n)]
        staged=[]
        for j in range(p.active_s):
            lo=j*n//p.active_s
            hi=(j+1)*n//p.active_s
            t=period*p.period_s+(j+p.arrival_offset_s)%p.period_s
            staged.extend((t,route) for route in vehicles[lo:hi])
        events.extend(sorted(staged,key=lambda x:x[0]))
    assert len(events)==demand_units//3600
    return tuple(events)
