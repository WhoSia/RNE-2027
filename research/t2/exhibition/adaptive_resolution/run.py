"""Controlled lab comparisons; each policy has fresh caches."""
import json,time,gc
from fractions import Fraction as F
from model import Config,Model,witness_belief
from planner import Planner

def run():
    rows=[];b=witness_belief()
    for erasure,service in [(F(0),'fixed'),(F(1,4),'fixed'),(F(0),'random'),(F(1,4),'random')]:
        for schedule in [(1,),(1,2,3,4)]:
            for budget in [0,1,4,8]:
                c=Config(schedule=schedule,erasure=erasure,service=service,budget=budget);policies={}
                for label,p,d in [('free','free',4),('head','head',4),('full','full',4),('qmdp','adaptive',1),('depth2','adaptive',2),('exact','adaptive',4)]:
                    gc.collect();start=time.perf_counter_ns();m=Model(c);v=Planner(m,p,d).report(b);v['elapsed_ms']=(time.perf_counter_ns()-start)/1e6;policies[label]=v
                optimum=F(policies['exact']['objective'])
                for label,v in policies.items():
                    if F(v['objective'])<optimum or v['worst_credits']>budget:raise AssertionError('dominance/budget')
                    if label in ('qmdp','depth2','exact') and F(v['lower'])>optimum:raise AssertionError('bound')
                    v['regret']=str(F(v['objective'])-optimum)
                rows.append({'erasure':str(erasure),'service':service,'schedule':schedule,'budget':budget,'policies':policies})
    return rows
if __name__=='__main__':print(json.dumps(run(),indent=2))
