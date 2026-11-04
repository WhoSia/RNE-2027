"""P10 minimal mechanistic witness: immutable original P2, no SUMO or field data."""
from __future__ import annotations
from dataclasses import replace
from pathlib import Path
import csv, json, sys
sys.path.insert(0,str(Path(__file__).parent/'code'))
from dt_convergence import SCENARIOS, PLANS, arrivals_for, make_config, run
from vehicle_schema import get_vehicle_spec

DTS=(.5,.4,.25,.2,.125,.1,.0625,.05)
CASE=('upstream_peak',18.,223,(24.,24.,24.))

def run_trace():
    sn,storage,seed,key=CASE
    scenario=next(s for s in SCENARIOS if s.name==sn)
    plan=next(p for p in PLANS if p.key==key)
    arrivals=arrivals_for(scenario,seed)
    spec=get_vehicle_spec('car')
    cfg=make_config(plan,storage,horizon_s=1200.)
    tl=cfg.timeline_at(0)
    side_end=tl.walk_start_s
    speed=min(8.,4.)
    clearance=(18.85+spec.length_m)/speed+spec.connector_clearance_buffer_s
    last_admissible=side_end-clearance
    assert tl.phase(last_admissible)=='S' and tl.green_remaining('S',last_admissible)+1e-9 >= clearance
    assert sum(arrivals[i].kind=='car' for i in (1,2,8))==3
    assert 2*spec.storage_footprint_m<=storage<3*spec.storage_footprint_m
    rows=[]
    for dt in DTS:
        result=run(replace(cfg,dt=dt),arrivals)
        events=result['events']
        def event(vid,typ,j):
            return next(x['t'] for x in events if x['id']==vid and x['event']==typ and x['j']==j)
        t1=event(1,'receive',1)
        t8=event(8,'connector_enter',0)
        t8_exit=event(8,'connector_exit',0)
        rows.append({'dt_s':dt,'link_receives_vehicle_1_at_s':round(t1,8),
                     'vehicle_8_enters_j0_at_s':round(t8,8),
                     'vehicle_8_exits_j0_at_s':round(t8_exit,8),
                     'last_side_entry_s':round(last_admissible,8),
                     'enter_after_last_feasible_s':t8>last_admissible+1e-6,
                     'entry_timestamp_before_link_receipt_s':round(t1-t8,8) if t8<t1 else 0,
                     'exposure_vehicle_seconds':round(result['summary']['exposure_vehicle_seconds'],7),
                     'all_completed':result['summary']['all_completed'],
                     'state_issues':result['summary']['issues']})
    return {'source_case':{'scenario':sn,'storage_m':storage,'seed':seed,'policy':key,'vehicle_1':1,'vehicle_2':2,'vehicle_8':8,'vehicle_count':len(arrivals)},
            'mechanism':{'side_green_end_s':side_end,'vehicle_car_clearance_s':clearance,
                         'last_side_entry_s':last_admissible,
                         'car_storage_m':spec.storage_footprint_m,
                         'two_cars_storage_m':2*spec.storage_footprint_m,
                         'three_cars_storage_m':3*spec.storage_footprint_m,
                         'link_storage_m':storage},'runs':rows}

def main():
    out=Path(__file__).parent
    evidence=run_trace()
    with (out/'boundary_trace.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(evidence['runs'][0]));w.writeheader();w.writerows(evidence['runs'])
    (out/'boundary_mechanism.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(evidence,indent=2))
if __name__=='__main__':main()
