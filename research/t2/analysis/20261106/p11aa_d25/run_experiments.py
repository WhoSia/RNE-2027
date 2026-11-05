"""Reproduce D25 synthetic geometry/GTFS edge cases; never optimizes signal phases."""
import csv
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'src'))
from phase_network import Step, Movement, StorageGeometry, simulate

ROOT=Path(__file__).parent
OUT=ROOT/'results'
OUT.mkdir(exist_ok=True)

def vehicle(name, at, duration=4):
    return Movement(name,at,'same_lane','vehicle',(Step(('A',),duration),))

scenarios={}
scenarios['two_cars']=[vehicle('first',0),vehicle('second',1)]
scenarios['bus_car']=[vehicle('first',0),vehicle('second',1)]
lengths={'two_cars':{'first':4500,'second':4500},'bus_car':{'first':11000,'second':4500}}
for name, movements in scenarios.items():
    nominal=simulate(movements,{'A':2})
    physical=simulate(movements,{'A':2},storage=StorageGeometry({'A':15000},lengths[name],2000))
    scenarios[name]={'nominal_starts':nominal.starts,'geometry_starts':physical.starts,'geometry_finishes':physical.finishes,
                     'zone_length_mm':15000,'gap_mm':2000,'vehicle_lengths_mm':lengths[name]}
rows=[]
for length in range(12000,20001,500):
    for gap in range(1000,3001,500):
        z=simulate([vehicle('first',0),vehicle('second',1)],{'A':2},
                   storage=StorageGeometry({'A':length},{'first':11000,'second':4500},gap))
        rows.append({'zone_length_mm':length,'gap_mm':gap,'second_entry_tick':z.starts['second'],
                     'required_two_vehicles_mm':15500+gap})
with (OUT/'length_gap_sweep.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
record={'source':'synthetic_only','scenarios':scenarios,'sweep':{'rows':len(rows),'length_min_mm':12000,'length_max_mm':20000,
        'gap_min_mm':1000,'gap_max_mm':3000},'validated_gtfs':'synthetic_fixture_only','p10_original_replay':'not_executed',
        'signal_policy':'P12_FROZEN'}
(OUT/'D25_results.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'cases':{k:v['geometry_starts'] for k,v in scenarios.items()},'sweep_count':len(rows)},indent=2))
