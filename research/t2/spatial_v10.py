"""T2 v1.0 physically placed one-lane-plus-turn-pocket cellular comparator.

Each 7m cell stores at most one vehicle; left turning vehicles use the
shared approach until the physical pocket fork. Deterministic front-to-back
motion, no teleport, protected nonoverlapping signal, finite road.
Not calibrated to real traffic and not a full lane-changing model.
"""
from dataclasses import dataclass,asdict
from collections import deque,Counter
from math import floor
import random

@dataclass(frozen=True)
class Config:
    duration_s:int=1800
    cycle_s:int=120
    left_green_s:int=35
    through_green_s:int=50
    clearance_s:int=3
    phase_order:str="leading"
    approach_length_m:float=140.
    pocket_length_m:float=28.
    cell_m:float=7.
    demand_vph:int=1500
    left_fraction:float=.30
    seed:int=0
    arrival_pattern:str="uniform"
    platoon_period_s:int=60
    platoon_on_s:int=20
    departure_headway_s:int=2
    entry_headway_s:int=1

def validate(c):
    ints=(c.duration_s,c.cycle_s,c.left_green_s,c.through_green_s,
          c.platoon_period_s,c.platoon_on_s,c.departure_headway_s,c.entry_headway_s)
    if any(not isinstance(x,int) or x<1 for x in ints):
        raise ValueError("positive integer timings required")
    if c.clearance_s<0 or c.left_green_s+c.through_green_s+2*c.clearance_s>c.cycle_s:
        raise ValueError("overlapping phase")
    if c.phase_order not in ("leading","lagging") or c.arrival_pattern not in ("uniform","platoon"):
        raise ValueError("unknown signal or arrival policy")
    if c.platoon_on_s>c.platoon_period_s or c.demand_vph<0 or not 0<=c.left_fraction<=1:
        raise ValueError("invalid demand")
    if c.cell_m<=0 or c.approach_length_m<=0 or c.pocket_length_m<0:
        raise ValueError("invalid road")
    n=floor(c.approach_length_m/c.cell_m+1e-9)
    k=floor(c.pocket_length_m/c.cell_m+1e-9)
    if not 0<=k<n:raise ValueError("pocket must be shorter than approach")
    return n,k

def phase(c,t):
    x=t%c.cycle_s
    first="L" if c.phase_order=="leading" else "S"
    second="S" if first=="L" else "L"
    width=c.left_green_s if first=="L" else c.through_green_s
    if x<width:return first
    if x<width+c.clearance_s:return "-"
    x-=width+c.clearance_s
    second_width=c.through_green_s if second=="S" else c.left_green_s
    return second if x<second_width else "-"

def arrivals(c):
    validate(c)
    rng=random.Random(c.seed)
    event=[]
    if c.arrival_pattern=="uniform":
        for t in range(c.duration_s):
            k=(t+1)*c.demand_vph//3600-t*c.demand_vph//3600
            event.extend((t,"L" if rng.random()<c.left_fraction else "S") for _ in range(k))
    else:
        prev=0
        for t in range(c.duration_s):
            if t%c.platoon_period_s>=c.platoon_on_s:continue
            active=(t//c.platoon_period_s)*c.platoon_on_s+t%c.platoon_period_s+1
            curr=active*c.demand_vph*c.platoon_period_s//(3600*c.platoon_on_s)
            event.extend((t,"L" if rng.random()<c.left_fraction else "S") for _ in range(curr-prev))
            prev=curr
    return tuple(event)

def simulate(c=Config(),events=None,*,trace=False):
    n,k=validate(c)
    if events is None:events=arrivals(c)
    if any(not isinstance(t,int) or not 0<=t<c.duration_s or route not in ("L","S") for t,route in events):
        raise ValueError("bad arrival event")
    if any(events[i][0]>events[i+1][0] for i in range(len(events)-1)):
        raise ValueError("unsorted arrivals")
    main={};bay={};outside=deque()
    count=Counter();cycles=[];log=[];ix=0
    last_exit={"L":-10**9,"S":-10**9};last_entry=-10**9
    frames=[]
    for t in range(c.duration_s):
        while ix<len(events) and events[ix][0]==t:
            outside.append((ix,events[ix][1],t));ix+=1
        lit=phase(c,t)
        for lane,occ in (("S",main),("L",bay)):
            if lit==lane and -1 in occ and occ[-1][1]==lane and t-last_exit[lane]>=c.departure_headway_s:
                v=occ.pop(-1);count["exit_"+lane]+=1;last_exit[lane]=t
                count["system_time_"+lane+"_s"]+=t-v[2]
                if trace:log.append((t,"exit",v[0],lane,-1))
        for x in sorted(tuple(bay),reverse=True):
            if x< -1 and x+1 not in bay:bay[x+1]=bay.pop(x)
        for x in sorted(tuple(main),reverse=True):
            if x not in main:continue
            v=main[x]
            if v[1]=="L" and k>0 and x==-k-1:
                if -k not in bay:
                    bay[-k]=main.pop(x);count["merges"]+=1
                    if trace:log.append((t,"merge",v[0],"L",-k))
                else:count["blocked_pocket_entry_s"]+=1
            elif v[1]=="L" and k==0 and x==-1:
                count["blocked_pocket_entry_s"]+=1
            elif x< -1 and x+1 not in main and not(v[1]=="L" and x>=-k-1):
                main[x+1]=main.pop(x)
        if outside and -n not in main and t-last_entry>=c.entry_headway_s:
            v=outside.popleft();main[-n]=v;count["admitted"]+=1;last_entry=t
            if trace:log.append((t,"admit",v[0],v[1],-n))
        if outside:count["insertion_delay_s"]+=1
        if lit=="S" and -1 not in main:count["through_green_no_stopline_vehicle_s"]+=1
        if lit=="S" and k>0 and -k-1 in main and main[-k-1][1]=="L" and -k in bay:
            count["pocket_block_during_S_green_s"]+=1
        if len(main)>n or len(bay)>k or any(x< -n or x>-1 for x in main) or any(x< -k or x>-1 for x in bay):
            raise AssertionError(("geometry",t))
        if len(set(v[0] for v in main.values())|set(v[0] for v in bay.values()))!=len(main)+len(bay):
            raise AssertionError(("duplicate",t))
        if ix!=count["exit_L"]+count["exit_S"]+len(outside)+len(main)+len(bay):
            raise AssertionError(("conservation",t))
        for metric,value in (("max_through_queue",len(main)),("max_bay_queue",len(bay)),("max_outside",len(outside))):
            count[metric]=max(count[metric],value)
        if trace:
            frames.append({"t":t,"signal":lit,
                "main":sorted((x,v[0],v[1]) for x,v in main.items()),
                "pocket":sorted((x,v[0],v[1]) for x,v in bay.items()),
                "outside":len(outside)})
        if (t+1)%c.cycle_s==0 or t==c.duration_s-1:
            cycles.append({"end_s":t+1,"exit_S":count["exit_S"],"exit_L":count["exit_L"],
                "through_vehicles":len(main),"pocket_vehicles":len(bay),
                "outside":len(outside),"blocked_pocket_s":count["blocked_pocket_entry_s"],
                "pocket_block_during_S_green_s":count["pocket_block_during_S_green_s"]})
    result={"model":"spatial_v10","status":"SYNTHETIC_UNCALIBRATED",
        "config":asdict(c),"approach_cells":n,"pocket_cells":k,
        "generated":len(events),"admitted":count["admitted"],
        "mean_system_time_S_s":count["system_time_S_s"]/count["exit_S"] if count["exit_S"] else None,
        "mean_system_time_L_s":count["system_time_L_s"]/count["exit_L"] if count["exit_L"] else None,
        "exit_S":count["exit_S"],"exit_L":count["exit_L"],
        "remaining":len(outside)+len(main)+len(bay),"outside":len(outside),
        "blocked_pocket_entry_s":count["blocked_pocket_entry_s"],
        "pocket_block_during_S_green_s":count["pocket_block_during_S_green_s"],
        "through_green_no_stopline_vehicle_s":count["through_green_no_stopline_vehicle_s"],
        "max_through_queue":count["max_through_queue"],"max_bay_queue":count["max_bay_queue"],
        "max_outside":count["max_outside"],"cycles":cycles}
    if trace:
        result["events"]=log
        result["frames"]=frames
    return result
