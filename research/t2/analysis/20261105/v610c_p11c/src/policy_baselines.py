"""P11-C explicit, strictly model-conditional policy-evaluation baselines.
Fixed, even-design, sequential prefix, and exhaustively evaluated oracle.
All methods see the SAME candidate policies, demands, objective and constraints.
This is a static offline plan search, NOT a real-time/field controller.
"""
from __future__ import annotations
from dataclasses import dataclass
from network import Network,Lane
from multihop_demo import make_network
from multihop import RouteDemand,RouteEngine

@dataclass(frozen=True)
class Trial:
    pattern:str
    source_storage_m:float
    link_storage_m:float
    travel_s:float
    offset_s:int
    completed:int
    total:int
    system_time_veh_s:float
    peak_source_m:float
    peak_link_m:float

def demand(pattern):
    if pattern not in ('balanced','main_peak'):
        raise ValueError('unsupported pattern')
    return tuple([RouteDemand(f'M{i}',('J0_main','J1_main'),i*(2.1 if pattern=='main_peak' else 3.6)) for i in range(12)]+
                 [RouteDemand(f'C{i}',('J1_cross',),i*(7.5 if pattern=='main_peak' else 3.8)) for i in range(8)])

def scenario_network(offset,source_storage,link_storage):
    base=make_network(offset=offset,link_storage=link_storage)
    lanes=tuple(Lane(l.id,l.length_m,source_storage if l.id in ('source','cross_in') else l.storage_m) for l in base.lanes)
    return Network(lanes,base.movements,base.plans)

def evaluate(pattern,source_storage,link_storage,travel,offset,horizon=180):
    a=demand(pattern)
    z=RouteEngine(scenario_network(offset,source_storage,link_storage),a,horizon,{'link':travel}).run()
    if z['unfinished']:
        raise AssertionError('benchmark censored: widen horizon or change model')
    starts={d.vehicle:d.arrival_s for d in a}
    value=sum(z['completion_times'][v]-starts[v] for v in starts)
    return Trial(pattern,source_storage,link_storage,travel,offset,z['completed'],z['total'],round(value,6),
                 z['peak_source_occupancy_m']['source'],z['peak_occupancy_m']['link'])

# Each non-oracle alternative is limited to four oracle-score queries at most.
CANDIDATE_POLICIES={
    'fixed_0':(0,),
    'even_grid_4':(0,2,4,6),
    'sequential_4':(0,1,2,3),
    'shifted_grid_4':(1,3,5,7),
    'oracle_all_8':tuple(range(8)),
}

def compare(pattern,source_storage,link_storage,travel):
    trials={off:evaluate(pattern,source_storage,link_storage,travel,off) for off in range(8)}
    best=min(trials.values(),key=lambda x:(x.system_time_veh_s,x.offset_s))
    rows=[]
    for name,offsets in CANDIDATE_POLICIES.items():
        cand=min((trials[o] for o in offsets),key=lambda x:(x.system_time_veh_s,x.offset_s))
        rows.append({'pattern':pattern,'source_storage_m':source_storage,'link_storage_m':link_storage,
                     'travel_s':travel,'policy_search':name,'eval_budget':len(offsets),
                     'chosen_offset_s':cand.offset_s,'score_veh_s':cand.system_time_veh_s,
                     'oracle_offset_s':best.offset_s,'oracle_score_veh_s':best.system_time_veh_s,
                     'regret_vs_oracle_veh_s':round(cand.system_time_veh_s-best.system_time_veh_s,6),
                     'completed':cand.completed,'peak_source_m':cand.peak_source_m})
    return rows,tuple(trials.values())
