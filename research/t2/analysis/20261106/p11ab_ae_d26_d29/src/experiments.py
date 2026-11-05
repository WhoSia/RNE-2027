"""Controlled experimental scenarios, no claim of field calibration."""
from dataclasses import dataclass
import random
from .micro_network import Link, Signal, Crossing, BusStop, Demand, Network

@dataclass(frozen=True)
class OD:
    origin: str
    destination: str
    rate_per_hour: float


def generate_od_demand(od:OD, route:tuple[str,...], seconds:int, seed:int=20261106, *, length_m=4.5):
    """Poisson emissions from a fixed route; independent of signal-policy choice."""
    if od.rate_per_hour<0 or seconds<0:raise ValueError('invalid source rate')
    rng=random.Random(seed)
    at=0.; result=[]
    while od.rate_per_hour>0:
        at += rng.expovariate(od.rate_per_hour/3600.)
        if at>=seconds:break
        result.append(Demand(f'{od.origin}_{od.destination}_{len(result)}',at,route,length_m))
    return result


def network_fixture(grade=0.0, curve_radius=None, downstream_block=0.0, with_pedestrians=True):
    links=[Link('A',35,10,grade,curve_radius,'J','straight'),
           Link('B',18,8,0,None,'J2','straight'),
           Link('C',42,10,0,None,'J3','straight'),
           Link('TURN',15,6,0,12,'J','left'),
           Link('SIDE',28,8,0,None,'J2','right')]
    net=Network(links,
        signals={'A':Signal(20,((0,12),)),'TURN':Signal(20,((12,18),))},
        crossings=[Crossing('J',((8,11),(28,31))) ] if with_pedestrians else [],
        stops=[BusStop('A',20,0,4)],dt_s=0.5)
    demands=[Demand('car1',0,('A','B','C')),
             Demand('car2',1,('A','B','C')),
             Demand('bus1',2,('A','B','C'),length_m=11,desired_speed_mps=7,kind='bus'),
             Demand('turn1',2,('TURN','B','C')),
             Demand('side1',3,('SIDE','C'))]
    blockers={'B':downstream_block} if downstream_block else {}
    return net,demands,blockers


def run_pair():
    net,demands,blockers=network_fixture(downstream_block=20)
    closed=net.run(demands,120,blockers)
    opened=net.run(demands,120)
    return {label:{'completed':len(out.completed_s),'admitted':len(out.admitted_s),
                   'first_completed_s':min(out.completed_s.values()) if out.completed_s else None,
                   'blocked':out.blocked,
                   'max_external_queue':max(n for t,n in out.queues)}
            for label,out in [('closed',closed),('open',opened)]}
