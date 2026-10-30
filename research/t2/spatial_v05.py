"""R&E T2 v0.5: auditable split-diverge *toy* cellular simulator.

The geometry factor is the global fork coordinate in 25-ft cells; the
capacity factor is a virtual cap K on physical bay occupancy.  K is NOT
an independent field-engineering intervention on a real pocket.
Signal modes leading/lagging model disjoint protected greens.  No field
calibration, no true velocity/braking or lane-changing behavior.
Standard library only.  Python 3.10+.
"""
from __future__ import annotations
from collections import Counter, deque
from dataclasses import dataclass, replace
import random


@dataclass(frozen=True)
class Config:
    duration: int = 4200
    cycle: int = 150
    through_green: int = 60
    left_green: int = 54
    signal_mode: str = "leading"  # leading, lagging, legacy_overlap
    fork_cells: int = -13  # global fork; bay entrance is fork+1
    bay_limit: int | None = None  # max number vehicles; virtual admission cap
    approach_ft: int = 2000
    demand_vph: int = 3000
    left_fraction: float = .4
    outer_straight_fraction: float = .55
    seed: int = 42
    speed_cells: int = 2
    gap_cells: int = 1
    headway_s: int = 2
    update_mode: str = "sequential"  # sequential forward sweep or synchronous parallel
    clearance_s: int = 0  # default reproduces first v0.5 experiment; 3 invokes phase schedule


def validate(c: Config) -> int:
    if c.duration <= 0 or c.cycle <= 0 or c.through_green <= 0 or c.left_green <= 0:
        raise ValueError("positive duration, cycle and green lengths required")
    if c.signal_mode not in ("leading", "lagging", "legacy_overlap"):
        raise ValueError("unrecognized signal mode")
    if c.clearance_s < 0 or (c.signal_mode=="legacy_overlap" and c.clearance_s):
        raise ValueError("clearance requires protected leading or lagging phase")
    if c.signal_mode != "legacy_overlap" and c.through_green + c.left_green+2*c.clearance_s > c.cycle:
        raise ValueError("protected greens must not overlap")
    if c.signal_mode == "legacy_overlap" and max(c.through_green,c.left_green)>c.cycle:
        raise ValueError("green cannot exceed cycle")
    if c.approach_ft % 25 or c.approach_ft <= 0:
        raise ValueError("approach length must be positive multiple of 25 ft")
    cells=c.approach_ft//25
    if not (-cells < c.fork_cells <= -5):
        raise ValueError("fork must be inside approach and ≥4 cells from stopline")
    if c.update_mode not in ("sequential", "parallel"):
        raise ValueError("invalid update mode")
    if c.gap_cells < 0 or c.speed_cells < 1 or c.headway_s < 1:
        raise ValueError("invalid movement parameters")
    if c.demand_vph < 0 or not 0 <= c.left_fraction <= 1 or not 0 <= c.outer_straight_fraction <= 1:
        raise ValueError("invalid demand fractions")
    # Bay entrance at fork+1; signal queue nose at x=-gap-1.
    # Packed max occupancy based on minimum centre-to-centre separation.
    first = c.fork_cells + 1
    last = -c.gap_cells - 1
    if first > last:
        raise ValueError("bay cannot accommodate stopline")
    physical_slots = (last-first)//(c.gap_cells+1)+1
    if c.bay_limit is not None and not 1 <= c.bay_limit <= physical_slots:
        raise ValueError(f"virtual bay limit must be 1..{physical_slots} for fork={c.fork_cells}")
    return physical_slots


def signal(c: Config, t: int) -> tuple[bool,bool]:
    if c.clearance_s:
        from signal_phases_v05 import PhaseConfig, greens
        return greens(t, PhaseConfig(cycle=c.cycle,green_left=c.left_green,
                                     green_through=c.through_green,
                                     clearance=c.clearance_s,order=c.signal_mode))
    phase=t % c.cycle
    if c.signal_mode == "leading":
        return c.left_green <= phase < c.left_green+c.through_green, phase < c.left_green
    if c.signal_mode == "lagging":
        return phase < c.through_green, c.through_green <= phase < c.through_green+c.left_green
    return phase<c.through_green, phase<c.left_green


def build_arrivals(c: Config) -> tuple[tuple[int,str,str],...]:
    """Fixed time stream independent of fork/capacity/signal intervention."""
    rng=random.Random(c.seed)
    arrivals=[]
    for t in range(c.duration):
        for _ in range((t+1)*c.demand_vph//3600-t*c.demand_vph//3600):
            left=rng.random()<c.left_fraction
            lane='upstream' if left or rng.random()>=c.outer_straight_fraction else 'outer'
            arrivals.append((t,'L' if left else 'S',lane))
    return tuple(arrivals)


def simulate(c: Config=Config(), arrivals: tuple[tuple[int,str,str],...] | None=None,
             *, audit: bool=True, keep_events: bool=False) -> dict:
    slots=validate(c)
    if arrivals is None:
        arrivals=build_arrivals(c)
    if any(t<0 or t>=c.duration or route not in ('S','L') or lane not in ('upstream','outer')
           or (route=='L' and lane!='upstream') for t,route,lane in arrivals):
        raise ValueError('invalid explicit arrivals')
    if any(arrivals[i][0]>arrivals[i+1][0] for i in range(len(arrivals)-1)):
        raise ValueError('arrivals must be sorted by nondecreasing time')
    cells=c.approach_ft//25
    nodes=('upstream','downstream','outer','bay')
    lanes={key:[] for key in nodes}
    waiting={'upstream':deque(),'outer':deque()}
    vehicles=[{'id':i,'arrive':t,'route':route,'lane':lane,'x':None}
              for i,(t,route,lane) in enumerate(arrivals)]
    index=0
    count=Counter()
    last_exit={key:-1000 for key in ('downstream','outer','bay')}
    events=[]
    exits_by_cycle=Counter()
    exits_by_route=Counter()
    first_bad=None
    prev_x={}

    def event(t,v,kind):
        if keep_events:
            events.append((t,v['id'],kind,v['x']))

    def move(row,stop):
        # A sequential sweep lets followers use an already-updated leader state.
        # A parallel update evaluates each bound from the preceding time-step state.
        prev=[v['x'] for v in row] if c.update_mode=='parallel' else None
        for i,v in enumerate(row):
            leader=(prev[i-1] if prev is not None else row[i-1]['x']) if i else stop
            bound=leader-c.gap_cells-1
            new_x=min(v['x']+c.speed_cells,bound)
            if new_x<v['x']:
                raise AssertionError(('backward_move',v['id'],v['x'],new_x))
            v['x']=new_x

    for t in range(c.duration):
        while index<len(vehicles) and vehicles[index]['arrive']<=t:
            v=vehicles[index]
            waiting[v['lane']].append(v)
            index+=1
        sg,lg=signal(c,t)
        for lane,green in (('bay',lg),('downstream',sg),('outer',sg)):
            row=lanes[lane]
            if green and not row:
                count['green_idle_'+lane+'_s']+=1
            if green and row and row[0]['x'] >= -c.speed_cells and t-last_exit[lane]>=c.headway_s:
                v=row.pop(0)
                if (lane=='bay') != (v['route']=='L'):
                    raise AssertionError(('wrong_exit_route',v['id'],lane))
                count['exit_'+lane]+=1
                exits_by_cycle[t//c.cycle]+=1
                exits_by_route[v['route']]+=1
                last_exit[lane]=t
                prev_x.pop(v['id'],None)
                event(t,v,'exit_'+lane)
        for lane in ('bay','downstream','outer'):
            move(lanes[lane],0)
        move(lanes['upstream'], c.fork_cells+c.gap_cells+1)
        upstream=lanes['upstream']
        if upstream and upstream[0]['x']>=c.fork_cells:
            v=upstream[0]
            target_lane='bay' if v['route']=='L' else 'downstream'
            target=lanes[target_lane]
            transfer_x=c.fork_cells+1
            if target_lane=='bay' and c.bay_limit is not None and len(target)>=c.bay_limit:
                count['fork_block_cap_s']+=1
            elif target and target[-1]['x']<transfer_x+c.gap_cells+1:
                count['fork_block_gap_'+target_lane+'_s']+=1
            else:
                upstream.pop(0)
                if transfer_x < v['x']:
                    raise AssertionError(('transfer_backwards',v['id']))
                v['x']=transfer_x
                v['lane']=target_lane
                target.append(v)
                count['transfer_'+target_lane]+=1
                event(t,v,'transfer_'+target_lane)
        for lane in ('upstream','outer'):
            if waiting[lane] and (not lanes[lane] or lanes[lane][-1]['x']>=-cells+c.gap_cells+1):
                v=waiting[lane].popleft()
                v['x']=-cells
                lanes[lane].append(v)
                count['admit_'+lane]+=1
                event(t,v,'admit_'+lane)
        if audit:
            active=[v for row in lanes.values() for v in row]
            ids=[v['id'] for v in active]
            if len(set(ids))!=len(ids):
                raise AssertionError(('duplicate_ownership',t))
            for lane,row in lanes.items():
                if any(row[i]['x']-row[i+1]['x'] < c.gap_cells+1 for i in range(len(row)-1)):
                    raise AssertionError(('collision',t,lane))
                if any(v['lane']!=lane for v in row):
                    raise AssertionError(('wrong_lane',t,lane))
                for v in row:
                    if v['id'] in prev_x and v['x']<prev_x[v['id']]:
                        raise AssertionError(('backwards',t,v['id']))
                    if lane=='upstream' and not -cells<=v['x']<=c.fork_cells:
                        raise AssertionError(('upstream_outside',t,v['id'],v['x']))
                    if lane=='bay' and not c.fork_cells+1<=v['x']<=-c.gap_cells-1:
                        raise AssertionError(('bay_outside',t,v['id'],v['x']))
            if c.bay_limit is not None and len(lanes['bay'])>c.bay_limit:
                raise AssertionError(('cap_exceeded',t))
            prev_x={v['id']:v['x'] for v in active}
            living=sum(map(len,lanes.values()))+sum(map(len,waiting.values()))
            exited=sum(v for k,v in count.items() if k.startswith('exit_'))
            if index != living+exited:
                raise AssertionError(('conservation_t',t,index,living,exited))
    count['arrivals']=len(vehicles)
    count['exits']=sum(v for k,v in count.items() if k.startswith('exit_'))
    count['remaining']=sum(map(len,lanes.values()))+sum(map(len,waiting.values()))
    if count['arrivals']!=count['exits']+count['remaining']:
        raise AssertionError('global conservation')
    count['bay_physical_slots']=slots
    count['fork_cells']=c.fork_cells
    return {'stats':dict(count),'cycle_exits':dict(exits_by_cycle),
            'route_exits':dict(exits_by_route),'events':events}


if __name__=='__main__':
    for mode in ('leading','lagging'):
        for fork in (-21,-13):
            for cap in (2,4):
                c=Config(signal_mode=mode,fork_cells=fork,bay_limit=cap,seed=0)
                r=simulate(c)
                print(mode,fork,cap,r['stats']['exits'])
