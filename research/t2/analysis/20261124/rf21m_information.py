"""RF21-M: ideal synthetic state information, not measured RF performance."""
from collections import defaultdict
from itertools import product
import json
from macro02b_audit import POL,CLOCKS,tape,tick

NAMES=('geometry','presence','fullness','both','counts')
def keys(ctx,obs):
    P,R=ctx;q,p,r=obs
    presence=(q>0,p>0,r>0);fullness=(q>0,p==P,r==R)
    return ctx,ctx+presence,ctx+fullness,ctx+presence+fullness,ctx+obs

def run():
    train=[defaultdict(list) for _ in NAMES];test=[];ntrain=0
    for seed,left,clock,P,R in product((*[s for s in range(60) if s%5],*range(80,100)),(6,12,18),CLOCKS,(1,3),(1,3)):
        ar=tape(seed,left,clock);s=((),)+(0,)*11
        for t in range(16):s=tick(s,t,4,0,P,R,ar.get(t),False)
        q,p,r,A,B,*_=s;frac=A/(A+B);dem=POL.index((5 if frac>=.75 else 3 if frac<=.25 else 4,0))
        cs=[]
        for g,o in POL:
            z=s
            for t in range(16,240):
                z=tick(z,t,g,o,P,R,ar.get(t),False)
                if z[5]+z[6]==24:break
            assert z[3]+z[4]==z[5]+z[6]==24
            cs.append(z[7]+z[8])
        ks=keys((P,R),(len(q),p,r));row=(seed,ks,dem,cs,min(cs))
        if seed<60:
            ntrain+=1
            for m,k in zip(train,ks):m[k].append(row)
        else:test.append(row)
    assert ntrain==1728 and len(test)==720
    choices=[{k:min(range(12),key=lambda i:sum(r[3][i] for r in rows)) for k,rows in m.items() if len({r[0] for r in rows})>=4} for m in train]
    names=(*NAMES,'demand');stats={n:dict(n=0,covered=0,J=0,regret=0,worst=0,better=0,tie=0,worse=0,miss=0) for n in names}
    partitions=[defaultdict(list) for _ in NAMES]
    for row in test:
        _,ks,dem,cs,best=row;base=choices[0][ks[0]];acts=[m.get(k) for m,k in zip(choices,ks)]+[dem]
        for m,k in zip(partitions,ks):m[k].append({i for i,c in enumerate(cs) if c==best})
        for n,a in zip(names,acts):
            z=stats[n];z['n']+=1;z['covered']+=a is not None;J=cs[base if a is None else a];d=J-best
            z['J']+=J;z['regret']+=d;z['worst']=max(z['worst'],d);z['better']+=J<cs[base];z['tie']+=J==cs[base];z['worse']+=J>cs[base];z['miss']+=d>0
    collisions={}
    for n,m in zip(NAMES,partitions):
        bad=[v for v in m.values() if not set.intersection(*v)];collisions[n]=dict(cells=len(m),incompatible=len(bad),worlds=sum(map(len,bad)))
    return dict(status='IDEAL_SYNTHETIC_OBSERVATION_NOT_RF_MEASUREMENT',train=ntrain,test=len(test),arms=29376,stats=stats,collisions=collisions)

if __name__=='__main__':print(json.dumps(run(),indent=2))
