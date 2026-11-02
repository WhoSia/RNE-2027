"""T2 v4.9 synthetic 3-signal corridor: per-vehicle IDM on finite links and legal OD routes.
Not SUMO, not calibrated, not physically safety-certified. Educational research prototype.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
import math
import random

DT = 0.5
JUNCTIONS = 3
LENGTHS = {"M0": 160., "M1": 180., "M2": 180., "S0": 85., "S1": 85., "S2": 85.}
DRIVER_LENGTH = 4.5
MIN_GAP = 2.0

@dataclass(frozen=True)
class DriverParameters:
    """Dimensionally explicit sensitivity factors, not field-calibrated drivers."""
    desired_speed_mps: float = 13.0
    headway_s: float = 1.3
    max_accel_mps2: float = 1.5
    comfort_brake_mps2: float = 2.0

    def __post_init__(self):
        for v in (self.desired_speed_mps, self.headway_s,
                  self.max_accel_mps2, self.comfort_brake_mps2):
            if not math.isfinite(v) or v <= 0:
                raise ValueError("driver parameters must be finite and positive")


@dataclass
class Vehicle:
    vid: int
    born: float
    route: tuple[str, ...]
    link_idx: int = 0
    x: float = 0.
    v: float = 0.
    waiting: float = 0.
    entered: float | None = None
    finished: float | None = None
    @property
    def link(self):return self.route[self.link_idx]

@dataclass(frozen=True)
class SignalPlan:
    name: str
    main_green: tuple[int,int,int]
    offset: tuple[int,int,int]
    cycle: int = 60
    lost: int = 2
    min_green: int = 15
    def __post_init__(self):
        if len(self.main_green)!=3 or len(self.offset)!=3 or self.cycle<=0 or self.lost<0:
            raise ValueError('invalid signal')
        if any(not(self.min_green<=g<=self.cycle-2*self.lost-self.min_green) for g in self.main_green):
            raise ValueError('insufficient phase green')
    def phase(self,j:int,t:float):
        if j not in (0,1,2): raise ValueError('invalid junction')
        p=(t-self.offset[j])%self.cycle
        g=self.main_green[j]
        if p<g:return 'main'
        if p<g+self.lost:return 'all_red'
        if p<self.cycle-self.lost:return 'side'
        return 'all_red'

PLANS = (
    SignalPlan('fixed_32', (32,32,32),(0,0,0)),
    SignalPlan('coordinated_32', (32,32,32),(0,14,28)),
    SignalPlan('main_priority_38', (38,38,38),(0,14,28)),
    SignalPlan('side_priority_25', (25,25,25),(0,14,28)),
)

@dataclass(frozen=True)
class Demand:
    name:str
    main_per_min: float
    side_per_min: tuple[float,float,float]
    intermediate_exit: float = .25
    side_merge: float = .65
    def __post_init__(self):
        if self.main_per_min<0 or any(x<0 for x in self.side_per_min):raise ValueError('negative demand')
        if not 0<=self.intermediate_exit<=1 or not 0<=self.side_merge<=1:raise ValueError('invalid route fractions')

DEMANDS=(
    Demand('balanced', 13.0,(4.,4.,4.),.25,.55),
    Demand('main_peak', 21.0,(2.5,2.5,2.5),.2,.6),
    Demand('side_peak', 10.0,(10.,9.,9.),.25,.55),
)

def make_arrivals(d:Demand,seed:int,arrive_until:float=320.,dt:float=DT):
    """Exogenous time-stamped demands; same seed list reused for all controllers."""
    r=random.Random(seed);events=[];vid=0
    for step in range(int(arrive_until/dt)):
        t=step*dt
        for origin,rate in [('M0',d.main_per_min),*[(f'S{i}',rate) for i,rate in enumerate(d.side_per_min)]]:
            # Bernoulli attempts limited to <=1 per step per source.
            p=rate*dt/60
            if p>1:raise ValueError('arrival probability >1')
            if r.random()>=p:continue
            if origin=='M0':
                # 1/2 split between exits at J0/J1; all remaining finish after J2
                x=r.random()
                if x<d.intermediate_exit/2:route=('M0',)
                elif x<d.intermediate_exit:route=('M0','M1')
                else:route=('M0','M1','M2')
            else:
                j=int(origin[1])
                if j==2 or r.random()>=d.side_merge:route=(origin,)
                elif j==1:route=(origin,'M2')
                else:
                    route=(origin,'M1','M2') if r.random()<.65 else (origin,'M1')
            events.append(Vehicle(vid=vid,born=t,route=route));vid+=1
    return events


def idm_accel(v:float,gap:float,lead_v:float,
              desired:float=13.0,a:float=1.5,b:float=2.0,headway:float=1.3,min_gap:float=MIN_GAP):
    """IDM longitudinal acceleration in m/s²; x and net gap in metres."""
    if min(v,gap,lead_v)<-1e-10:raise ValueError('negative kinematics')
    star=min_gap+max(0., v*headway+v*(v-lead_v)/(2*math.sqrt(a*b)))
    return a*(1-(v/desired)**4-(star/max(gap,1e-4))**2)


def simulate(plan:SignalPlan, demands:list[Vehicle], horizon:float=580., dt:float=DT,
             save_trajectory:bool=False, driver:DriverParameters | None=None):
    """A simple car-following network with three signalized crossings.

    Assumptions: main/side incoming links each have one lane, competing for a single downstream
    lane (when turning). A red/all-red holds the first vehicle at the stop line. No conflict-free
    turn matrix, explicit lane-changing, pedestrians, transit stopping or graded roads. All
    arriving vehicles are on identical OD manifests across signal policies.

    Each vehicle has position/speed in its current link and traverses at most one junction
    per timestep. A separate pending demand queue records spillback beyond the model boundary.
    """
    if horizon<=0 or dt<=0:raise ValueError('time inputs')
    if not math.isclose(horizon/dt, round(horizon/dt), rel_tol=0., abs_tol=1e-9):
        raise ValueError('horizon must be an integer multiple of dt')
    if driver is None:driver=DriverParameters()
    vehicles={v.vid:Vehicle(vid=v.vid,born=v.born,route=v.route) for v in demands}
    arrivals=sorted(vehicles.values(),key=lambda v:(v.born,v.vid))
    # The link queue is in order of entering. The tail is index -1, front is index 0.
    lanes={k:deque() for k in LENGTHS}
    waiting={k:deque() for k in ('M0','S0','S1','S2')}
    controls={k:-100. for k in LENGTHS}
    completed=[];events=[];snapshots=[];queue_series=[];generated=0;entered=0;vehicle_seconds=0.
    arrived_index=0; blocked=0; downstream_full_ticks=0; release_events=0
    nsteps=int(horizon/dt)
    for step in range(nsteps):
        t=step*dt
        while arrived_index<len(arrivals) and arrivals[arrived_index].born<=t+1e-8:
            v=arrivals[arrived_index];waiting[v.route[0]].append(v.vid)
            arrived_index+=1;generated+=1
        # Integrate occupant exposure BEFORE this tick's crossing completions.
        # Vehicles completed at t+dt still consume dt vehicle-seconds on [t,t+dt).
        vehicle_seconds+=(generated-len(completed))*dt
        # Entrance supply: a new vehicle must start behind the current last vehicle with clearance.
        for source,pending in waiting.items():
            if not pending:continue
            tail=lanes[source][-1] if lanes[source] else None
            if tail is not None and vehicles[tail].x<DRIVER_LENGTH+MIN_GAP+1:
                continue
            vid=pending.popleft();v=vehicles[vid];v.entered=t;v.x=0.;v.v=0.
            lanes[source].append(vid);entered+=1
        # Compute full lane motions without moving a single vehicle to the next link yet.
        transfers=[]
        for link,queue in lanes.items():
            if not queue:continue
            j=int(link[1]);movement='main' if link[0]=='M' else 'side'
            movable=(plan.phase(j,t)==movement and t-controls[link]>=2.0)
            old=[(vehicles[vid].x,vehicles[vid].v) for vid in queue]
            new=[]
            for k,vid in enumerate(queue):
                v=vehicles[vid]
                if k==0:
                    target=v.route[v.link_idx+1] if v.link_idx+1<len(v.route) else None
                    # Receiving space measured BEFORE transfers; no cross-tick same-step double hop.
                    downstream_clear=(target is None or not lanes[target] or vehicles[lanes[target][-1]].x>=DRIVER_LENGTH+MIN_GAP+1.)
                    if movable and not downstream_clear and v.x>=LENGTHS[link]-15.:
                        downstream_full_ticks+=1
                    allowed=movable and downstream_clear
                    if allowed:gap=1e6; lead_v=v.v
                    else:gap=max(0.,LENGTHS[link]-.3-v.x);lead_v=0.
                else:
                    leader_x,leader_v=old[k-1]
                    gap=max(0.,leader_x-DRIVER_LENGTH-v.x)
                a=idm_accel(v.v,gap,lead_v,desired=driver.desired_speed_mps,
                            a=driver.max_accel_mps2,b=driver.comfort_brake_mps2,
                            headway=driver.headway_s)
                candidate=max(0.,v.v+max(-7.,a)*dt)
                max_front=1e9 if (k==0 and allowed) else (LENGTHS[link]-.3 if k==0 else new[k-1][0]-DRIVER_LENGTH-MIN_GAP)
                # Bounded change prevents overlap in this discretization; no generalized crash-free theorem.
                next_x=min(v.x+candidate*dt,max_front)
                next_x=max(v.x,min(next_x,max_front))
                next_speed=max(0.,(next_x-v.x)/dt)
                new.append((next_x,next_speed))
                if next_speed<.5:v.waiting+=dt
                if k==0 and allowed and next_x>=LENGTHS[link]-1e-8:
                    transfers.append((link,vid,target,next_x-LENGTHS[link]))
            for vid,(x,speed) in zip(queue,new):
                vehicles[vid].x=x;vehicles[vid].v=speed
        # Commit crossings; check receiving space after motions and earlier transfers to prevent merge overlap.
        for link,vid,target,overflow in transfers:
            assert lanes[link] and lanes[link][0]==vid
            if target is not None and lanes[target]:
                tail=vehicles[lanes[target][-1]]
                if tail.x<DRIVER_LENGTH+MIN_GAP+1.+overflow:
                    # cannot fit - stop at the junction boundary
                    vehicles[vid].x=LENGTHS[link]-.3;vehicles[vid].v=0.;blocked+=1
                    continue
            lanes[link].popleft();controls[link]=t;release_events+=1
            veh=vehicles[vid]
            if target is None:
                veh.finished=t+dt;completed.append(vid)
                events.append(dict(id=vid,origin=veh.route[0],destination=link,
                                   born_s=veh.born,finished_s=veh.finished,
                                   duration_s=veh.finished-veh.born,stopped_s=veh.waiting))
            else:
                veh.link_idx+=1
                veh.x=min(overflow,.8);veh.v=max(0.,veh.v)
                lanes[target].append(vid)
        # Ordered lane invariants and global conservation.
        inside=sum(len(lane) for lane in lanes.values())
        outside=sum(len(q) for q in waiting.values())
        assert generated==inside+outside+len(completed)
        for link,lane in lanes.items():
            assert all(0<=vehicles[v].x<=LENGTHS[link]+1e-8 for v in lane)
            for leader,follower in zip(lane,list(lane)[1:]):
                assert vehicles[leader].x-vehicles[follower].x>=DRIVER_LENGTH+MIN_GAP-1e-7
        if step%int(5/dt)==0:
            stopline={key:sum(1 for vid in lane if LENGTHS[key]-vehicles[vid].x<=40 and vehicles[vid].v<2.0) for key,lane in lanes.items()}
            queue_series.append({'t_s':t,'completed':len(completed),'inside':inside,'upstream_pending':outside,
                **{f'queue_{k}':v for k,v in stopline.items()},
                'main_vehicles':sum(len(lanes[f'M{j}']) for j in range(3)),
                'side_vehicles':sum(len(lanes[f'S{j}']) for j in range(3)),
                'waiting_total':sum(1 for x in vehicles.values() if x.entered is not None and x.finished is None and x.v<.5)})
        if save_trajectory and step%int(2/dt)==0:
            for link,lane in lanes.items():
                for vid in lane:
                    v=vehicles[vid];snapshots.append({'t_s':t,'id':vid,'link':link,'x_m':v.x,'speed_mps':v.v})
    generated=len([x for x in arrivals if x.born<horizon])
    assert generated==len(completed)+sum(len(x) for x in lanes.values())+sum(len(x) for x in waiting.values())
    # Independently reconstruct integral of unfinished entities from each birth to
    # completion or right-censoring at horizon. This does not double-count future time.
    completed_duration_total=sum(x['duration_s'] for x in events)
    censored_duration_total=sum(horizon-v.born for v in vehicles.values()
                                if v.finished is None and v.born<horizon)
    reconstructed_exposure=completed_duration_total+censored_duration_total
    assert abs(vehicle_seconds-reconstructed_exposure)<1e-6, (vehicle_seconds,reconstructed_exposure)
    durations=sorted(x['duration_s'] for x in events)
    mean=lambda a:sum(a)/len(a) if a else None
    quantile=lambda a,p:a[min(len(a)-1,math.ceil(len(a)*p)-1)] if a else None
    summary={'policy':plan.name,'generated':generated,'entered':entered,'completed':len(completed),
             'remaining_inside':sum(len(x) for x in lanes.values()),
             'pending_boundary':sum(len(x) for x in waiting.values()),
             'mean_completed_duration_s':mean(durations),
             'p90_completed_duration_s':quantile(durations,.9),
             'mean_completed_stopped_s':mean([x['stopped_s'] for x in events]),
             'blocked_transfers':blocked,'downstream_full_ticks':downstream_full_ticks,
             'release_events':release_events,
             'system_vehicle_seconds_in_horizon':vehicle_seconds,
             'completed_vehicle_seconds':completed_duration_total,
             'right_censored_vehicle_seconds':censored_duration_total,
             'exposure_reconstruction_error_s':vehicle_seconds-reconstructed_exposure,
             'exposure_seconds_per_generated':vehicle_seconds/generated if generated else None}
    return {'summary':summary,'trips':events,'queues':queue_series,'trajectories':snapshots}
