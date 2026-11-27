"""Frozen conditional finite-population acceptance suite, not traffic sampling."""
from itertools import product
from fractions import Fraction as F
from model import Config, Model, witness_belief, mass
from planner import Planner
from lazy_certificate import select_lazy
import json

POLICIES=(('free','free',4),('head','head',4),('full','full',4),('qmdp','adaptive',1),('depth2','adaptive',2),('exact','adaptive',4))
FIXED=('free','head','full')

def run():
    out=[]
    for name,erasure,service in [('ideal',F(0),'fixed'),('broad',F(1,4),'random')]:
        for schedule in [(1,),(1,2,3,4)]:
            c=Config(schedule=schedule,erasure=erasure,service=service,budget=4)
            m=Model(c);ps={k:Planner(m,p,d) for k,p,d in POLICIES};rows=[]
            for s,l,n0 in product(range(3),range(3),range(1,4)):
                b=witness_belief((s,l),'0'*n0+'1'*(4-n0))
                reports={k:p.report(b) for k,p in ps.items()}
                lazy,_=select_lazy(m,b)
                reports['lazy']=lazy['policy']
                opt=F(reports['exact']['objective'])
                for k,v in reports.items():
                    if F(v['objective'])<opt or v['worst_credits']>c.budget:raise AssertionError('dominance/budget')
                    if k in ('qmdp','depth2','exact','lazy') and F(v['lower'])>opt:raise AssertionError('invalid bound')
                    if k=='lazy' and not F(lazy['lower'])<=opt<=F(lazy['upper']):raise AssertionError('invalid lazy interval')
                if not lazy['exact'] or F(lazy['upper'])!=opt:raise AssertionError('full-cap certification')
                oracle=min(F(reports[k]['objective']) for k in FIXED)
                rows.append({'q':[s,l],'n0':n0,'n1':4-n0,'worlds':mass(b),'policy':{k:{kk:v[kk] for kk in ('objective','stock','credits','worst_credits','mode','lower','gap')} for k,v in reports.items()},'classwise_fixed':str(oracle),'gain_vs_classwise_fixed':str(oracle-opt),'lazy':{k:lazy[k] for k in ('selected_depth','explored_depth','evaluations','lower','upper','gap','exact')}})
            n=sum(r['worlds'] for r in rows);assert n==126 and len(rows)==27
            weighted=lambda f:sum((r['worlds']*F(f(r)) for r in rows),F(0))/n
            costs={k:weighted(lambda r:r['policy'][k]['objective']) for k in (*ps,'lazy')}
            credits={k:weighted(lambda r:r['policy'][k]['credits']) for k in (*ps,'lazy')}
            baseline=min(FIXED,key=lambda k:costs[k]);oracle=weighted(lambda r:r['classwise_fixed']);opt=costs['exact']
            out.append({'law':name,'schedule':schedule,'worlds':n,'classes':len(rows),'objective':{k:str(v) for k,v in costs.items()},'credits':{k:str(v) for k,v in credits.items()},'best_global_fixed':baseline,'best_global_gain':str(costs[baseline]-opt),'classwise_fixed_cost':str(oracle),'classwise_gain':str(oracle-opt),'positive_vs_classwise_classes':sum(F(r['gain_vs_classwise_fixed'])>0 for r in rows),'positive_vs_free_classes':sum(F(r['policy']['free']['objective'])>F(r['policy']['exact']['objective']) for r in rows),'depth2_failures':sum(F(r['policy']['depth2']['objective'])>F(r['policy']['exact']['objective']) for r in rows),'qmdp_failures':sum(F(r['policy']['qmdp']['objective'])>F(r['policy']['exact']['objective']) for r in rows),'lazy_depth_counts':{str(d):sum(r['lazy']['explored_depth']==d for r in rows) for d in range(1,5)},'rows':rows})
            print(name,schedule,'complete',flush=True,file=__import__('sys').stderr)
    return out
if __name__=='__main__': print(json.dumps(run(),indent=2))
