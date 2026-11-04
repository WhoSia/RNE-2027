"""Small deterministic signal-policy optimizer using independent event-time engine.

This is an exhaustive **oracle within specified finite choices**, not a new scalable
optimizer or evidence of real-world superiority. Units: s and veh-s.
"""
from dataclasses import replace
from dataclasses import dataclass
from network import SignalPlan, Phase, Network
from events import EventEngine, Demand

@dataclass(frozen=True)
class Evaluation:
    split_main_s:float
    offset_s:float
    completed:int
    total:int
    wait_veh_s:float
    unfinished:int

def score(net:Network, demands:tuple[Demand,...], horizon:float)->tuple[int,int,float,int]:
    data=EventEngine(net,demands,horizon).run()
    admissions={e['vehicle']:e['t_s'] for e in data['events'] if e['event']=='admit'}
    wait=sum((admissions.get(d.vehicle,horizon)-min(horizon,d.arrival_s)) for d in demands if d.arrival_s<=horizon)
    return data['completed'],data['total'],round(wait,6),data['unfinished']

def alternatives(net:Network, junction:str, cycle_s:float,
                 main_green_options:tuple[float,...],offset_options:tuple[float,...]):
    """Four-phase illustrative main/red/side/red signal, same safety intergreen.

    On each policy the green split is changed, not the demand or network state.
    """
    if cycle_s<=2:raise ValueError('cycle too short')
    for green in main_green_options:
        side=cycle_s-green-2
        if green<=0 or side<=0:continue
        for offset in offset_options:
            plan=SignalPlan(junction,(
                Phase(green,frozenset({'main'}),'main green'),
                Phase(1,frozenset(),'all red'),
                Phase(side,frozenset({'side'}),'side green'),
                Phase(1,frozenset(),'all red')),offset)
            yield green,offset,replace(net,plans=tuple(plan if p.junction==junction else p for p in net.plans))

def optimize(net:Network, junction:str,demands:tuple[Demand,...],horizon:float,
             cycle_s:float,green_options:tuple[float,...],offsets:tuple[float,...]):
    records=[]
    for g,off,candidate in alternatives(net,junction,cycle_s,green_options,offsets):
        done,total,wait,unfinished=score(candidate,demands,horizon)
        records.append(Evaluation(g,off,done,total,wait,unfinished))
    if not records:raise ValueError('no feasible plan')
    # No policy with unfinished vehicles can outscore a completed policy.
    return sorted(records,key=lambda r:(r.unfinished,r.wait_veh_s,r.split_main_s,r.offset_s))
