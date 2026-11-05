"""Reproduce synthetic spatial-conflict witness and export audit data."""
import csv,json,hashlib,sys
from pathlib import Path
from dataclasses import asdict
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'src'))
from lane_fifo import Demand,simulate
rules={frozenset(('car','ped'))}
cases={
'legacy_global':[Demand(0,'car_A','a',('rA',),5,'car'),Demand(1,'ped_B','b',('rB',),1,'ped')],
'explicit_disjoint_zones':[Demand(0,'car_A','a',('rA',),5,'car','A'),Demand(1,'ped_B','b',('rB',),1,'ped','B')],
'explicit_same_zone':[Demand(0,'car_A','a',('rA',),5,'car','J'),Demand(1,'ped_B','b',('rB',),1,'ped','J')],
}
rows=[]
for key,demands in cases.items():
    result=simulate(demands,{'rA':1,'rB':1},rules)
    rows.append({'case':key,'ped_request_s':1,'ped_entry_s':result.entries['ped_B'],
                 'ped_wait_s':result.entries['ped_B']-1,'max_occupied_rA':result.max_occupation['rA'],
                 'max_occupied_rB':result.max_occupation['rB'], 'all_completed':len(result.exits)==2})
p=root/'results';p.mkdir(exist_ok=True)
with (p/'spatial_conflict_witness.csv').open('w',newline='',encoding='utf8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(p/'spatial_conflict_witness.json').write_text(json.dumps({'model':'research_only','policy':'frozen','rows':rows},indent=2),encoding='utf8')
print(json.dumps(rows,indent=2))
