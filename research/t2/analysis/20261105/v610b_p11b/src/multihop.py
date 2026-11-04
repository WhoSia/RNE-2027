"""v6.10-B independent event-driven multi-junction route prototype.

Physical conventions: receiving-link footprint is reserved at connector admission,
and released ONLY on the subsequent connector admission or terminal exit.
The earliest downstream admission is link-ready time; not an instantaneous jump.
At an equal timestamp exits and link readiness are processed before admissions.
Upstream source demands wait outside network storage (explicit limitation).
No lane changing, saturation flow headway, continuous geometry or field calibration.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from heapq import heappop, heappush
from itertools import count
from math import isfinite
from collections import deque
from network import Network

EXIT, READY, ARRIVE, CHECK = 0, 1, 2, 3

@dataclass(frozen=True)
class RouteDemand:
    vehicle: str
    movements: tuple[str, ...]
    arrival_s: float
    footprint_m: float = 6.5
    def __post_init__(self):
        if not self.vehicle or not self.movements or not isfinite(self.arrival_s) or self.arrival_s < 0:
            raise ValueError('bad route demand')
        if not isfinite(self.footprint_m) or self.footprint_m <= 0:
            raise ValueError('bad footprint')

@dataclass(order=True,frozen=True)
class Event:
    t: float
    rank: int
    serial: int
    kind: str=field(compare=False)
    vehicle: str=field(compare=False, default='')

class RouteEngine:
    def __init__(self, net:Network, demands: tuple[RouteDemand,...], horizon_s:float,
                 link_travel_s:dict[str,float]):
        if not isfinite(horizon_s) or horizon_s<=0:raise ValueError('bad horizon')
        self.net,self.horizon=net,horizon_s
        self.demands={d.vehicle:d for d in demands}
        if len(self.demands)!=len(demands):raise ValueError('duplicate vehicles')
        self.travel={l.id:float(link_travel_s.get(l.id,0)) for l in net.lanes}
        if any(not isfinite(v) or v<0 for v in self.travel.values()):raise ValueError('bad travel times')
        self.movements={m.id:m for m in net.movements}
        for d in demands:
            route=[self.movements[x] for x in d.movements]
            if any(m.to_lane!=n.from_lane for m,n in zip(route,route[1:])):
                raise ValueError('route discontinuity')
            if any(d.footprint_m>net.lane(m.to_lane).storage_m for m in route):
                raise ValueError('vehicle footprint exceeds receiving capacity')
        self.occ={l.id:0.0 for l in net.lanes}
        self.queues={m.id:deque() for m in net.movements}
        self.stage={d.vehicle:0 for d in demands}
        self.place={d.vehicle:'not_arrived' for d in demands}
        self.active={} # vehicle -> movement
        self.holder={} # vehicle -> reserved/occupied lane, if any
        self.completed={}
        self.log=[];self.queue=[];self.seq=count();self.now=-1.0
        self.peak={l.id:0 for l in net.lanes}
        for d in demands:self.push(d.arrival_s,ARRIVE,'arrival',d.vehicle)
        self.push(0,CHECK,'check')
        for plan in net.plans:
            t=0.0
            while t<horizon_s-1e-10:
                _,_,remain=plan.at(t)
                if remain<=1e-10:raise AssertionError('stuck phase boundary')
                t=round(t+remain,10)
                if t<=horizon_s:self.push(t,CHECK,'check')
    def push(self,t,rank,kind,vehicle=''):
        if not isfinite(t) or t<self.now-1e-8:raise AssertionError('retroactive event scheduling')
        heappush(self.queue,Event(t,rank,next(self.seq),kind,vehicle))
    def log_event(self,kind,vid='',movement='',lane=''):
        self.log.append({'t_s':round(self.now,10),'event':kind,'vehicle':vid,'movement':movement,'lane':lane})
    def validate(self):
        for l in self.net.lanes:
            if not -1e-8<=self.occ[l.id]<=l.storage_m+1e-8:raise AssertionError('storage exceeded')
        reserved={lid:0 for lid in self.occ}
        for v,lid in self.holder.items():reserved[lid]+=self.demands[v].footprint_m
        if any(abs(self.occ[l]-reserved[l])>1e-8 for l in self.occ):raise AssertionError('occupancy ledger mismatch')
        if any(v in self.completed for v in self.active):raise AssertionError('vehicle active and finished')
    def run(self):
        while self.queue:
            event=heappop(self.queue)
            if event.t>self.horizon+1e-9:break
            if event.t<self.now-1e-8:raise AssertionError('time reversal')
            self.now=event.t;v=event.vehicle
            if event.kind=='arrival':
                if self.place[v]!='not_arrived':raise AssertionError('duplicate arrival')
                m=self.demands[v].movements[0]
                self.queues[m].append(v);self.place[v]='queued'
                self.log_event('arrival',v,m);self.push(self.now,CHECK,'check')
            elif event.kind=='link_ready':
                if self.place[v]!='in_transit':raise AssertionError('ready before connector exit')
                m=self.demands[v].movements[self.stage[v]]
                self.queues[m].append(v);self.place[v]='queued'
                self.log_event('link_ready',v,m,self.holder[v]);self.push(self.now,CHECK,'check')
            elif event.kind=='connector_exit':
                if v not in self.active:raise AssertionError('release without connector')
                m_id=self.active.pop(v);d=self.demands[v]
                self.log_event('connector_exit',v,m_id,self.holder[v]);self.stage[v]+=1
                if self.stage[v]==len(d.movements):
                    lane=self.holder.pop(v);self.occ[lane]-=d.footprint_m
                    self.completed[v]=self.now;self.place[v]='completed'
                    self.log_event('complete',v,m_id,lane)
                    self.push(self.now,CHECK,'check')
                else:
                    self.place[v]='in_transit'
                    lane=self.holder[v]
                    self.push(self.now+self.travel[lane],READY,'link_ready',v)
            elif event.kind=='check':
                # A single deterministic admission per movement per check; continue via CHECK events
                for mid, waiting in self.queues.items():
                    if not waiting:continue
                    m=self.movements[mid];v=waiting[0];d=self.demands[v]
                    if any(x==mid or x in m.conflicts for x in self.active.values()):continue
                    if not self.net.plan(m.junction).permits(mid,self.now,m.clearance_s):continue
                    if self.occ[m.to_lane]+d.footprint_m>self.net.lane(m.to_lane).storage_m+1e-9:continue
                    # A vehicle may only release a previously occupied lane at its NEXT legal admission.
                    waiting.popleft()
                    if v in self.holder:
                        old=self.holder.pop(v);self.occ[old]-=d.footprint_m
                        self.log_event('upstream_freed',v,mid,old)
                    self.occ[m.to_lane]+=d.footprint_m
                    self.peak[m.to_lane]=max(self.peak[m.to_lane],self.occ[m.to_lane])
                    self.holder[v]=m.to_lane;self.active[v]=mid;self.place[v]='in_connector'
                    self.log_event('admit',v,mid,m.to_lane)
                    self.push(self.now+m.clearance_s,EXIT,'connector_exit',v)
            else:raise AssertionError('unknown event')
            self.validate()
        # Explicitly count undeparted/unqueued/in-transit as unfinished.
        return {'total':len(self.demands),'completed':len(self.completed),
                'unfinished':len(self.demands)-len(self.completed),
                'completion_times':self.completed,'events':self.log,
                'peak_occupancy_m':self.peak, 'final_occupancy_m':self.occ,
                'states':self.place}
