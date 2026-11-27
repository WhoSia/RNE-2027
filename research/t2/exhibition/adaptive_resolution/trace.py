"""Causal replay: only environment observes the hidden physical state."""
from itertools import product
from fractions import Fraction as F
from model import CREDITS,PRICE,mass


def advance(planner,b,h,k,x,service,arrival,erased):
    model=planner.model
    m=planner.sense(b,h,k,min(h,planner.depth))[1]
    if CREDITS[m]>k:raise AssertionError('budget')
    value=None
    if m:
        value=model.observe(x,m)
        if value not in model.partition(b,m):raise ValueError('OUT_OF_SUPPORT: paid observation')
        b=model.partition(b,m)[value][1]
    k-=CREDITS[m]
    a=planner.control(b,h,k,min(h,planner.depth))[1]
    y,stock=model.transition(x,a,service,arrival)
    free=model.observe(y,0,erased)
    if h>1:
        _,p=model.predict(b,a)
        if free not in p:raise ValueError('OUT_OF_SUPPORT: free observation')
        next_b=p[free][1]
    else:next_b=None
    row={'stage':model.c.horizon-h+1,'mode':m,'paid_value':value,'action':a,'posterior_support':len(b),'remaining_budget':k,'stock':stock,'free_next':free,'next_support':len(next_b) if next_b else None,'truth_before':x,'truth_after':y,'service':service,'arrival':arrival,'erased':erased}
    return next_b,k,y,row


def replay(planner,b,truth,events):
    if truth not in dict(b):raise ValueError('OUT_OF_SUPPORT: initial state')
    h=planner.model.c.horizon;k=planner.model.c.budget;rows=[]
    if len(events)!=h:raise ValueError('event length')
    for service,arrival,erased in events:
        b,k,truth,row=advance(planner,b,h,k,truth,service,arrival,erased);rows.append(row);h-=1
    return {'rows':rows,'stock':sum(r['stock'] for r in rows),'credits':planner.model.c.budget-k}


def exhaustive(planner,b):
    """Separate event-tree evaluator, no calls to planner.evaluate or its cache."""
    m=planner.model;c=m.c;total=F(0);stock=F(0);credits=F(0);worst=0;leaves=0
    services=(2,) if c.service=='fixed' else (1,2)
    def walk(b,h,k,x,weight,acc,used):
        nonlocal total,stock,credits,worst,leaves
        for s,z in product(services,('0','1')):
            for erased,prob in ((False,1-c.erasure),(True,c.erasure)) if h>1 else ((False,F(1)),):
                if not prob:continue
                p=weight*prob/(2*len(services));nb,nk,y,row=advance(planner,b,h,k,x,s,z,erased)
                ns=acc+row['stock'];nu=used+CREDITS[row['mode']]
                if h==1:
                    leaves+=1;total+=p;stock+=p*ns;credits+=p*nu;worst=max(worst,nu)
                else:walk(nb,h-1,nk,y,p,ns,nu)
    for x,w in b:walk(b,c.horizon,c.budget,x,F(w,mass(b)),0,0)
    if total!=1 or worst>c.budget:raise AssertionError('event tree mass/budget')
    return {'objective':str(stock+PRICE*credits),'stock':str(stock),'credits':str(credits),'worst_credits':worst,'leaves':leaves}
