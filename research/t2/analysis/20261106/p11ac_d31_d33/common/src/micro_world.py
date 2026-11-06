"""D27-D28: deterministic microscopic *reference*, not calibrated road safety software.
Single-direction lanes, discrete time. Snapshot-based synchronous updating.
All lengths m, speed m/s, time s. No real-road control actuation.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import defaultdict
from math import isfinite

@dataclass(frozen=True)
class Road:
    name: str
    length_m: float
    lanes: int
    speed_limit_mps: float
    downstream: tuple[str, ...] = ()
    grade: float = 0.0
    curve_radius_m: float | None = None
    capacity_override: int | None = None

@dataclass(frozen=True)
class Vehicle:
    identity: str
    route: tuple[str, ...]
    depart_s: int
    lane: int = 0
    length_m: float = 4.5
    desired_mps: float = 12.0
    accel_mps2: float = 1.5
    decel_mps2: float = 3.0
    bus_dwell_s: int = 0
    stop_road: str | None = None
    target_lane: int | None = None  # optional one-time lane choice within start road

@dataclass
class State:
    spec: Vehicle
    road_ix: int = 0
    lane: int = 0
    rear_m: float = 0.0
    speed_mps: float = 0.0
    dwell_left: int = 0
    waiting_s: int = 0
    entered_at: int = 0

@dataclass(frozen=True)
class FixedSignal:
    cycle_s: int = 60
    green_s: int = 30
    offset_s: int = 0
    def permits(self, t: int) -> bool:
        if self.cycle_s <= 0 or not 0 < self.green_s <= self.cycle_s:
            raise ValueError('invalid fixed signal')
        return (t-self.offset_s) % self.cycle_s < self.green_s

@dataclass
class Output:
    admissions: dict[str, int] = field(default_factory=dict)
    finishes: dict[str, int] = field(default_factory=dict)
    states: dict[int, dict[str, tuple[str,int,float,float]]] = field(default_factory=dict)
    events: list[tuple[int,str,str,str]] = field(default_factory=list)
    max_queue: int = 0
    collision_violations: int = 0
    throughput_by_road: dict[str,int] = field(default_factory=dict)


def run(roads: dict[str,Road], demand: list[Vehicle], *, horizon_s=180, dt_s=1,
        minimum_gap_m=2.0, signals: dict[str,FixedSignal]|None=None,
        pedestrians: dict[str,list[tuple[int,int]]]|None=None, controller=None) -> Output:
    if dt_s != 1: raise ValueError('reference accepts exactly 1s time steps; convergence is NOT established')
    if horizon_s<1 or type(horizon_s) is not int or minimum_gap_m<0:raise ValueError('invalid horizon/gap')
    if not roads:raise ValueError('empty roads')
    for name,r in roads.items():
        if name!=r.name or r.length_m<=0 or r.lanes<1 or r.speed_limit_mps<=0 or not isfinite(r.grade):
            raise ValueError('invalid road geometry')
        if not -0.25<=r.grade<=0.25:raise ValueError('reference grade outside test envelope')
        if r.curve_radius_m is not None and r.curve_radius_m<=0:raise ValueError('invalid curvature')
        if any(link not in roads for link in r.downstream):raise ValueError('unknown connection')
    ids=set()
    for v in demand:
        if not v.identity or v.identity in ids or not v.route or v.depart_s<0 or type(v.depart_s) is not int:
            raise ValueError('invalid demand')
        ids.add(v.identity)
        if any(road not in roads for road in v.route) or any(b not in roads[a].downstream for a,b in zip(v.route,v.route[1:])):
            raise ValueError('discontinuous route')
        if v.lane<0 or v.lane>=roads[v.route[0]].lanes or v.length_m<=0 or v.desired_mps<=0 or v.accel_mps2<=0 or v.decel_mps2<=0 or v.bus_dwell_s<0:
            raise ValueError('invalid vehicle physics')
        if v.stop_road is not None and v.stop_road not in v.route:raise ValueError('unknown bus stop road')
        if v.target_lane is not None and (type(v.target_lane) is not int or not 0<=v.target_lane<roads[v.route[0]].lanes):
            raise ValueError('invalid target lane')
    sig=signals or {}; ped=pedestrians or {}
    for name in set(sig)|set(ped):
        if name not in roads:raise ValueError('unknown intersection')
    states:dict[str,State]={}; done=set(); out=Output(throughput_by_road={k:0 for k in roads})
    pending=sorted(demand,key=lambda v:(v.depart_s,v.identity))
    def occupants(road,lane,source):
        return sorted([s for s in source.values() if s.spec.route[s.road_ix]==road and s.lane==lane],key=lambda s:s.rear_m)
    def gap_ok(road,lane,rear,length,source,exclude=None):
        if rear<0 or rear+length>roads[road].length_m+1e-9:return False
        for x in occupants(road,lane,source):
            if x.spec.identity==exclude:continue
            if not (rear+length+minimum_gap_m<=x.rear_m+1e-9 or x.rear_m+x.spec.length_m+minimum_gap_m<=rear+1e-9):return False
        return True
    def signal_ok(road,t):
        if controller is not None and road in controller.approaches and not controller.permits(road,t):return False
        if road in sig and not sig[road].permits(t):return False
        if any(a<=t<b for a,b in ped.get(road,[])):return False
        return True
    if controller is not None and sig:
        raise ValueError('use fixed signals OR a controller, not both')
    for t in range(horizon_s):
        if controller is not None:
            # Read only upstream sensors from the current snapshot.
            # No future vehicle outcomes or test cohort information is given.
            requests = {road: sum(v.route[0] == road and v.depart_s <= t for v in pending)
                        + sum(s.spec.route[s.road_ix] == road for s in states.values())
                        for road in controller.approaches}
            controller.observe(t, requests)
        # Entry at current t uses road space *before* advancement over [t,t+1).
        waiting=[]
        for v in pending:
            if v.depart_s<=t and gap_ok(v.route[0],v.lane,0,v.length_m,states):
                states[v.identity]=State(v,lane=v.lane,entered_at=t)
                out.admissions[v.identity]=t;out.events.append((t,'admit',v.identity,v.route[0]))
            else:waiting.append(v)
        pending=waiting
        out.max_queue=max(out.max_queue,len([v for v in pending if v.depart_s<=t]))
        # Lane-change requests are non-optimizing and accepted only in an empty gap.
        # Snapshot check avoids accepting crossing/simultaneous opposite swaps.
        lane_snapshot={k:(v.spec.route[v.road_ix],v.lane,v.rear_m) for k,v in states.items()}
        for mid in sorted(states):
            s=states[mid];target=s.spec.target_lane
            if target is None or s.road_ix!=0 or target==s.lane:continue
            road=s.spec.route[0]
            opposite=any(other!=mid and r==road and l==target and
                         states[other].spec.target_lane==s.lane and abs(x-s.rear_m)<s.spec.length_m+minimum_gap_m
                         for other,(r,l,x) in lane_snapshot.items())
            if not opposite and gap_ok(road,target,s.rear_m,s.spec.length_m,states,exclude=mid):
                s.lane=target
                out.events.append((t,'lane_change',mid,road))
        # Compute all movements from frozen snapshot, order front to back per lane.
        frozen={k:State(v.spec,v.road_ix,v.lane,v.rear_m,v.speed_mps,v.dwell_left,v.waiting_s,v.entered_at) for k,v in states.items()}
        candidates={}
        for mid,s in frozen.items():
            roadname=s.spec.route[s.road_ix];r=roads[roadname]
            if s.dwell_left>0:
                candidates[mid]=(roadname,s.lane,s.rear_m,0.0,s.dwell_left-1,False)
                continue
            # Curve and grade penalties are simplified reference constraints, not calibrated physics.
            vmax=min(r.speed_limit_mps,s.spec.desired_mps)
            if r.curve_radius_m is not None:vmax=min(vmax,(2.0*r.curve_radius_m)**0.5)
            if r.grade>0:vmax=max(0.5,vmax*(1-min(r.grade,0.2)))
            speed=min(vmax,s.speed_mps+s.spec.accel_mps2*dt_s)
            lane_neighbors=[x for x in occupants(roadname,s.lane,frozen) if x.spec.identity!=mid and x.rear_m>s.rear_m]
            if lane_neighbors:
                leader=min(lane_neighbors,key=lambda x:x.rear_m)
                room=max(0,leader.rear_m-(s.rear_m+s.spec.length_m)-minimum_gap_m)
                speed=min(speed,room/dt_s)
            front=s.rear_m+s.spec.length_m
            limit=max(0.0,r.length_m-front)
            if s.road_ix<len(s.spec.route)-1 and signal_ok(roadname,t):
                next_road=s.spec.route[s.road_ix+1]
                # Must be able to move wholly into next road, reserve at its entry.
                transfer_possible=gap_ok(next_road, min(s.lane,roads[next_road].lanes-1),0,s.spec.length_m,frozen)
            else:transfer_possible=False
            if speed*dt_s >=limit and (s.road_ix==len(s.spec.route)-1 or transfer_possible):
                if not signal_ok(roadname,t):speed=min(speed,limit/dt_s)
                else:candidates[mid]=(roadname,s.lane,s.rear_m,speed,0,True);continue
            speed=min(speed,limit/dt_s)
            candidates[mid]=(roadname,s.lane,min(s.rear_m+speed*dt_s,r.length_m-s.spec.length_m),speed,0,False)
        # Evaluate transitions with a current-time reservation; no retroactive release.
        nextstates={}
        for mid in sorted(candidates,key=lambda i:(-frozen[i].rear_m,i)):
            road,lane,rear,speed,dwell,transfer=candidates[mid]
            s=frozen[mid]; ix=s.road_ix;nr=road;nl=lane;nx=rear;exit_road=False
            if transfer:
                exit_road=True
                if ix+1<len(s.spec.route):
                    nr=s.spec.route[ix+1];nl=min(lane,roads[nr].lanes-1);nx=0.0
                    if not gap_ok(nr,nl,0,s.spec.length_m,nextstates) or not gap_ok(nr,nl,0,s.spec.length_m,frozen):
                        exit_road=False;nr=road;nl=lane;nx=roads[road].length_m-s.spec.length_m;speed=0
                else:
                    out.finishes[mid]=t+1;out.events.append((t+1,'finish',mid,road));out.throughput_by_road[road]+=1
                    done.add(mid);continue
            if exit_road:
                ix+=1;speed=0;out.throughput_by_road[road]+=1
                out.events.append((t+1,'transfer',mid,nr))
            if s.spec.stop_road==nr and s.spec.bus_dwell_s and nr!=road and s.spec.bus_dwell_s>0:
                dwell=s.spec.bus_dwell_s
            nextstates[mid]=State(s.spec,ix,nl,nx,speed,dwell,s.waiting_s+int(speed==0),s.entered_at)
        # Safety oracle of resultant snapshot. If it fails, do not count it as a successful model.
        for nr,r in roads.items():
            for lane in range(r.lanes):
                here=occupants(nr,lane,nextstates)
                for behind,ahead in zip(here,here[1:]):
                    if behind.rear_m+behind.spec.length_m+minimum_gap_m>ahead.rear_m+1e-7:
                        out.collision_violations+=1
                        raise AssertionError(f'overlap at {t}: {behind.spec.identity} / {ahead.spec.identity}')
        states=nextstates
        out.states[t+1]={mid:(s.spec.route[s.road_ix],s.lane,round(s.rear_m,6),round(s.speed_mps,6)) for mid,s in states.items()}
        assert set(out.finishes).isdisjoint(states)
        assert len(states)+len(out.finishes)+len(pending)==len(demand)
    return out
