"""Separate event-path enumeration; shares model and chosen policy, not value evaluator."""
from fractions import Fraction as F
from itertools import product
from model import CREDITS,mass
from objective import NAMES,ZERO,add,weighted
from trace import advance

def enumerate_vector(p,b):
    c=p.model.c;services=(2,) if c.service=='fixed' else (1,2);total=F(0);v=ZERO;worst=0;leaves=0
    def walk(b,h,k,x,prob,acc):
        nonlocal total,v,worst,leaves
        for s,z in product(services,('0','1')):
            for erased,e in ((False,1-c.erasure),(True,c.erasure)) if h>1 else ((False,F(1)),):
                if not e:continue
                q=prob*e/(2*len(services));nb,nk,y,row=advance(p,b,h,k,x,s,z,erased)
                # independently calculate residual movement stock from previous state and actual departures
                st=[x[0]+x[2].count('0'),x[1]+x[2].count('1')];a=row['action'];st[a]-=min(x[a],s)
                assert sum(st)==row['stock']
                av=add(acc,(st[0],st[1],max(st),sum(st) if h==1 else 0,CREDITS[row['mode']]))
                if h==1:
                    leaves+=1;total+=q;v=add(v,tuple(q*t for t in av));worst=max(worst,av[4])
                else:walk(nb,h-1,nk,y,q,av)
    for x,w in b:walk(b,c.horizon,c.budget,x,F(w,mass(b)),ZERO)
    assert total==1 and worst<=c.budget
    return {'vector':{n:str(x) for n,x in zip(NAMES,v)},'objective':str(p.obj.cost(v)),'worst_credits':int(worst),'leaves':leaves}
