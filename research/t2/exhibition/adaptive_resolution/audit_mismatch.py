"""Exact model-mismatch evaluation: separate nominal belief and true events."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json
from model import Config,Model,witness_belief,CREDITS,PRICE,mass
from planner import Planner
from trace import advance

LAWS={'ideal':('fixed',F(0)),'service':('random',F(0)),'broad':('random',F(1,4)),'erasure':('fixed',F(1,4))}
def config(name):
    service,erasure=LAWS[name]
    return Config(service=service,erasure=erasure,schedule=(1,2,3,4),budget=4)

def evaluate(nominal,actual,depth,b):
    p=Planner(Model(config(nominal)),depth=depth);true=config(actual)
    services=(2,) if true.service=='fixed' else (1,2);abort=Counter();completed=F(0);stock=F(0);credits=F(0);leaves=0
    def walk(b,h,k,x,prob,r,c):
        nonlocal completed,stock,credits,leaves
        for s,z in product(services,('0','1')):
            for erased,weight in ((False,1-true.erasure),(True,true.erasure)) if h>1 else ((False,F(1)),):
                if not weight:continue
                pr=prob*weight/(2*len(services))
                try:bb,kk,y,row=advance(p,b,h,k,x,s,z,erased)
                except ValueError as e:
                    if not str(e).startswith('OUT_OF_SUPPORT'):raise
                    abort[(5-h,str(e))]+=pr;continue
                rr=r+row['stock'];cc=c+CREDITS[row['mode']]
                if cc>4:raise AssertionError('budget')
                if h==1:completed+=pr;stock+=pr*rr;credits+=pr*cc;leaves+=1
                else:walk(bb,h-1,kk,y,pr,rr,cc)
    for x,w in b:walk(b,4,4,x,F(w,mass(b)),0,0)
    if completed+sum(abort.values())!=1:raise AssertionError('mass')
    conditional=(stock+PRICE*credits)/completed if completed else None
    return {'nominal':nominal,'actual':actual,'depth':depth,'complete_probability':str(completed),'abort_probability':str(1-completed),'abort_by_stage':[{'stage':stage,'reason':reason,'mass':str(pr)} for (stage,reason),pr in sorted(abort.items())],'conditional_complete_cost':str(conditional) if conditional is not None else None,'true_exact':str(F(Planner(Model(true)).report(b)['objective'])),'unconditional_regret':str(conditional-F(Planner(Model(true)).report(b)['objective'])) if completed==1 else None,'completed_leaves':leaves}

if __name__=='__main__':
    b=witness_belief();r=[evaluate(n,a,d,b) for n,a,d in product(('ideal','service','broad'),LAWS,(2,4))]
    for x in r:
        if x['nominal']==x['actual']:assert x['abort_probability']=='0' and x['unconditional_regret']=='0'
        if x['nominal']=='broad':assert x['abort_probability']=='0'
    print(json.dumps(r,indent=2))
