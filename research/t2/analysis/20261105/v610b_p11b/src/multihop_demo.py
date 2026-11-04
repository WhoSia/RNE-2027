"""Small connected 2-junction test and paired offset experiment; synthetic only."""
from dataclasses import replace
from network import Lane,Movement,Phase,SignalPlan,Network
from multihop import RouteDemand,RouteEngine
import json,csv
from pathlib import Path

def make_network(offset=0, link_storage=13):
    lanes=(Lane('source',80,80),Lane('link',60,link_storage),Lane('sink',80,80),Lane('cross_in',60,60),Lane('cross_sink',80,80))
    movements=(Movement('J0_main','J0','source','link','straight',2),
               Movement('J1_main','J1','link','sink','straight',2,('J1_cross',)),
               Movement('J1_cross','J1','cross_in','cross_sink','left',2,('J1_main',)))
    plans=(SignalPlan('J0',(Phase(4,frozenset({'J0_main'})),Phase(2,frozenset()))),
           SignalPlan('J1',(Phase(3,frozenset({'J1_main'})),Phase(1,frozenset()),Phase(3,frozenset({'J1_cross'})),Phase(1,frozenset())),offset))
    return Network(lanes,movements,plans)

def run(offset,travel=3,storage=13,pattern='balanced'):
    ds=tuple([RouteDemand(f'M{i}',('J0_main','J1_main'),i*(2.1 if pattern=='main_peak' else 3.6)) for i in range(12)] +
             [RouteDemand(f'C{i}',('J1_cross',),i*(7.5 if pattern=='main_peak' else 3.8)) for i in range(8)])
    z=RouteEngine(make_network(offset,storage),ds,150,{'link':travel}).run()
    if z['unfinished']:raise AssertionError('incomplete benchmark')
    starts={d.vehicle:d.arrival_s for d in ds}
    exposure=sum(z['completion_times'][v]-starts[v] for v in starts)
    return {'offset_s':offset,'pattern':pattern,'storage_m':storage,'travel_s':travel,
            'completed':z['completed'],'total':z['total'],'total_system_time_veh_s':round(exposure,6),
            'max_link_occupancy_m':z['peak_occupancy_m']['link']}

if __name__=='__main__':
    rows=[run(off,travel,storage,pattern) for pattern in ('balanced','main_peak')
          for storage in (6.5,13) for travel in (1,3,5) for off in range(8)]
    out=Path(__file__).resolve().parents[1]/'results';out.mkdir(exist_ok=True)
    with (out/'multihop_offset_experiment.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    best={}
    for pattern in ('balanced','main_peak'):
        for storage in (6.5,13):
            for travel in (1,3,5):
                subset=[x for x in rows if (x['pattern'],x['storage_m'],x['travel_s'])==(pattern,storage,travel)]
                a=min(subset,key=lambda x:(x['total_system_time_veh_s'],x['offset_s']))
                best[f'{pattern}|{storage}|{travel}']=a
    (out/'multihop_summary.json').write_text(json.dumps({'executions':len(rows),'best':best},indent=2))
    print(json.dumps({'executions':len(rows),'best':best},indent=2))
