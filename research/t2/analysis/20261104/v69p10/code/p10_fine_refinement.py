"""P10 nested refinement on capacity-time-gated exploratory copy."""
from pathlib import Path
from dataclasses import replace
import csv,json
from p10_capacity_ablation import SCENARIOS,PLANS,arrivals_for,make_config,new
DTS=(.05,.04,.025,.02,.0125,.01)
def compute():
 s=next(x for x in SCENARIOS if x.name=='upstream_peak');p=next(x for x in PLANS if x.key==(24.,24.,24.));a=arrivals_for(s,223)
 rows=[]
 for dt in DTS:
  z=new.run(replace(make_config(p,18,horizon_s=1200),dt=dt),a)
  def find(vid,t,j):return next(e['t'] for e in z['events'] if e['id']==vid and e['event']==t and e['j']==j)
  r1=find(1,'receive',1);e8=find(8,'connector_enter',0)
  rows.append({'dt_s':dt,'vehicle1_received_at_s':round(r1,7),'vehicle8_entered_at_s':round(e8,7),
                'vehicle8_in_first_side_green':e8<53,
                'exposure_vehicle_seconds':round(z['summary']['exposure_vehicle_seconds'],6),
                'all_completed':z['summary']['all_completed'],'issues':z['summary']['issues']})
 return rows
if __name__=='__main__':
 rows=compute();p=Path(__file__).parent
 with (p/'fine_refinement.csv').open('w',newline='',encoding='utf8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(json.dumps(rows,indent=2))
