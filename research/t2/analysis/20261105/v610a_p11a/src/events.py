"""Causally ordered event-time test engine, not a traffic micro-simulator.

At equal timestamps: free downstream occupancy first; then admit queued vehicles.
No action at t can use a release timestamped strictly after t.
"""
from dataclasses import dataclass,field
from heapq import heappush,heappop
from math import isfinite
from itertools import count
from network import Network

RELEASE,ARRIVAL,ADMIT=0,1,2
@dataclass(order=True,frozen=True)
class Event:
    time_s:float
    priority:int
    serial:int
    kind:str=field(compare=False)
    vehicle:str=field(compare=False)
    movement:str=field(compare=False)

@dataclass(frozen=True)
class Demand:
    vehicle:str
    movement:str
    arrival_s:float
    footprint_m:float=6.5
    def __post_init__(self):
        if not self.vehicle or not isfinite(self.arrival_s) or self.arrival_s<0 or not isfinite(self.footprint_m) or self.footprint_m<=0:
            raise ValueError('invalid demand')

class EventEngine:
    def __init__(self,net:Network,demands:tuple[Demand,...],horizon_s:float):
        if not isfinite(horizon_s) or horizon_s<=0:raise ValueError('invalid horizon')
        self.net=net;self.demands={d.vehicle:d for d in demands};self.horizon=horizon_s
        if len(self.demands)!=len(demands):raise ValueError('duplicate vehicle')
        self.events=[];self.serial=count();self.occupancy={l.id:0. for l in net.lanes};self.queues={m.id:[] for m in net.movements}
        self.completed=set();self.active=set();self.status={d.vehicle:'not_arrived' for d in demands};self.log=[];self.last_time=-1.
        for d in demands:
            net.movement(d.movement)
            if d.footprint_m>net.lane(net.movement(d.movement).to_lane).storage_m:
                raise ValueError('vehicle too large for receiving lane')
            self._push(d.arrival_s,ARRIVAL,'arrival',d.vehicle,d.movement)
        self._push(0,ADMIT,'admit_check','','')
        # Revisit queues at every phase boundary, including offsets.
        for plan in net.plans:
            t=0.0
            while t<horizon_s:
                _,_,remain=plan.at(t)
                # include future change only; ensures strictly advancing schedule
                if remain<=1e-9:raise AssertionError('zero-duration phase')
                t+=remain
                if t<=horizon_s:self._push(round(t,9),ADMIT,'admit_check','','')
    def _push(self,t,p,kind,v,m):
        if not isfinite(t) or t<self.last_time-1e-8:raise AssertionError('causality backdating')
        heappush(self.events,Event(t,p,next(self.serial),kind,v,m))
    def _log(self,e):self.log.append({'t_s':e.time_s,'event':e.kind,'vehicle':e.vehicle,'movement':e.movement})
    def run(self):
        while self.events:
            e=heappop(self.events)
            if e.time_s>self.horizon+1e-9:break
            if e.time_s<self.last_time-1e-8:raise AssertionError('clock reversal')
            self.last_time=e.time_s
            if e.kind=='arrival':
                if self.status[e.vehicle]!='not_arrived':raise AssertionError('duplicate demand')
                self.status[e.vehicle]='queued';self.queues[e.movement].append(e.vehicle);self._push(e.time_s,ADMIT,'admit_check','','')
            elif e.kind=='release':
                d=self.demands[e.vehicle]; m=self.net.movement(d.movement)
                if e.vehicle not in self.active:raise AssertionError('nonactive release')
                self.active.remove(e.vehicle);self.completed.add(e.vehicle);self.status[e.vehicle]='completed'
                self.occupancy[m.to_lane]-=d.footprint_m
                if self.occupancy[m.to_lane]<-1e-8:raise AssertionError('negative storage')
                self._push(e.time_s,ADMIT,'admit_check','','')
            elif e.kind=='admit_check':
                for m in self.net.movements:
                    if not self.queues[m.id]:continue
                    d=self.demands[self.queues[m.id][0]]
                    if self.occupancy[m.to_lane]+d.footprint_m>self.net.lane(m.to_lane).storage_m+1e-9:continue
                    if not self.net.plan(m.junction).permits(m.id,e.time_s,m.clearance_s):continue
                    # Connector exclusivity: simultaneously conflicting active movement forbidden.
                    if any(self.net.movement(self.demands[v].movement).id in m.conflicts for v in self.active):continue
                    self.queues[m.id].pop(0);self.active.add(d.vehicle);self.status[d.vehicle]='active'
                    self.occupancy[m.to_lane]+=d.footprint_m
                    self._push(e.time_s+m.clearance_s,RELEASE,'release',d.vehicle,m.id)
                    self._log(Event(e.time_s,ADMIT,e.serial,'admit',d.vehicle,m.id))
            else:raise AssertionError('unknown event')
            self._log(e)
            for l in self.net.lanes:
                if self.occupancy[l.id]<-1e-8 or self.occupancy[l.id]>l.storage_m+1e-8:raise AssertionError('capacity violation')
        return {'completed':len(self.completed),'total':len(self.demands),'unfinished':len(self.demands)-len(self.completed),'events':self.log,'peak_occupancy_m':dict(self.occupancy)}
