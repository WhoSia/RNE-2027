"""Reproduce the partial-overlap defect in the pinned P11-W reference and D22."""
import importlib.util
import json
from pathlib import Path
from src.lane_fifo import Demand, simulate

ROOT=Path(__file__).resolve().parent
rule={frozenset(('car','ped'))}
demands=[
    Demand(0,'car_A','A',('a',),5,'car',('north','shared')),
    Demand(1,'ped_B','B',('b',),2,'ped',('shared','south')),
    Demand(1,'car_C','C',('c',),1,'car',('far',)),
]
capacities={'a':1,'b':1,'c':1}
new=simulate(demands,capacities,rule)
base_path=ROOT/'baseline'/'lane_fifo_W_original.py'
spec=importlib.util.spec_from_file_location('w_baseline',base_path)
module=importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name]=module
spec.loader.exec_module(module)
old=module.simulate([module.Demand(*d.__dict__.values()) for d in demands],capacities,rule)
assert old.entries['ped_B']==1 and new.entries['ped_B']==5
assert new.entries['car_C']==1
record={
 'source':'synthetic fixed-duration events only',
 'policy_optimizer':'FROZEN',
 'cases':{
  'W_existing':{'entries':old.entries,'exits':old.exits},
  'X_multi_zone':{'entries':new.entries,'exits':new.exits},
 },
 'difference':{'ped_B_entry_delay_sec':new.entries['ped_B']-old.entries['ped_B'],
               'cause':'W compares equality of zone tuples, missing partial overlap',
               'C_unaffected':new.entries['car_C']==old.entries['car_C']},
 'limitations':['all zones reserved atomically for full duration','no longitudinal trajectory','no measured traffic or SUMO','not an intersection operating policy']
}
out=ROOT/'results';out.mkdir(exist_ok=True)
(out/'paired_partial_overlap.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(record,indent=2,ensure_ascii=False))
