"""Reproduce independent 9-policy synthetic search on new typed signal model."""
import csv,json
from pathlib import Path
from network import Lane,Movement,Phase,SignalPlan,Network
from events import Demand
from policy_search import optimize

NET=Network((Lane('up_main',80,50),Lane('up_side',80,50),Lane('out',18,18)),
 (Movement('main','J','up_main','out','straight',2,('side',)),Movement('side','J','up_side','out','left',2,('main',))),
 (SignalPlan('J',(Phase(5,frozenset({'main'})),Phase(1,frozenset()),Phase(5,frozenset({'side'})),Phase(1,frozenset()))),))
CASES={
 'main_peak':tuple([Demand(f'M{i}','main',i*2.3) for i in range(16)]+[Demand(f'S{i}','side',i*7.3) for i in range(5)]),
 'side_peak':tuple([Demand(f'M{i}','main',i*7.3) for i in range(5)]+[Demand(f'S{i}','side',i*2.3) for i in range(16)]),
 'balanced':tuple([Demand(f'M{i}','main',i*4.3) for i in range(10)]+[Demand(f'S{i}','side',i*4.3) for i in range(10)])
}
def main():
 rows=[];summary={}
 for case,demand in CASES.items():
  result=optimize(NET,'J',demand,100,12,(3,4,5,6,7,8),(0,1,2))
  # 18 choices; include candidate list for inspection
  for r in result:rows.append({'case':case,**r.__dict__})
  best=result[0]
  summary[case]={'policies':len(result),'best_main_green_s':best.split_main_s,'best_offset_s':best.offset_s,
                 'best_wait_vehicle_s':best.wait_veh_s,'completed':best.completed,'total':best.total,
                 'best_policy_is_unique':sum(r.unfinished==best.unfinished and r.wait_veh_s==best.wait_veh_s for r in result)==1}
 out=Path(__file__).parents[1]/'results';out.mkdir(exist_ok=True)
 with (out/'signal_policy_search.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (out/'signal_policy_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
