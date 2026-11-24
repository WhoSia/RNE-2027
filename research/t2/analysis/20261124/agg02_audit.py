"""Independent native conditional-transfer audit, abstract synthetic model only."""
from collections import defaultdict
from itertools import product
import json

CLOCKS=('dense','platoon','sparse')
NAMES=('context','count_independent','count_joint','movement_joint')

def tape(seed,left,clock):
    order=list(range(24)); x=seed+1
    for i in range(23,0,-1):
        x=(1664525*x+1013904223)&0xffffffff;j=x%(i+1)
        order[i],order[j]=order[j],order[i]
    return {(i if clock=='dense' else 8*(i//4)+i%4 if clock=='platoon' else 4*i):('L' if v<left else 'S') for i,v in enumerate(order)}

def blocks(seed,left,clock,P,R,g,o):
    arrivals=tape(seed,left,clock); q=();p=r=A=Y=Z=0
    for t in range(240):
        if t>=16 and t%8==0:
            ctx=(P,R,g,o,t//8);ct=ctx+(len(q),p,r);mv=ct+(q.count('S'),q.count('L'),q[0] if q else '-')
            keys=(ctx,ct,mv);active=bool(q);D=B=X=0
        green=t%8<(4 if t<16 else g); down=(t+(0 if t<16 else o))%8<4
        h=q[0] if q else None; demand=int(h=='S' and green);space=int(r<R);flow=demand*space
        admit=int(h=='L' and p<P);ly=int(not green and p>0);sz=int(r>0 and down)
        v=arrivals.get(t);q=q[flow+admit:]+((v,) if v else ());p+=admit-ly;r+=flow-sz;A+=int(v is not None);Y+=ly;Z+=sz
        assert A==len(q)+p+r+Y+Z and 0<=p<=P and 0<=r<=R
        if t>=16:
            D+=demand;B+=space;X+=flow
            if t%8==7:
                assert X<=min(D,B)
                yield keys,active,D,B,X
    assert A==Y+Z==24

def run():
    maps=[defaultdict(lambda:[0,0,0,0,set()]) for _ in range(3)]
    seeds=[s for s in range(60) if s%5];coverage=[0,0,0]; stats={k:{n:[0,0,0.,0.,0.] for n in NAMES} for k in ('all','active_at_start',*CLOCKS)}
    train_n=test_n=0
    for seed,left,clock,P,R,g,o in product(seeds,(6,12,18),CLOCKS,(1,3),(1,3),(3,4,5),(0,2,4,6)):
        train_n+=1
        for keys,active,d,b,x in blocks(seed,left,clock,P,R,g,o):
            for m,k in zip(maps,keys):
                z=m[k];z[0]+=1;z[1]+=d;z[2]+=b;z[3]+=x;z[4].add(seed)
    supported=lambda v:v is not None and len(v[4])>=4
    seed_abs=defaultdict(lambda:[[0.]*4,[0.]*4])
    for seed,left,clock,P,R,g,o in product(range(160,180),(6,12,18),CLOCKS,(1,3),(1,3),(3,4,5),(0,2,4,6)):
        test_n+=1
        for keys,active,d,b,x in blocks(seed,left,clock,P,R,g,o):
            base,ct,mv=[m.get(k) for m,k in zip(maps,keys)];assert supported(base)
            coverage[0]+=int(supported(ct));coverage[1]+=int(supported(mv));coverage[2]+=1
            ct=ct if supported(ct) else base;mv=mv if supported(mv) else ct
            pred=(base[3]/base[0],ct[1]*ct[2]/(8*ct[0]**2),ct[3]/ct[0],mv[3]/mv[0])
            for i,(n,v) in enumerate(zip(NAMES,pred)):
                err=v-x;seed_abs[seed][0][i]+=abs(err)
                if active:seed_abs[seed][1][i]+=abs(err)
                for k in ('all',clock)+(('active_at_start',) if active else ()):
                    z=stats[k][n];z[0]+=1;z[1]+=x;z[2]+=err;z[3]+=abs(err);z[4]+=err*err
    assert (train_n,test_n)==(20736,8640)
    return dict(trainArms=train_n,testArms=test_n,coverage=dict(zip(('count','movement','total'),coverage)),cells=[dict(all=len(m),supported=sum(supported(v) for v in m.values())) for m in maps],columns=['n','actual','signed','absolute','squared'],stats=stats,seed_absolute=seed_abs)

if __name__=='__main__':print(json.dumps(run(),indent=2))
