"""Reproduce v5.9 standalone trajectory sensitivity results; standard library only."""
import csv,json
from itertools import product
from pathlib import Path
from bezier_dynamics import Dynamics,make_profile,crossing_occupancy,example_turn,example_through
R=Path(__file__).parent
rows=[]
for shape,curve in [('turn',example_turn()),('through',example_through())]:
 for lat,entry,maxspeed in product((1.,1.8,3.),(3.,7.,11.),(9.,13.)):
  p=make_profile(curve,Dynamics(lateral_accel=lat,max_speed=maxspeed),entry)
  o=crossing_occupancy(p)
  rows.append(dict(shape=shape,lateral_limit_mps2=lat,entry_speed_mps=entry,maximum_speed_mps=maxspeed,
    full_path_time_s=round(p[-1]['t_s'],4),zone_occupancy_exact_s=round(o['exact_duration_s'],4),
    zone_occupancy_rounded_s=o['duration_s'],max_lateral_mps2=round(max(k['a_lat_mps2'] for k in p),4),
    max_speed_real_mps=round(max(k['v_mps'] for k in p),4)))
with (R/'dynamics_sweep.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for name,curve in [('turn',example_turn()),('through',example_through())]:
 p=make_profile(curve,Dynamics(),7.)
 with (R/f'{name}_trace.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(p[0]));w.writeheader();w.writerows(p)
summary=dict(runs=len(rows),turn_min_zone_s=min(r['zone_occupancy_rounded_s'] for r in rows if r['shape']=='turn'),
 turn_max_zone_s=max(r['zone_occupancy_rounded_s'] for r in rows if r['shape']=='turn'),
 through_min_zone_s=min(r['zone_occupancy_rounded_s'] for r in rows if r['shape']=='through'),
 through_max_zone_s=max(r['zone_occupancy_rounded_s'] for r in rows if r['shape']=='through'))
(R/'experiment_summary.json').write_text(json.dumps(summary,indent=2))
print(summary)
