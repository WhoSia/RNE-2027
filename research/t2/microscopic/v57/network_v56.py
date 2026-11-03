"""T2 v5.2 explicit finite turn-bay queues, derived from T2 v5.1 based on v5.0.1 synthetic 3-signal corridor: per-vehicle IDM on finite links and legal OD routes.
Not SUMO, not calibrated, not physically safety-certified. Educational research prototype.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
from geometry import ClearanceGraph
import math
import random

DT = 0.5
JUNCTIONS = 3
LENGTHS = {"M0": 160., "M1": 180., "M2": 180., "S0": 85., "S1": 85., "S2": 85.}
DRIVER_LENGTH = 4.5
MIN_GAP = 2.0
# Every turn is an explicit incoming-lane -> downstream-lane connection.
# This is a conservative two-stage *movement* conflict model, not a geometrically
# validated real intersection. Same incoming lane is FIFO (no turn pocket yet).
SUCCESSOR = {"M0": "M1", "M1": "M2", "M2": None,
             "S0": "M1", "S1": "M2", "S2": None}
SOURCES = ("M0", "S0", "S1", "S2")
MOVEMENT_STAGE = {"main_through":"main", "main_exit":"main", "main_outflow":"main",
                  "side_merge":"side", "side_exit":"side"}
MOVEMENTS = tuple(MOVEMENT_STAGE)
CONFLICTS = {a: frozenset(b for b in MOVEMENTS if b!=a) for a in MOVEMENTS}

@dataclass(frozen=True)
class TurnParameters:
    # Model parameter study, NOT a measured urban saturation flow or safety clearance.
    main_through_s: float=2.0
    main_exit_s: float=2.0
    side_merge_s: float=2.0
    side_exit_s: float=2.0

    def __post_init__(self):
        if any(not math.isfinite(v) or v<0.5 for v in vars(self).values()):
            raise ValueError("turn headways must be finite >=0.5 s")

    def headway(self,movement):
        if movement not in MOVEMENT_STAGE:raise ValueError("unknown movement")
        return {"main_through":self.main_through_s,"main_outflow":self.main_through_s,"main_exit":self.main_exit_s,
                "side_merge":self.side_merge_s,"side_exit":self.side_exit_s}[movement]


@dataclass(frozen=True)
class PocketGeometry:
    """Lengths of local main-exit bays at J0, J1, J2 (metres).

    Zero means there is no separate bay. A positive bay is a logical parallel
    lane over the final length of the corresponding main approach. Lateral
    transfer is discrete, not a continuous lateral car-following law.
    """
    lengths_m: tuple[float,float,float]=(0.,0.,0.)
    def __post_init__(self):
        if len(self.lengths_m)!=3:raise ValueError('three bay lengths required')
        if self.lengths_m[2]!=0:raise ValueError('terminal main outflow is not a turn exit: no bay at J2')
        for j,length in enumerate(self.lengths_m):
            if not math.isfinite(length) or length<0 or length>=LENGTHS[f'M{j}']-DRIVER_LENGTH:
                raise ValueError('bay length must fit within main approach')
    def capacity(self,j:int):
        length=self.lengths_m[j]
        return 0 if length<=0 else max(1,math.floor(length/(DRIVER_LENGTH+MIN_GAP)))


def base_link(link:str):
    return 'M'+link[1:] if link.startswith('P') else link


def movement_for(link, target):
    link=base_link(link)
    if link not in SUCCESSOR:raise ValueError("invalid incoming link")
    if target not in (SUCCESSOR[link],None):
        raise ValueError("nonadjacent turn")
    if link=='M2' and target is None:return 'main_outflow'
    return ("main_" if link.startswith("M") else "side_") + \
        (("through" if link.startswith("M") else "merge") if target else "exit")


def check_route(route):
    if not route or route[0] not in SOURCES:
        raise ValueError("invalid source")
    for link,nxt in zip(route,route[1:]):
        if link not in SUCCESSOR or SUCCESSOR[link]!=nxt:
            raise ValueError("nonadjacent route")
    if route[-1] not in SUCCESSOR:raise ValueError("invalid destination")
    return True

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
    turn_green: tuple[int,int,int] = (0,0,0)
    def __post_init__(self):
        if len(self.main_green)!=3 or len(self.offset)!=3 or len(self.turn_green)!=3 or self.cycle<=0 or self.lost<0:
            raise ValueError('invalid signal')
        if any(t<0 for t in self.turn_green):raise ValueError('negative protected turn time')
        for j,g in enumerate(self.main_green):
            t=self.turn_green[j]
            lost_total=self.lost*(3 if t else 2)
            side=self.cycle-g-t-lost_total
            if g<self.min_green or side<self.min_green or (t and t<self.min_green):
                raise ValueError('insufficient phase green')
    def phase(self,j:int,t:float):
        if j not in (0,1,2): raise ValueError('invalid junction')
        p=(t-self.offset[j])%self.cycle
        g=self.main_green[j]
        if p<g:return 'main'
        if p<g+self.lost:return 'all_red'
        turn=self.turn_green[j]
        if turn and p<g+self.lost+turn:return 'turn'
        if turn and p<g+2*self.lost+turn:return 'all_red'
        if p<self.cycle-self.lost:return 'side'
        return 'all_red'

# Spatial correspondences are hypotheses for a synthetic four-way node,
# not ground-truthed geometry at any Korean junction.
GEOMETRY_MOVEMENTS = {
    'main_through': 'W>E', 'main_outflow': 'W>E',
    'main_exit': 'W>S', 'side_merge': 'N>E', 'side_exit': 'N>W',
}
GEOMETRY_GRAPH = ClearanceGraph(2.5)

@dataclass(frozen=True)
class ParallelSignalPlan:
    """Permit concurrent main and side vehicles in the first portion of main green.

    Only *geometry-compatible* movements are dispatched concurrently.
    A zero parallel window recovers the original plan's timing semantics.
    """
    base: SignalPlan
    parallel_window_s: float=10.
    @property
    def name(self):return self.base.name+f'_parallel{self.parallel_window_s:g}'
    @property
    def turn_green(self):return self.base.turn_green
    def phase(self,j,t):
        original=self.base.phase(j,t)
        p=(t-self.base.offset[j])%self.base.cycle
        if original=='main' and p<self.parallel_window_s:return 'parallel'
        return original

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


def simulate(plan:SignalPlan | ParallelSignalPlan, demands:list[Vehicle], horizon:float=580., dt:float=DT,
             save_trajectory:bool=False, driver:DriverParameters | None=None,
             turns:TurnParameters | None=None,
             pockets:PocketGeometry | None=None):
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
    if turns is None:turns=TurnParameters()
    if pockets is None:pockets=PocketGeometry()
    if any(t>0 and pockets.lengths_m[j]<=0 for j,t in enumerate(plan.turn_green)):
        raise ValueError('protected turn stage requires explicit turn bay')
    ids=[v.vid for v in demands]
    if len(ids)!=len(set(ids)):raise ValueError("duplicate vehicle ID")
    for v in demands:
        check_route(v.route)
        if not math.isfinite(v.born) or v.born<0 or abs(v.born/dt-round(v.born/dt))>1e-8:
            raise ValueError("birth times must be finite, nonnegative, and timestep aligned")
    vehicles={v.vid:Vehicle(vid=v.vid,born=v.born,route=v.route) for v in demands}
    arrivals=sorted(vehicles.values(),key=lambda v:(v.born,v.vid))
    # The link queue is in order of entering. The tail is index -1, front is index 0.
    lanes={k:deque() for k in LENGTHS}
    for j in range(3):
        if pockets.lengths_m[j]>0:lanes[f'P{j}']=deque()
    link_lengths={k:LENGTHS[base_link(k)] for k in lanes}
    waiting={k:deque() for k in ('M0','S0','S1','S2')}
    next_release={k:-100. for k in lanes}
    next_junction_release={j:-100. for j in range(3)}
    bay_diversions=0;bay_wait_ticks=0;bay_occupancy_max={f'P{j}':0 for j in range(3)}
    completed=[];events=[];crossings=[];snapshots=[];queue_series=[];generated=0;entered=0;vehicle_seconds=0.
    arrived_index=0; blocked=0; downstream_full_ticks=0; release_events=0; reconciled_followers=0
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
        # Divert an exit-bound vehicle into the finite parallel turn bay only
        # after it reaches the bay entrance. The maneuver has no longitudinal
        # teleport, though lateral transition time is idealized to zero.
        for j in range(3):
            length=pockets.lengths_m[j]
            if length<=0:continue
            base=f'M{j}';bay=f'P{j}';entrance=LENGTHS[base]-length
            for vid in list(lanes[base]):
                veh=vehicles[vid]
                if veh.link_idx+1<len(veh.route) or veh.x<entrance-1e-8:
                    continue
                if len(lanes[bay])>=pockets.capacity(j):
                    bay_wait_ticks+=1;continue
                if lanes[bay] and vehicles[lanes[bay][-1]].x-veh.x<DRIVER_LENGTH+MIN_GAP-1e-8:
                    bay_wait_ticks+=1;continue
                lanes[base].remove(vid);lanes[bay].append(vid)
                bay_diversions+=1
            bay_occupancy_max[bay]=max(bay_occupancy_max[bay],len(lanes[bay]))
        # Before integrating motion, build a dispatch set from the current
        # signal stage. Under 'parallel', independent lanes can run together
        # ONLY if their geometric movement paths are compatible.
        selected={}
        for j in range(3):
            stage=plan.phase(j,t)
            if stage=='side':
                selected[j]={f'S{j}'}
            elif stage=='turn':
                bay=f'P{j}'
                selected[j]={bay} if bay in lanes and lanes[bay] and t+1e-9>=next_release[bay] else set()
            elif stage in ('main','parallel'):
                candidates=[key for key in (f'M{j}',f'P{j}') if key in lanes and lanes[key]]
                candidates=[key for key in candidates if not (
                    key.startswith('M') and pockets.lengths_m[j]>0 and
                    vehicles[lanes[key][0]].link_idx==len(vehicles[lanes[key][0]].route)-1)]
                if plan.turn_green[j]:candidates=[key for key in candidates if not key.startswith('P')]
                candidates=[key for key in candidates if t+1e-9>=next_release[key]]
                first=max(candidates,key=lambda key:(vehicles[lanes[key][0]].x,
                        -next_release[key],key.startswith('P'))) if candidates else None
                chosen=set([first]) if first is not None else set()
                if stage=='parallel' and lanes[f'S{j}'] and t+1e-9>=next_release[f'S{j}']:
                    side=f'S{j}'
                    if not chosen:
                        chosen.add(side)
                    else:
                        lead=vehicles[lanes[first][0]]
                        lead_next=lead.route[lead.link_idx+1] if lead.link_idx+1<len(lead.route) else None
                        sidelead=vehicles[lanes[side][0]]
                        sidenext=sidelead.route[sidelead.link_idx+1] if sidelead.link_idx+1<len(sidelead.route) else None
                        m1=GEOMETRY_MOVEMENTS[movement_for(first,lead_next)]
                        m2=GEOMETRY_MOVEMENTS[movement_for(side,sidenext)]
                        if GEOMETRY_GRAPH.compatible((m1,m2)):
                            chosen.add(side)
                selected[j]=chosen
            else:selected[j]=set()
        # Compute full lane motions without moving a single vehicle to the next link yet.
        transfers=[]
        before_motion={}
        for link,queue in lanes.items():
            if not queue:continue
            j=int(link[1]);front=vehicles[queue[0]]
            target=front.route[front.link_idx+1] if front.link_idx+1<len(front.route) else None
            move_type=movement_for(link,target)
            expected_stage=('turn' if move_type=='main_exit' and plan.turn_green[j] else MOVEMENT_STAGE[move_type])
            movable=(link in selected.get(j,set()) and (plan.phase(j,t)==expected_stage or plan.phase(j,t)=='parallel')
                and t+1e-9>=next_release[link] and (plan.phase(j,t)=='parallel' or t+1e-9>=next_junction_release[j]))
            old=[(vehicles[vid].x,vehicles[vid].v) for vid in queue]
            before_motion[link]=old
            new=[]
            for k,vid in enumerate(queue):
                v=vehicles[vid]
                if k==0:
                    target=v.route[v.link_idx+1] if v.link_idx+1<len(v.route) else None
                    # Receiving space measured BEFORE transfers; no cross-tick same-step double hop.
                    downstream_clear=(target is None or not lanes[target] or vehicles[lanes[target][-1]].x>=DRIVER_LENGTH+MIN_GAP+1.)
                    if movable and not downstream_clear and v.x>=link_lengths[link]-15.:
                        downstream_full_ticks+=1
                    allowed=movable and downstream_clear
                    if allowed:gap=1e6; lead_v=v.v
                    else:gap=max(0.,link_lengths[link]-.3-v.x);lead_v=0.
                else:
                    leader_x,leader_v=old[k-1]
                    gap=max(0.,leader_x-DRIVER_LENGTH-v.x)
                a=idm_accel(v.v,gap,lead_v,desired=driver.desired_speed_mps,
                            a=driver.max_accel_mps2,b=driver.comfort_brake_mps2,
                            headway=driver.headway_s)
                candidate=max(0.,v.v+max(-7.,a)*dt)
                max_front=1e9 if (k==0 and allowed) else (link_lengths[link]-.3 if k==0 else new[k-1][0]-DRIVER_LENGTH-MIN_GAP)
                if link.startswith('M') and pockets.lengths_m[j]>0 and v.link_idx==len(v.route)-1:
                    # Exit-bound vehicles must enter their pocket; if the bay
                    # is full they queue at its beginning, blocking through.
                    max_front=min(max_front,LENGTHS[link]-pockets.lengths_m[j])
                # Bounded change prevents overlap in this discretization; no generalized crash-free theorem.
                next_x=min(v.x+candidate*dt,max_front)
                next_x=max(v.x,min(next_x,max_front))
                next_speed=max(0.,(next_x-v.x)/dt)
                new.append((next_x,next_speed))
                if next_speed<.5:v.waiting+=dt
                if k==0 and allowed and next_x>=link_lengths[link]-1e-8:
                    transfers.append((link,vid,target,next_x-link_lengths[link]))
            for vid,(x,speed) in zip(queue,new):
                vehicles[vid].x=x;vehicles[vid].v=speed
        # Commit crossings; check receiving space after motions and earlier transfers to prevent merge overlap.
        for link,vid,target,overflow in transfers:
            assert lanes[link] and lanes[link][0]==vid
            if target is not None and lanes[target]:
                tail=vehicles[lanes[target][-1]]
                if tail.x<DRIVER_LENGTH+MIN_GAP+1.+overflow:
                    # Transactional rejection: the leader's canceled crossing must
                    # not leave its followers in positions based on the crossed leader.
                    # Reconcile this WHOLE incoming lane against its pre-tick geometry.
                    prior=before_motion[link]
                    lane_ids=list(lanes[link])
                    assert lane_ids[0]==vid
                    previous_speed=vehicles[vid].v
                    vehicles[vid].x=min(link_lengths[link]-1e-6,max(prior[0][0],link_lengths[link]-.3))
                    vehicles[vid].v=max(0.,(vehicles[vid].x-prior[0][0])/dt)
                    if previous_speed>=.5 and vehicles[vid].v<.5:
                        vehicles[vid].waiting+=dt
                    prev=vehicles[vid].x
                    for k,other in enumerate(lane_ids[1:],1):
                        follower=vehicles[other]
                        new_x=min(follower.x,prev-DRIVER_LENGTH-MIN_GAP)
                        if new_x<prior[k][0]-1e-7:
                            raise AssertionError(("blocked transfer would require reverse movement",step,link,vid,k))
                        former_speed=follower.v
                        former_x=follower.x
                        follower.x=max(prior[k][0],new_x)
                        follower.v=max(0.,(follower.x-prior[k][0])/dt)
                        if former_speed>=.5 and follower.v<.5:
                            follower.waiting+=dt
                        if follower.x<former_x-1e-8:
                            reconciled_followers+=1
                        prev=follower.x
                    blocked+=1
                    continue
            lanes[link].popleft()
            move_type=movement_for(link,target)
            next_release[link]=t+turns.headway(move_type)
            next_junction_release[int(link[1])]=t+turns.headway(move_type)
            crossings.append(dict(t_s=t+dt,id=vid,junction=int(link[1]),
                from_link=base_link(link),to_link=target,movement=move_type,physical_lane=link,
                phase=plan.phase(int(link[1]),t)))
            assert crossings[-1]['phase'] in (('turn' if move_type=='main_exit' and plan.turn_green[int(link[1])] else MOVEMENT_STAGE[move_type]),'parallel')
            release_events+=1
            veh=vehicles[vid]
            if target is None:
                veh.finished=t+dt;completed.append(vid)
                events.append(dict(id=vid,origin=veh.route[0],destination=base_link(link),
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
            assert all(0<=vehicles[v].x<=link_lengths[link]+1e-8 for v in lane)
            for leader,follower in zip(lane,list(lane)[1:]):
                assert vehicles[leader].x-vehicles[follower].x>=DRIVER_LENGTH+MIN_GAP-1e-7, (step, t, link, leader, follower, vehicles[leader].x, vehicles[follower].x, blocked)
        if step%int(5/dt)==0:
            stopline={key:sum(1 for vid in lane if link_lengths[key]-vehicles[vid].x<=40 and vehicles[vid].v<2.0) for key,lane in lanes.items()}
            queue_series.append({'t_s':t,'completed':len(completed),'inside':inside,'upstream_pending':outside,
                **{f'queue_{k}':v for k,v in stopline.items()},
                'main_vehicles':sum(len(lanes[f'M{j}'])+len(lanes.get(f'P{j}',())) for j in range(3)),
                'side_vehicles':sum(len(lanes[f'S{j}']) for j in range(3)),
                'waiting_total':sum(1 for x in vehicles.values() if x.entered is not None and x.finished is None and x.v<.5),
                **{f'occupancy_{k}':len(lanes[k]) for k in lanes if k.startswith('P')}})
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
             'blocked_transfers':blocked,'reconciled_followers':reconciled_followers,'downstream_full_ticks':downstream_full_ticks,
             'release_events':release_events,
             'crossings_by_movement':{m:sum(e['movement']==m for e in crossings) for m in MOVEMENTS},
             'turn_clearance_s':vars(turns),
             'pocket_geometry_m':pockets.lengths_m,
             'pocket_capacity_vehicles':{f'P{j}':pockets.capacity(j) for j in range(3)},
             'pocket_diversions':bay_diversions,'pocket_wait_ticks':bay_wait_ticks,
             'pocket_peak_occupancy':bay_occupancy_max,
             'system_vehicle_seconds_in_horizon':vehicle_seconds,
             'completed_vehicle_seconds':completed_duration_total,
             'right_censored_vehicle_seconds':censored_duration_total,
             'exposure_reconstruction_error_s':vehicle_seconds-reconstructed_exposure,
             'exposure_seconds_per_generated':vehicle_seconds/generated if generated else None}
    summary['signal_turn_green_s']=plan.turn_green
    # Independent physical graph check of co-timed crossing events.
    simultaneous={}
    for e in crossings:
        key=(e['junction'],round(e['t_s']/dt))
        simultaneous.setdefault(key,[]).append(GEOMETRY_MOVEMENTS[e['movement']])
    for key,moves in simultaneous.items():
        if len(moves)>1 and not GEOMETRY_GRAPH.compatible(moves):
            raise AssertionError(('geometric crossing conflict',key,moves))
    summary['parallel_crossing_slots']=sum(len(moves)>1 for moves in simultaneous.values())
    summary['geometry_clearance_m']=GEOMETRY_GRAPH.separation
    return {'summary':summary,'trips':events,'queues':queue_series,'trajectories':snapshots,'crossings':crossings}
