"""Historical v5.9 speed-profile admission clipping audit; no field calibration."""
import csv
from itertools import product
from bezier_dynamics import Dynamics,make_profile,example_turn,example_through
rows=[]
for shape,curve in (("turn",example_turn()),("through",example_through())):
 for lat,entry,max_speed in product((1.,1.8,3.),(3.,7.,11.),(9.,13.)):
  cfg=Dynamics(lateral_accel=lat,max_speed=max_speed)
  p=make_profile(curve,cfg,entry)
  effective=p[0]['v_mps']
  rows.append(dict(shape=shape,lateral_accel=lat,requested_entry_mps=entry,max_speed_mps=max_speed,
   effective_entry_mps=round(effective,6),entry_clipped=int(effective<entry-1e-9),
   clip_mps=round(entry-effective,6)))
with open('admission_audit.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
print('runs',len(rows),'clipped',sum(x['entry_clipped'] for x in rows), 'clipped turning',sum(x['entry_clipped'] for x in rows if x['shape']=='turn'))
