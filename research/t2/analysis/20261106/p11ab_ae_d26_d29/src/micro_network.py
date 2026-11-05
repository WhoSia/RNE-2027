"""Research-only deterministic microscopic reference. SI units; fixed-time signals.

This is an experimental no-lane-change model with finite, one-dimensional storage.
It does not certify safety, simulate realistic yielding, or optimize signal timing.
The state at the START of a tick controls all admission/transfer decisions.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import defaultdict
from math import isfinite, sqrt
import heapq

EPS = 1e-9
LAT_ACCEL_MPS2 = 2.0  # uncalibrated model ceiling, m/s^2

@dataclass(frozen=True)
class Link:
    name: str
    length_m: float
    speed_mps: float = 10.0
    grade: float = 0.0
    curve_radius_m: float | None = None
    junction: str | None = None  # resource at downstream end
    approach: str = 'straight'

@dataclass(frozen=True)
class Signal:
    cycle_s: float
    green_intervals: tuple[tuple[float, float], ...]
    offset_s: float = 0.0
    def green(self, t: float) -> bool:
        if self.cycle_s <= 0: raise ValueError('invalid signal cycle')
        phase = (t - self.offset_s) % self.cycle_s
        return any(a <= phase < b for a,b in self.green_intervals)

@dataclass(frozen=True)
class Crossing:
    junction: str
    intervals_s: tuple[tuple[float,float], ...]
    def occupied(self, t: float) -> bool:
        return any(a <= t < b for a,b in self.intervals_s)

@dataclass(frozen=True)
class BusStop:
    link: str
    position_m: float
    start_s: float
    dwell_s: float

@dataclass(frozen=True)
class Demand:
    identity: str
    arrival_s: float
    route: tuple[str, ...]
    length_m: float = 4.5
    desired_speed_mps: float = 11.0
    acceleration_mps2: float = 2.0
    deceleration_mps2: float = 3.0
    kind: str = 'car'

@dataclass
class Vehicle:
    spec: Demand
    segment: int = 0
    front_m: float = 0.0
    speed_mps: float = 0.0
    stop_done: bool = False
    dwell_end_s: float | None = None
    lane_override: str | None = None

@dataclass
class Output:
    admitted_s: dict[str,float] = field(default_factory=dict)
    completed_s: dict[str,float] = field(default_factory=dict)
    transfers: list[tuple[float,str,str,str]] = field(default_factory=list)
    occupancies: list[tuple[float,dict[str,int]]] = field(default_factory=list)
    queues: list[tuple[float,int]] = field(default_factory=list)
    blocked: dict[str,int] = field(default_factory=lambda:defaultdict(int))
    lane_changes: list[tuple[float,str,str,str]] = field(default_factory=list)
    traces: dict[str,list[tuple[float,str,float,float]]] = field(default_factory=lambda:defaultdict(list))

class Network:
    def __init__(self, links:list[Link], *, signals:dict[str,Signal]|None=None,
                 crossings:list[Crossing]|None=None, stops:list[BusStop]|None=None,
                 minimum_gap_m:float=2.0, dt_s:float=0.5,
                 lateral_neighbors:dict[str,tuple[str,...]]|None=None,
                 connections:dict[str,tuple[str,...]]|None=None):
        self.links={x.name:x for x in links}
        if not self.links or len(self.links)!=len(links): raise ValueError('unique links required')
        if dt_s<=0 or not isfinite(dt_s) or minimum_gap_m<0: raise ValueError('invalid spacing/time step')
        self.dt=dt_s
        self.gap=minimum_gap_m
        self.signals=signals or {}
        self.lateral_neighbors=lateral_neighbors or {}
        self.connections=connections
        for ln, neighbors in self.lateral_neighbors.items():
            if ln not in self.links or any(n not in self.links or abs(self.links[ln].length_m-self.links[n].length_m)>EPS for n in neighbors):
                raise ValueError("lane changes require adjacent equal-length reference links")
        self.crossings=crossings or []
        self.stops=stops or []
        for l in links:
            if l.length_m<=0 or l.speed_mps<=0 or not all(isfinite(x) for x in [l.length_m,l.speed_mps,l.grade]):raise ValueError('bad link')
            if l.curve_radius_m is not None and l.curve_radius_m<=0:raise ValueError('bad radius')
        for stop in self.stops:
            if stop.link not in self.links or not(0 <= stop.position_m <= self.links[stop.link].length_m) or stop.dwell_s<0:
                raise ValueError('invalid stop')

    def speed_cap(self,l:Link):
        # Experimental speed ceiling only: no calibrated tire/grade dynamic law.
        base = l.speed_mps * max(0.55, 1.0 - max(0,l.grade)*2)
        return min(base, sqrt(LAT_ACCEL_MPS2*l.curve_radius_m)) if l.curve_radius_m else base

    def run(self, specs:list[Demand], horizon_s:float, blocked_until:dict[str,float]|None=None,
            lane_change_requests:dict[str,tuple[float,str]]|None=None)->Output:
        if horizon_s<=0:raise ValueError('invalid horizon')
        blocked_until=blocked_until or {}
        lane_change_requests=lane_change_requests or {}
        if len({d.identity for d in specs})!=len(specs):raise ValueError('duplicate vehicle')
        for d in specs:
            if not d.route or any(name not in self.links for name in d.route) or d.arrival_s<0 or d.length_m<=0 or d.desired_speed_mps<=0 or d.acceleration_mps2<=0 or d.deceleration_mps2<=0:
                raise ValueError('invalid demand')
            if any(d.length_m>self.links[x].length_m for x in d.route):raise ValueError('vehicle longer than link')
            if self.connections is not None and any(v not in self.connections.get(u,()) for u,v in zip(d.route,d.route[1:])):
                raise ValueError("invalid route connection")
        if any(vid not in {d.identity for d in specs} or at<0 or target not in self.links
               for vid,(at,target) in lane_change_requests.items()):
            raise ValueError("invalid lane change request")
        pending=sorted(specs,key=lambda d:(d.arrival_s,d.identity))
        active:dict[str,Vehicle]={}
        output=Output()
        completed=set()
        changed=set()
        def current_link(v:Vehicle):
            return v.lane_override or v.spec.route[v.segment]
        clock=0.0
        ticks=int(horizon_s/self.dt)
        for it in range(ticks+1):
            clock=round(it*self.dt,9)
            if clock>horizon_s+EPS:break
            # Admission uses ONLY start-of-tick occupancy; simultaneous arrivals processed in stable order.
            for d in tuple(pending):
                if d.arrival_s>clock+EPS:break
                link=d.route[0]
                others=[v for v in active.values() if current_link(v)==link]
                min_rear=min((v.front_m-v.spec.length_m for v in others),default=float('inf'))
                if min_rear >= d.length_m+self.gap-EPS:  # front at length, gap before closest rear
                    active[d.identity]=Vehicle(d,front_m=d.length_m)
                    output.admitted_s[d.identity]=clock
                    pending.remove(d)
            # Deterministic lateral transfer between parallel equal-length links.
            # Only checks longitudinal interval overlap at the event time; NO lane-change maneuver trajectory.
            for mid,(requested,target) in sorted(lane_change_requests.items()):
                if mid not in active or mid in changed or clock<requested-EPS:continue
                v=active[mid];old=current_link(v)
                if target==old:
                    changed.add(mid);continue
                if target not in self.lateral_neighbors.get(old,()):
                    raise ValueError("unconnected lane-change request")
                conflicting=False
                for oid, other in active.items():
                    if oid==mid or current_link(other)!=target:continue
                    separate=(v.front_m+self.gap <= other.front_m-other.spec.length_m+EPS or
                              other.front_m+self.gap <= v.front_m-v.spec.length_m+EPS)
                    if not separate:conflicting=True;break
                if not conflicting:
                    v.lane_override=target
                    v.speed_mps=min(v.speed_mps,self.speed_cap(self.links[target]))
                    changed.add(mid)
                    output.lane_changes.append((clock,mid,old,target))
            output.occupancies.append((clock,{l:sum(current_link(v)==l for v in active.values()) for l in self.links}))
            output.queues.append((clock,sum(d.arrival_s<=clock+EPS for d in pending)))
            for mid,v in active.items():
                output.traces[mid].append((clock,current_link(v),round(v.front_m,6),round(v.speed_mps,6)))
            if it==ticks:break
            snapshot={mid:(current_link(v),v.front_m,v.speed_mps) for mid,v in active.items()}
            proposals=[]
            # Descending front distance within link; no crossing changes for same-tick leader movement.
            for mid,v in sorted(active.items(),key=lambda kv:(kv[1].spec.route[kv[1].segment],-kv[1].front_m,kv[0])):
                link_name=current_link(v);link=self.links[link_name]
                head_gap=float('inf')
                for another, (ln,x,_) in snapshot.items():
                    if another!=mid and ln==link_name and x>v.front_m:
                        head_gap=min(head_gap,x-active[another].spec.length_m-v.front_m-self.gap)
                head_gap=max(0.0,head_gap)
                distance_to_end=max(0.0,link.length_m-v.front_m)
                vtarget=min(v.spec.desired_speed_mps,self.speed_cap(link))
                # conservative upper bound on distance; reaction/delay not calibrated
                vnew=min(vtarget,v.speed_mps+v.spec.acceleration_mps2*self.dt)
                move=min(vnew*self.dt,head_gap,distance_to_end)
                # bus stop: do not leap over stop and enforce exact dwell interval.
                if v.spec.kind=='bus' and not v.stop_done:
                    for stop in self.stops:
                        if stop.link==link_name and stop.position_m>=v.front_m-EPS:
                            if v.front_m+move>=stop.position_m-EPS:
                                move=max(0.,stop.position_m-v.front_m)
                                v.dwell_end_s=clock+self.dt+stop.dwell_s
                                v.stop_done=True
                            break
                if v.dwell_end_s is not None and clock < v.dwell_end_s-EPS:
                    move=0.0
                vnew=move/self.dt
                proposals.append((mid,move,vnew))
            for mid,move,vnew in proposals:
                v=active[mid]
                v.front_m+=move
                v.speed_mps=vnew
            # End-of-link transfer: do not use downstream exit/space freed in the SAME tick.
            # Only vehicle positions that were already at stop line in the START snapshot can transfer.
            reservations:dict[str,list[tuple[float,float]]]=defaultdict(list)
            used_junction=set()
            done=[]
            for mid,v in sorted(active.items(),key=lambda p:(p[1].spec.arrival_s,p[0])):
                link_name=current_link(v);link=self.links[link_name]
                old_link,old_front,_=snapshot[mid]
                if old_front<link.length_m-EPS:continue
                if blocked_until.get(link_name,0.)>clock+EPS:
                    output.blocked['downstream_closed']+=1;continue
                if link_name in self.signals and not (self.signals[link_name].green(clock) and self.signals[link_name].green(clock + self.dt-1e-8)):
                    output.blocked['red']+=1;continue
                junction=link.junction
                if junction and (junction in used_junction or any(c.junction==junction and c.occupied(clock) for c in self.crossings)):
                    output.blocked['junction_or_pedestrian']+=1;continue
                if v.segment+1==len(v.spec.route):
                    done.append(mid)
                    if junction:used_junction.add(junction)
                    continue
                dest=v.spec.route[v.segment+1]
                dest_people=[(oid,u) for oid,u in active.items() if oid!=mid and snapshot[oid][0]==dest]
                tail=min((snapshot[oid][1]-u.spec.length_m for oid,u in dest_people),default=float('inf'))
                tail=min(tail,*( [x-vlen for x,vlen in reservations[dest]] or [float('inf')] ))
                # front position of transferred vehicle starts at vehicle length
                if tail < v.spec.length_m+self.gap-EPS:
                    output.blocked['no_receiving_space']+=1;continue
                reservations[dest].append((v.spec.length_m,v.spec.length_m))
                v.segment+=1
                v.lane_override=None
                v.front_m=v.spec.length_m
                v.speed_mps=0.
                output.transfers.append((round(clock+self.dt,9),mid,link_name,dest))
                if junction:used_junction.add(junction)
            for mid in done:
                output.completed_s[mid]=round(clock+self.dt,9)
                completed.add(mid)
                del active[mid]
            # The resulting state is for clock+dt.  All transfers use resources from the tick snapshot.
            for ln in self.links:
                vs=sorted((v for v in active.values() if current_link(v)==ln),key=lambda v:v.front_m)
                for a,b in zip(vs,vs[1:]):
                    if a.front_m>b.front_m-b.spec.length_m+self.gap+1e-7:
                        raise AssertionError(f'vehicle overlap on {ln}: {a.spec.identity}, {b.spec.identity}')
            if len(active)+len(pending)+len(completed)!=len(specs):raise AssertionError('vehicle conservation')
        output.blocked=dict(output.blocked)
        return output


def shortest_distance_route(links:list[Link],adjacency:dict[str,tuple[str,...]],start:str,goal:str):
    """Static graph reference. This does NOT select signal control timings."""
    lookup={x.name:x for x in links}
    pq=[(0.,start,(start,))]
    best={start:0.}
    while pq:
        d,node,path=heapq.heappop(pq)
        if d!=best[node]:continue
        if node==goal:return d,path
        for nxt in adjacency.get(node,()):
            nd=d+lookup[nxt].length_m
            if nd<best.get(nxt,float('inf')):
                best[nxt]=nd
                heapq.heappush(pq,(nd,nxt,path+(nxt,)))
    return float('inf'),()
