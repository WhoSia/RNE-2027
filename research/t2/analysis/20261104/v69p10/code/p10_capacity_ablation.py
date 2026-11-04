"""Independent P10 capacity-time ablation. No original-source mutation."""
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
import sys,csv,json
from dataclasses import replace
sys.path.insert(0,str(Path(__file__).parent/'code'))
from dt_convergence import SCENARIOS,PLANS,arrivals_for,make_config,run
from p10_boundary_trace import CASE,DTS
sp=spec_from_file_location('corridor_capacity_time_safe',Path(__file__).parent/'corridor_capacity_time_safe.py')
new=module_from_spec(sp);sys.modules[sp.name]=new;sp.loader.exec_module(new)

def compare():
 scenario,storage,seed,key=CASE
 s=next(s for s in SCENARIOS if s.name==scenario)
 p=next(p for p in PLANS if p.key==key)
 arrivals=arrivals_for(s,seed)
 rows=[]
 for dt in DTS:
  for method,runner in [('original',run),('capacity-time-gate',new.run)]:
   z=runner(replace(make_config(p,storage,horizon_s=1200),dt=dt),arrivals)
   def evt(vid,event,j):
    return next(e['t'] for e in z['events'] if e['id']==vid and e['event']==event and e['j']==j)
   t1=evt(1,'receive',1);t8=evt(8,'connector_enter',0)
   rows.append({'dt_s':dt,'method':method,'vehicle1_link_exit_s':round(t1,8),'vehicle8_enter_s':round(t8,8),
                'retroactive_capacity_use':t8<t1 and t8>40 and t8<53,
                'exposure_vehicle_seconds':round(z['summary']['exposure_vehicle_seconds'],6),
                'completed':z['summary']['completed'],'issues':z['summary']['issues']})
 return rows
if __name__=='__main__':
 rows=compare();out=Path(__file__).parent
 with (out/'capacity_gate_ablation.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(json.dumps(rows,indent=2))
