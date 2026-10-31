"""T2 v0.9: paired counterfactuals with time-stamped arrivals and world-contact switches.

This is a finite-queue mesoscopic *hypothesis model*, NOT a validated
car-following model. The explicit delayed upstream admission boundary
separates generated demand from entry into the modeled link.
"""
from __future__ import annotations
from dataclasses import dataclass, replace, asdict
from collections import deque, Counter
from math import floor
import random

@dataclass(frozen=True)
class Params:
    horizon_s:int=1800
    cycle_s:int=120
    left_green_s:int=35
    straight_green_s:int=50
    clearance_s:int=3
    phase_order:str="leading"
    bay_length_m:float=28
    straight_storage_m:float=56
    upstream_storage_m:float=84
    pitch_m:float=7
    left_headway_s:int=2
    straight_headway_s:int=2
    arrival_rate_vph:int=1500
    turn_share:float=.30
    seed:int=0
    arrival_pattern:str="uniform" # uniform | platoon
    platoon_cycle_s:int=60
    platoon_active_s:int=20
    feeder_policy:str="fifo" # fifo | bypass
    max_entry_per_s:int=1

def check(c:Params):
    if min(c.horizon_s,c.cycle_s,c.left_green_s,c.straight_green_s,
           c.left_headway_s,c.straight_headway_s,c.max_entry_per_s)<1: raise ValueError("time/flow >0 required")
    if c.clearance_s<0 or c.left_green_s+c.straight_green_s+2*c.clearance_s>c.cycle_s:
        raise ValueError("protected greens overlap")
    if c.phase_order not in ("leading","lagging") or c.feeder_policy not in ("fifo","bypass"):
        raise ValueError("unknown phase or feeder policy")
    if c.arrival_pattern not in ("uniform","platoon") or c.platoon_cycle_s<1 or not 1<=c.platoon_active_s<=c.platoon_cycle_s:
        raise ValueError("invalid arrival pattern")
    if c.arrival_rate_vph<0 or not 0<=c.turn_share<=1 or min(c.bay_length_m,c.straight_storage_m,c.upstream_storage_m)<0 or c.pitch_m<=0:
        raise ValueError("invalid demand or geometry")
    return tuple(floor(x/c.pitch_m+1e-9) for x in
                 (c.bay_length_m,c.straight_storage_m,c.upstream_storage_m))

def green(c:Params,t:int):
    x=t%c.cycle_s
    a="L" if c.phase_order=="leading" else "S"
    b="S" if a=="L" else "L"
    first=c.left_green_s if a=="L" else c.straight_green_s
    second=c.straight_green_s if b=="S" else c.left_green_s
    if x<first:return a
    if x<first+c.clearance_s:return "-"
    if x<first+c.clearance_s+second:return b
    return "-"

def demand(c:Params):
    """Timestamped demand tuple (second, route), independent of interventions."""
    check(c)
    rng=random.Random(c.seed)
    rate=c.arrival_rate_vph
    events=[]
    if c.arrival_pattern=="uniform":
        for t in range(c.horizon_s):
            count=((t+1)*rate)//3600-(t*rate)//3600
            events.extend((t,"L" if rng.random()<c.turn_share else "S") for _ in range(count))
    else:
        active=c.platoon_active_s
        period=c.platoon_cycle_s
        # Deterministic weighted-floor cumulative method; exactly conserved
        # over full periods; total generated vehicles may differ at horizon boundary.
        cumulative=0
        for t in range(c.horizon_s):
            pulse=t%period
            if pulse>=active:continue
            active_index=(t//period)*active+pulse
            new=(active_index+1)*rate*period//(3600*active)
            count=new-cumulative
            cumulative=new
            events.extend((t,"L" if rng.random()<c.turn_share else "S") for _ in range(count))
    return tuple(events)

def run(c:Params,events=None):
    left_cap,straight_cap,upstream_cap=check(c)
    if events is None:events=demand(c)
    if any(not isinstance(t,int) or t<0 or t>=c.horizon_s or route not in ("L","S") for t,route in events):
        raise ValueError("invalid arrivals")
    if any(events[i][0]>events[i+1][0] for i in range(len(events)-1)):
        raise ValueError("arrival events not sorted")
    outside=deque()
    upstream=deque()
    bay=deque()
    straight=deque()
    dest={"L":bay,"S":straight}
    cap={"L":left_cap,"S":straight_cap}
    last={"L":-1000000,"S":-1000000}
    counter=Counter()
    by_cycle=[]
    next_id=0
    entry_events=[]
    throughput=[]
    for t in range(c.horizon_s):
        while next_id<len(events) and events[next_id][0]==t:
            outside.append((next_id,events[next_id][1],t));next_id+=1
        phase=green(c,t)
        if phase in dest and dest[phase] and t-last[phase]>=(
            c.left_headway_s if phase=="L" else c.straight_headway_s):
            v=dest[phase].popleft()
            last[phase]=t
            counter["exit_"+phase]+=1
            throughput.append((t,v[0],phase))
        # Inside-link entry: route-aware transfer, optional pass around at fork.
        for _ in range(c.max_entry_per_s):
            if not upstream:break
            selected=0
            if c.feeder_policy=="bypass":
                for j,v in enumerate(upstream):
                    if len(dest[v[1]])<cap[v[1]]:
                        selected=j;break
            vehicle=upstream[selected]
            route=vehicle[1]
            if len(dest[route])>=cap[route]:
                counter["blocked_"+route+"_seconds"]+=1
                if route=="L" and phase=="S":counter["left_spillback_during_straight_green_s"]+=1
                break
            # deque indexing/removal by ID, deterministic and distinct
            del upstream[selected]
            dest[route].append(vehicle)
            counter["entered_"+route]+=1
            entry_events.append((t,vehicle[0],route))
        # Demand admission: explicit finite upstream length; overflow stays outside.
        while outside and len(upstream)<upstream_cap:
            upstream.append(outside.popleft())
            counter["admitted"]+=1
        if outside:counter["insertion_delay_affected_seconds"]+=1
        counter["max_outside"]=max(counter["max_outside"],len(outside))
        counter["max_upstream"]=max(counter["max_upstream"],len(upstream))
        counter["max_bay"]=max(counter["max_bay"],len(bay))
        counter["max_straight"]=max(counter["max_straight"],len(straight))
        count=counter["exit_L"]+counter["exit_S"]
        if next_id!=count+len(outside)+len(upstream)+len(bay)+len(straight):
            raise AssertionError(("conservation",t))
        if len(upstream)>upstream_cap or len(bay)>left_cap or len(straight)>straight_cap:
            raise AssertionError(("storage",t))
        if (t+1)%c.cycle_s==0 or t==c.horizon_s-1:
            by_cycle.append({"end_s":t+1,"exit_L":counter["exit_L"],"exit_S":counter["exit_S"],
                 "outside":len(outside),"upstream":len(upstream),"bay":len(bay),
                 "straight":len(straight),"spillback_s":counter["blocked_L_seconds"]})
    return {"config":asdict(c),"world_status":"SYNTHETIC_UNCALIBRATED",
        "storage_slots":{"bay":left_cap,"straight":straight_cap,"upstream":upstream_cap},
        "generated":len(events),"admitted":counter["admitted"],
        "exits_L":counter["exit_L"],"exits_S":counter["exit_S"],
        "remaining":len(outside)+len(upstream)+len(bay)+len(straight),
        "still_outside":len(outside),
        "blocked_L_seconds":counter["blocked_L_seconds"],
        "blocked_S_seconds":counter["blocked_S_seconds"],
        "left_spillback_during_straight_green_s":counter["left_spillback_during_straight_green_s"],
        "insertion_delay_affected_seconds":counter["insertion_delay_affected_seconds"],
        "max_inside":counter["max_upstream"]+counter["max_bay"]+counter["max_straight"],
        "cycle_history":by_cycle,"stopline_events":throughput,"fork_events":entry_events}
